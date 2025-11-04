"""Web UI server for ETH Gas Tracker."""
import asyncio
import json
from pathlib import Path
from typing import Optional
from datetime import datetime
from aiohttp import web
import aiohttp

from .tracker import GasTracker
from .networks import NETWORKS, TX_TYPES
from .history import GasHistory
from .stats import GasStats
from .compare import NetworkComparator
from .prediction import GasPredictor


class WebUI:
    """Web-based user interface for gas tracking."""

    def __init__(self, host: str = "0.0.0.0", port: int = 8080):
        """Initialize Web UI server."""
        self.host = host
        self.port = port
        self.app = web.Application()
        self.history = GasHistory()
        self._setup_routes()

    def _setup_routes(self):
        """Setup HTTP routes."""
        self.app.router.add_get("/", self.handle_index)
        self.app.router.add_get("/dashboard", self.handle_dashboard)
        self.app.router.add_get("/api/networks", self.api_get_networks)
        self.app.router.add_get("/api/gas/{network}", self.api_get_gas)
        self.app.router.add_get("/api/compare", self.api_compare_networks)
        self.app.router.add_get("/api/history/{network}", self.api_get_history)
        self.app.router.add_get("/api/stats/{network}", self.api_get_stats)
        self.app.router.add_get("/api/predict/{network}", self.api_predict)
        self.app.router.add_static("/static", Path(__file__).parent / "static", name="static")

    async def handle_index(self, request):
        """Serve main HTML page."""
        html = self._get_html_template()
        return web.Response(text=html, content_type="text/html")

    async def handle_dashboard(self, request):
        """Serve dashboard page."""
        return await self.handle_index(request)

    async def api_get_networks(self, request):
        """API: Get list of available networks."""
        networks = {
            network_id: {
                "name": network["name"],
                "chain_id": network["chain_id"],
                "explorer": network["explorer"]
            }
            for network_id, network in NETWORKS.items()
        }
        return web.json_response(networks)

    async def api_get_gas(self, request):
        """API: Get gas prices for a network."""
        network_id = request.match_info["network"]

        if network_id not in NETWORKS:
            return web.json_response(
                {"error": f"Unknown network: {network_id}"},
                status=404
            )

        network = NETWORKS[network_id]
        tracker = GasTracker(network["rpc"], network["coingecko_id"])

        try:
            data = await tracker.get_gas_data()
            data["network"] = network["name"]
            data["network_id"] = network_id
            return web.json_response(data)
        except Exception as e:
            return web.json_response(
                {"error": str(e)},
                status=500
            )

    async def api_compare_networks(self, request):
        """API: Compare gas prices across all networks."""
        comparator = NetworkComparator()

        try:
            data = await comparator.get_all_gas_data()
            return web.json_response(data)
        except Exception as e:
            return web.json_response(
                {"error": str(e)},
                status=500
            )

    async def api_get_history(self, request):
        """API: Get historical data for a network."""
        network_id = request.match_info["network"]
        limit = int(request.query.get("limit", 100))

        if network_id not in NETWORKS:
            return web.json_response(
                {"error": f"Unknown network: {network_id}"},
                status=404
            )

        network_name = NETWORKS[network_id]["name"]
        records = self.history.get_records(network=network_name, limit=limit)

        return web.json_response(records)

    async def api_get_stats(self, request):
        """API: Get statistics for a network."""
        network_id = request.match_info["network"]
        hours = int(request.query.get("hours", 24))

        if network_id not in NETWORKS:
            return web.json_response(
                {"error": f"Unknown network: {network_id}"},
                status=404
            )

        network_name = NETWORKS[network_id]["name"]
        records = self.history.get_records(network=network_name)
        filtered = GasStats.filter_by_timeframe(records, hours)

        if not filtered:
            return web.json_response(
                {"error": "No historical data available"},
                status=404
            )

        stats = GasStats.calculate_advanced_stats(filtered)
        return web.json_response(stats)

    async def api_predict(self, request):
        """API: Predict gas prices for a network."""
        network_id = request.match_info["network"]
        method = request.query.get("method", "moving_average")

        if network_id not in NETWORKS:
            return web.json_response(
                {"error": f"Unknown network: {network_id}"},
                status=404
            )

        network_name = NETWORKS[network_id]["name"]
        records = self.history.get_records(network=network_name, limit=100)

        if not records:
            return web.json_response(
                {"error": "No historical data available for prediction"},
                status=404
            )

        predictor = GasPredictor(records)
        prediction = predictor.predict_next_hour(method=method)

        return web.json_response(prediction)

    def _get_html_template(self) -> str:
        """Get HTML template for web UI."""
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ETH Gas Tracker - Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            color: white;
            margin-bottom: 30px;
        }

        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
        }

        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .card {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
        }

        .card-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0f0f0;
        }

        .network-name {
            font-size: 1.4em;
            font-weight: bold;
            color: #667eea;
        }

        .loading {
            color: #999;
            font-style: italic;
        }

        .error {
            color: #e74c3c;
        }

        .gas-info {
            margin: 15px 0;
        }

        .gas-row {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
            border-bottom: 1px solid #f5f5f5;
        }

        .gas-label {
            color: #666;
        }

        .gas-value {
            font-weight: bold;
            font-size: 1.1em;
        }

        .price-indicator {
            display: inline-block;
            width: 12px;
            height: 12px;
            border-radius: 50%;
            margin-left: 8px;
        }

        .price-low { background: #27ae60; }
        .price-medium { background: #f39c12; }
        .price-high { background: #e74c3c; }

        .controls {
            background: white;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        .controls h2 {
            margin-bottom: 15px;
            color: #667eea;
        }

        button {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 1em;
            margin-right: 10px;
            transition: background 0.2s;
        }

        button:hover {
            background: #5568d3;
        }

        button:disabled {
            background: #ccc;
            cursor: not-allowed;
        }

        .refresh-indicator {
            display: inline-block;
            margin-left: 10px;
            color: #666;
            font-size: 0.9em;
        }

        .comparison-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }

        .comparison-table th,
        .comparison-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #f0f0f0;
        }

        .comparison-table th {
            background: #f8f9fa;
            font-weight: bold;
            color: #667eea;
        }

        .comparison-table tr:hover {
            background: #f8f9fa;
        }

        .winner {
            background: #d4edda !important;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .spinner {
            display: inline-block;
            width: 14px;
            height: 14px;
            border: 2px solid #f3f3f3;
            border-top: 2px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>⛽ ETH Gas Tracker</h1>
            <p class="subtitle">Real-time gas prices across multiple networks</p>
        </header>

        <div class="controls">
            <h2>Controls</h2>
            <button onclick="refreshAll()">🔄 Refresh All</button>
            <button onclick="toggleAutoRefresh()">
                <span id="auto-refresh-text">▶️ Start Auto-Refresh</span>
            </button>
            <button onclick="showComparison()">📊 Compare Networks</button>
            <span class="refresh-indicator" id="refresh-indicator"></span>
        </div>

        <div class="grid" id="network-grid"></div>

        <div id="comparison-section" style="display: none;">
            <div class="card" style="grid-column: 1 / -1;">
                <div class="card-header">
                    <h2>Network Comparison</h2>
                </div>
                <div id="comparison-content"></div>
            </div>
        </div>
    </div>

    <script>
        let autoRefreshInterval = null;
        let isAutoRefreshing = false;

        async function fetchNetworks() {
            const response = await fetch('/api/networks');
            return await response.json();
        }

        async function fetchGasData(networkId) {
            try {
                const response = await fetch(`/api/gas/${networkId}`);
                return await response.json();
            } catch (error) {
                return { error: error.message };
            }
        }

        function getPriceIndicator(baseeFee) {
            if (baseeFee < 20) return 'price-low';
            if (baseeFee < 50) return 'price-medium';
            return 'price-high';
        }

        function renderNetworkCard(networkId, networkInfo, gasData) {
            const card = document.createElement('div');
            card.className = 'card';
            card.id = `card-${networkId}`;

            let content = `
                <div class="card-header">
                    <span class="network-name">${networkInfo.name}</span>
                </div>
            `;

            if (gasData.error) {
                content += `<div class="error">❌ Error: ${gasData.error}</div>`;
            } else if (!gasData.base_fee_gwei) {
                content += `<div class="loading">Loading...</div>`;
            } else {
                const indicator = getPriceIndicator(gasData.base_fee_gwei);
                content += `
                    <div class="gas-info">
                        <div class="gas-row">
                            <span class="gas-label">Base Fee:</span>
                            <span class="gas-value">
                                ${gasData.base_fee_gwei.toFixed(2)} gwei
                                <span class="price-indicator ${indicator}"></span>
                            </span>
                        </div>
                        <div class="gas-row">
                            <span class="gas-label">Priority Tip:</span>
                            <span class="gas-value">${gasData.priority_tip_gwei.toFixed(2)} gwei</span>
                        </div>
                        <div class="gas-row">
                            <span class="gas-label">Max Fee:</span>
                            <span class="gas-value">${gasData.max_fee_gwei.toFixed(2)} gwei</span>
                        </div>
                        ${gasData.token_price_usd ? `
                        <div class="gas-row">
                            <span class="gas-label">Token Price:</span>
                            <span class="gas-value">$${gasData.token_price_usd.toFixed(2)}</span>
                        </div>
                        ` : ''}
                        ${gasData.simple_transfer_usd ? `
                        <div class="gas-row">
                            <span class="gas-label">Simple Transfer:</span>
                            <span class="gas-value">$${gasData.simple_transfer_usd.toFixed(4)}</span>
                        </div>
                        ` : ''}
                    </div>
                `;
            }

            card.innerHTML = content;
            return card;
        }

        async function loadNetwork(networkId, networkInfo) {
            const gasData = await fetchGasData(networkId);
            const grid = document.getElementById('network-grid');
            const existingCard = document.getElementById(`card-${networkId}`);
            const newCard = renderNetworkCard(networkId, networkInfo, gasData);

            if (existingCard) {
                existingCard.replaceWith(newCard);
            } else {
                grid.appendChild(newCard);
            }
        }

        async function refreshAll() {
            document.getElementById('refresh-indicator').innerHTML = '<span class="spinner"></span> Refreshing...';
            const networks = await fetchNetworks();
            const promises = Object.entries(networks).map(([id, info]) =>
                loadNetwork(id, info)
            );
            await Promise.all(promises);
            document.getElementById('refresh-indicator').textContent = `Last updated: ${new Date().toLocaleTimeString()}`;
        }

        function toggleAutoRefresh() {
            isAutoRefreshing = !isAutoRefreshing;
            const button = document.getElementById('auto-refresh-text');

            if (isAutoRefreshing) {
                button.textContent = '⏸️ Stop Auto-Refresh';
                refreshAll();
                autoRefreshInterval = setInterval(refreshAll, 10000); // 10 seconds
            } else {
                button.textContent = '▶️ Start Auto-Refresh';
                if (autoRefreshInterval) {
                    clearInterval(autoRefreshInterval);
                    autoRefreshInterval = null;
                }
            }
        }

        async function showComparison() {
            const section = document.getElementById('comparison-section');
            section.style.display = 'block';

            const content = document.getElementById('comparison-content');
            content.innerHTML = '<div class="loading"><span class="spinner"></span> Loading comparison...</div>';

            const response = await fetch('/api/compare');
            const data = await response.json();

            // Calculate costs for simple transfer
            const costs = [];
            for (const [networkId, gasData] of Object.entries(data)) {
                if (!gasData.error && gasData.max_fee_gwei) {
                    const costNative = (gasData.max_fee_gwei * 1e-9) * 21000;
                    const costUsd = costNative * (gasData.token_price_usd || 0);
                    costs.push({
                        network: gasData.network || networkId,
                        baseFee: gasData.base_fee_gwei,
                        maxFee: gasData.max_fee_gwei,
                        costUsd: costUsd
                    });
                }
            }

            costs.sort((a, b) => a.costUsd - b.costUsd);

            let table = '<table class="comparison-table"><thead><tr>';
            table += '<th>Rank</th><th>Network</th><th>Base Fee</th><th>Max Fee</th><th>Cost (USD)</th>';
            table += '</tr></thead><tbody>';

            costs.forEach((item, index) => {
                const rowClass = index === 0 ? 'winner' : '';
                table += `<tr class="${rowClass}">`;
                table += `<td>${index === 0 ? '🏆' : index + 1}</td>`;
                table += `<td>${item.network}</td>`;
                table += `<td>${item.baseFee.toFixed(2)} gwei</td>`;
                table += `<td>${item.maxFee.toFixed(2)} gwei</td>`;
                table += `<td>$${item.costUsd.toFixed(4)}</td>`;
                table += '</tr>';
            });

            table += '</tbody></table>';
            content.innerHTML = table;
        }

        // Initialize on load
        refreshAll();
    </script>
</body>
</html>"""

    async def start(self):
        """Start the web server."""
        runner = web.AppRunner(self.app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        print(f"🌐 Web UI started at http://{self.host}:{self.port}")
        print("   Press Ctrl+C to stop")


def run_web_ui(host: str = "0.0.0.0", port: int = 8080):
    """
    Run the web UI server.

    Args:
        host: Host address to bind to
        port: Port number to listen on
    """
    ui = WebUI(host, port)

    async def run():
        await ui.start()
        # Keep running
        try:
            await asyncio.Event().wait()
        except KeyboardInterrupt:
            print("\n👋 Shutting down...")

    asyncio.run(run())
