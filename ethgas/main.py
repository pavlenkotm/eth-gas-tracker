import argparse
import asyncio
import aiohttp
import math

DEFAULT_RPC = "https://eth.llamarpc.com"  # любой общий ETH RPC
COINGECKO = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"

async def eth_call(session, url, payload):
    async with session.post(url, json=payload, timeout=15) as r:
        r.raise_for_status()
        return await r.json()

async def get_base_fee_gwei(session, rpc_url):
    # eth_feeHistory на 1 блок возвращает baseFeePerGas следующего блока
    payload = {"jsonrpc":"2.0","id":1,"method":"eth_feeHistory","params":[1,"latest",[]]}
    data = await eth_call(session, rpc_url, payload)
    base_wei = int(data["result"]["baseFeePerGas"][-1], 16)
    return base_wei / 1e9  # gwei

async def get_eth_usd(session):
    try:
        data = await (await session.get(COINGECKO, timeout=10)).json()
        return float(data["ethereum"]["usd"])
    except Exception:
        return None

async def main():
    p = argparse.ArgumentParser(description="ETH Gas Tracker (no API keys).")
    p.add_argument("--rpc", default=DEFAULT_RPC, help="Ethereum RPC URL")
    p.add_argument("--priority", type=float, default=1.5, help="priority tip in gwei (default 1.5)")
    p.add_argument("--show-usd", action="store_true", help="estimate tx cost in USD (simple transfer, 21k gas)")
    args = p.parse_args()

    async with aiohttp.ClientSession() as session:
        base = await get_base_fee_gwei(session, args.rpc)
        max_fee = base + args.priority
        line = f"Base: {base:.1f} gwei | Priority: {args.priority:.1f} | Max: {max_fee:.1f}"

        if args.show_usd:
            price = await get_eth_usd(session)
            if price:
                # оценка для простой L1-транзакции 21_000 газа
                usd = (max_fee * 1e-9) * 21000 * price
                line += f" | Tx ≈ ${usd:.2f}"

        print(line)

if __name__ == "__main__":
    asyncio.run(main())
