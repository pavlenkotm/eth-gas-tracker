"""Core gas tracking functionality."""

import aiohttp
from typing import Dict, Optional

COINGECKO_API = "https://api.coingecko.com/api/v3/simple/price"


class GasTracker:
    """Tracks gas prices for a specific network."""

    def __init__(self, rpc_url: str, coingecko_id: str, network_name: str = "Ethereum"):
        self.rpc_url = rpc_url
        self.coingecko_id = coingecko_id
        self.network_name = network_name

    async def eth_call(self, session: aiohttp.ClientSession, payload: dict) -> dict:
        """Make a JSON-RPC call to the network."""
        async with session.post(self.rpc_url, json=payload, timeout=15) as r:
            r.raise_for_status()
            return await r.json()

    async def get_base_fee_gwei(self, session: aiohttp.ClientSession) -> float:
        """Get current base fee in gwei using eth_feeHistory."""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "eth_feeHistory",
            "params": [1, "latest", []],
        }
        data = await self.eth_call(session, payload)
        base_wei = int(data["result"]["baseFeePerGas"][-1], 16)
        return base_wei / 1e9

    async def get_token_price_usd(self, session: aiohttp.ClientSession) -> Optional[float]:
        """Get token price in USD from CoinGecko."""
        try:
            url = f"{COINGECKO_API}?ids={self.coingecko_id}&vs_currencies=usd"
            async with session.get(url, timeout=10) as r:
                data = await r.json()
                return float(data[self.coingecko_id]["usd"])
        except Exception:
            return None

    async def get_gas_data(
        self, session: aiohttp.ClientSession, priority_tip: float = 1.5
    ) -> Dict:
        """Get comprehensive gas data including base fee, priority, and prices."""
        base_fee = await self.get_base_fee_gwei(session)
        max_fee = base_fee + priority_tip
        token_price = await self.get_token_price_usd(session)

        return {
            "network": self.network_name,
            "base_fee": base_fee,
            "priority_tip": priority_tip,
            "max_fee": max_fee,
            "token_price_usd": token_price,
        }

    def calculate_tx_cost(
        self, gas_price_gwei: float, gas_units: int, token_price_usd: Optional[float]
    ) -> Dict:
        """Calculate transaction cost in native token and USD."""
        cost_native = (gas_price_gwei * 1e-9) * gas_units
        cost_usd = cost_native * token_price_usd if token_price_usd else None

        return {"cost_native": cost_native, "cost_usd": cost_usd, "gas_units": gas_units}
