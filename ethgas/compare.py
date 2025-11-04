"""Network comparison functionality."""
import asyncio
import json
from typing import Dict, List, Optional
from .tracker import GasTracker
from .networks import NETWORKS, TX_TYPES


class NetworkComparator:
    """Compare gas prices across multiple networks."""

    def __init__(self, networks: Optional[List[str]] = None):
        """Initialize comparator with network list."""
        self.networks = networks or list(NETWORKS.keys())

    async def get_all_gas_data(self) -> Dict[str, dict]:
        """Fetch gas data from all networks in parallel."""
        tasks = []
        network_names = []

        for network_id in self.networks:
            if network_id not in NETWORKS:
                continue
            network = NETWORKS[network_id]
            tracker = GasTracker(network["rpc"], network["coingecko_id"])
            tasks.append(tracker.get_gas_data())
            network_names.append(network_id)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        data = {}
        for network_id, result in zip(network_names, results):
            if isinstance(result, Exception):
                data[network_id] = {"error": str(result)}
            else:
                data[network_id] = result

        return data

    def format_comparison_table(self, data: Dict[str, dict], tx_type: str = "simple") -> str:
        """Format comparison as ASCII table."""
        if tx_type not in TX_TYPES:
            tx_type = "simple"

        gas_units = TX_TYPES[tx_type]["gas"]
        tx_name = TX_TYPES[tx_type]["name"]

        # Header
        lines = []
        lines.append("=" * 100)
        lines.append(f"GAS PRICE COMPARISON - {tx_name} ({gas_units:,} gas)")
        lines.append("=" * 100)
        lines.append(f"{'Network':<20} {'Base Fee':<15} {'Priority':<15} {'Max Fee':<15} {'Cost (Native)':<15} {'Cost (USD)':<15}")
        lines.append("-" * 100)

        # Sort by USD cost (cheapest first)
        sorted_networks = []
        for network_id, network_data in data.items():
            if "error" in network_data:
                continue

            network_name = NETWORKS[network_id]["name"]
            base_fee = network_data.get("base_fee_gwei", 0)
            priority_tip = network_data.get("priority_tip_gwei", 0)
            max_fee = network_data.get("max_fee_gwei", 0)
            token_price = network_data.get("token_price_usd", 0)

            # Calculate cost
            cost_native = (max_fee * 1e-9) * gas_units
            cost_usd = cost_native * token_price if token_price else 0

            sorted_networks.append({
                "network_id": network_id,
                "name": network_name,
                "base_fee": base_fee,
                "priority_tip": priority_tip,
                "max_fee": max_fee,
                "cost_native": cost_native,
                "cost_usd": cost_usd,
            })

        sorted_networks.sort(key=lambda x: x["cost_usd"])

        # Add rows
        for idx, net in enumerate(sorted_networks):
            indicator = "🏆" if idx == 0 else f"{idx + 1}."
            symbol = NETWORKS[net["network_id"]].get("coingecko_id", "").upper()[:4]

            lines.append(
                f"{indicator} {net['name']:<17} "
                f"{net['base_fee']:>10.2f} gwei   "
                f"{net['priority_tip']:>10.2f} gwei   "
                f"{net['max_fee']:>10.2f} gwei   "
                f"{net['cost_native']:>10.6f} {symbol}   "
                f"${net['cost_usd']:>10.4f}"
            )

        # Add errors section
        errors = []
        for network_id, network_data in data.items():
            if "error" in network_data:
                network_name = NETWORKS[network_id]["name"]
                errors.append(f"  ⚠ {network_name}: {network_data['error']}")

        if errors:
            lines.append("-" * 100)
            lines.append("ERRORS:")
            lines.extend(errors)

        lines.append("=" * 100)

        return "\n".join(lines)

    def format_comparison_json(self, data: Dict[str, dict]) -> str:
        """Format comparison as JSON."""
        output = {}

        for network_id, network_data in data.items():
            network_name = NETWORKS[network_id]["name"]
            output[network_id] = {
                "network_name": network_name,
                "data": network_data
            }

        return json.dumps(output, indent=2)

    def get_cheapest_network(self, data: Dict[str, dict], tx_type: str = "simple") -> Optional[Dict]:
        """Find the cheapest network for a given transaction type."""
        if tx_type not in TX_TYPES:
            tx_type = "simple"

        gas_units = TX_TYPES[tx_type]["gas"]
        cheapest = None
        min_cost = float('inf')

        for network_id, network_data in data.items():
            if "error" in network_data:
                continue

            max_fee = network_data.get("max_fee_gwei", 0)
            token_price = network_data.get("token_price_usd", 0)

            cost_native = (max_fee * 1e-9) * gas_units
            cost_usd = cost_native * token_price if token_price else float('inf')

            if cost_usd < min_cost:
                min_cost = cost_usd
                cheapest = {
                    "network_id": network_id,
                    "network_name": NETWORKS[network_id]["name"],
                    "cost_usd": cost_usd,
                    "cost_native": cost_native,
                    "data": network_data
                }

        return cheapest


async def compare_networks(networks: Optional[List[str]] = None,
                          tx_type: str = "simple",
                          output_format: str = "table") -> str:
    """
    Compare gas prices across networks.

    Args:
        networks: List of network IDs to compare (default: all)
        tx_type: Transaction type to compare costs for
        output_format: Output format ('table' or 'json')

    Returns:
        Formatted comparison string
    """
    comparator = NetworkComparator(networks)
    data = await comparator.get_all_gas_data()

    if output_format == "json":
        return comparator.format_comparison_json(data)
    else:
        return comparator.format_comparison_table(data, tx_type)
