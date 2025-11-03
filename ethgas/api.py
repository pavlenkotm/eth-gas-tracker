"""Simple REST API server for gas price data."""

import asyncio
import json
from aiohttp import web
from typing import Dict

from .tracker import GasTracker
from .networks import NETWORKS, TX_TYPES
from .history import GasHistory
from .stats import GasStats


class GasAPI:
    """REST API server for gas tracking."""

    def __init__(self, host: str = "0.0.0.0", port: int = 8080):
        self.host = host
        self.port = port
        self.app = web.Application()
        self.history = GasHistory()
        self.setup_routes()

    def setup_routes(self):
        """Setup API routes."""
        self.app.router.add_get("/", self.index)
        self.app.router.add_get("/gas/{network}", self.get_gas)
        self.app.router.add_get("/networks", self.get_networks)
        self.app.router.add_get("/history/{network}", self.get_history)
        self.app.router.add_get("/stats/{network}", self.get_stats)
        self.app.router.add_get("/health", self.health_check)

    async def index(self, request: web.Request) -> web.Response:
        """API documentation endpoint."""
        docs = {
            "service": "ETH Gas Tracker API",
            "version": "1.0.0",
            "endpoints": {
                "/": "This documentation",
                "/gas/{network}": "Get current gas prices for network",
                "/networks": "List available networks",
                "/history/{network}": "Get historical data (params: limit=N)",
                "/stats/{network}": "Get statistics (params: hours=N)",
                "/health": "Health check",
            },
            "available_networks": list(NETWORKS.keys()),
        }
        return web.json_response(docs)

    async def get_gas(self, request: web.Request) -> web.Response:
        """Get current gas prices for a network."""
        network_name = request.match_info["network"]

        if network_name not in NETWORKS:
            return web.json_response(
                {"error": f"Unknown network: {network_name}"}, status=404
            )

        network = NETWORKS[network_name]
        tracker = GasTracker(
            network["rpc"], network["coingecko_id"], network["name"]
        )

        try:
            async with web.ClientSession() as session:
                gas_data = await tracker.get_gas_data(session)

                # Calculate costs for different tx types
                tx_costs = {}
                for tx_type, tx_info in TX_TYPES.items():
                    cost = tracker.calculate_tx_cost(
                        gas_data["max_fee"],
                        tx_info["gas"],
                        gas_data["token_price_usd"],
                    )
                    tx_costs[tx_type] = {
                        "name": tx_info["name"],
                        "gas_units": tx_info["gas"],
                        "cost_usd": cost["cost_usd"],
                    }

                response = {
                    **gas_data,
                    "tx_costs": tx_costs,
                }

                return web.json_response(response)

        except Exception as e:
            return web.json_response({"error": str(e)}, status=500)

    async def get_networks(self, request: web.Request) -> web.Response:
        """List all available networks."""
        networks_list = []
        for key, info in NETWORKS.items():
            networks_list.append(
                {
                    "id": key,
                    "name": info["name"],
                    "chain_id": info["chain_id"],
                    "explorer": info["explorer"],
                }
            )
        return web.json_response({"networks": networks_list})

    async def get_history(self, request: web.Request) -> web.Response:
        """Get historical gas data for a network."""
        network_name = request.match_info["network"]
        limit = int(request.query.get("limit", 100))

        if network_name not in NETWORKS:
            return web.json_response(
                {"error": f"Unknown network: {network_name}"}, status=404
            )

        network = NETWORKS[network_name]
        records = self.history.get_records(network=network["name"], limit=limit)

        return web.json_response({"network": network["name"], "records": records})

    async def get_stats(self, request: web.Request) -> web.Response:
        """Get statistics for a network."""
        network_name = request.match_info["network"]
        hours = int(request.query.get("hours", 24))

        if network_name not in NETWORKS:
            return web.json_response(
                {"error": f"Unknown network: {network_name}"}, status=404
            )

        network = NETWORKS[network_name]
        records = self.history.get_records(network=network["name"])
        records = GasStats.filter_by_timeframe(records, hours)
        stats = GasStats.calculate_stats(records)

        if stats is None:
            return web.json_response(
                {"error": "No data available"}, status=404
            )

        return web.json_response(
            {"network": network["name"], "timeframe_hours": hours, "stats": stats}
        )

    async def health_check(self, request: web.Request) -> web.Response:
        """Health check endpoint."""
        return web.json_response({"status": "healthy"})

    def run(self):
        """Start the API server."""
        print(f"🚀 Starting Gas Tracker API on http://{self.host}:{self.port}")
        print(f"📖 API documentation: http://{self.host}:{self.port}/")
        web.run_app(self.app, host=self.host, port=self.port, print=None)
