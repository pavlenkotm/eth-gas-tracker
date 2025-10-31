"""Ethereum gas tracker using eth_feeHistory without API keys."""
import argparse
import asyncio
import sys
from typing import Optional, Dict, Any
import aiohttp

DEFAULT_RPC = "https://eth.llamarpc.com"
COINGECKO = "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd"


async def eth_call(
    session: aiohttp.ClientSession,
    url: str,
    payload: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Make a JSON-RPC call to an Ethereum node.

    Args:
        session: aiohttp client session
        url: RPC endpoint URL
        payload: JSON-RPC payload

    Returns:
        JSON-RPC response as dict

    Raises:
        aiohttp.ClientError: On network errors
        ValueError: On invalid JSON response
    """
    try:
        async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=15)) as r:
            r.raise_for_status()
            data = await r.json()

            if "error" in data:
                raise ValueError(f"RPC error: {data['error']}")

            return data
    except aiohttp.ClientError as e:
        raise aiohttp.ClientError(f"Failed to connect to RPC: {e}") from e
    except asyncio.TimeoutError as e:
        raise asyncio.TimeoutError(f"RPC request timed out: {url}") from e


async def get_base_fee_gwei(session: aiohttp.ClientSession, rpc_url: str) -> float:
    """
    Get current base fee from Ethereum network using eth_feeHistory.

    Args:
        session: aiohttp client session
        rpc_url: Ethereum RPC endpoint URL

    Returns:
        Base fee in gwei

    Raises:
        ValueError: If RPC response is invalid or missing expected fields
        aiohttp.ClientError: On network errors
    """
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "eth_feeHistory",
        "params": [1, "latest", []]
    }

    try:
        data = await eth_call(session, rpc_url, payload)

        # Validate response structure
        if "result" not in data:
            raise ValueError("Missing 'result' in RPC response")

        result = data["result"]
        if "baseFeePerGas" not in result:
            raise ValueError("Missing 'baseFeePerGas' in RPC result")

        base_fee_list = result["baseFeePerGas"]
        if not base_fee_list or len(base_fee_list) == 0:
            raise ValueError("Empty 'baseFeePerGas' array in response")

        # eth_feeHistory returns base fee for next block in last element
        base_wei = int(base_fee_list[-1], 16)
        return base_wei / 1e9  # Convert wei to gwei

    except (KeyError, IndexError, TypeError) as e:
        raise ValueError(f"Invalid RPC response structure: {e}") from e
    except ValueError as e:
        if "invalid literal" in str(e):
            raise ValueError(f"Invalid hex value in baseFeePerGas: {e}") from e
        raise


async def get_eth_usd(session: aiohttp.ClientSession) -> Optional[float]:
    """
    Get current ETH price in USD from CoinGecko.

    Args:
        session: aiohttp client session

    Returns:
        ETH price in USD, or None if request fails
    """
    try:
        async with session.get(COINGECKO, timeout=aiohttp.ClientTimeout(total=10)) as r:
            r.raise_for_status()
            data = await r.json()

        if "ethereum" not in data or "usd" not in data["ethereum"]:
            return None

        return float(data["ethereum"]["usd"])
    except (aiohttp.ClientError, ValueError, KeyError, asyncio.TimeoutError):
        return None


async def main() -> None:
    """Main entry point for ETH gas tracker CLI."""
    parser = argparse.ArgumentParser(
        description="ETH Gas Tracker (no API keys required)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--rpc",
        default=DEFAULT_RPC,
        help="Ethereum RPC URL"
    )
    parser.add_argument(
        "--priority",
        type=float,
        default=1.5,
        help="Priority tip in gwei"
    )
    parser.add_argument(
        "--show-usd",
        action="store_true",
        help="Estimate tx cost in USD (simple transfer, 21k gas)"
    )
    args = parser.parse_args()

    # Validate priority fee
    if args.priority < 0:
        print("Error: Priority fee cannot be negative", file=sys.stderr)
        sys.exit(1)

    try:
        async with aiohttp.ClientSession() as session:
            base = await get_base_fee_gwei(session, args.rpc)
            max_fee = base + args.priority
            line = f"Base: {base:.1f} gwei | Priority: {args.priority:.1f} | Max: {max_fee:.1f}"

            if args.show_usd:
                price = await get_eth_usd(session)
                if price:
                    # Estimate cost for simple L1 transaction (21,000 gas)
                    usd = (max_fee * 1e-9) * 21000 * price
                    line += f" | Tx ≈ ${usd:.2f}"
                else:
                    line += " | Tx: price unavailable"

            print(line)

    except (aiohttp.ClientError, ValueError, asyncio.TimeoutError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(130)


if __name__ == "__main__":
    asyncio.run(main())
