"""ETH Gas Tracker - Main CLI application."""

import argparse
import asyncio
import aiohttp
import json
import sys
from datetime import datetime

from .networks import NETWORKS, TX_TYPES
from .tracker import GasTracker
from .history import GasHistory
from .stats import GasStats
from .graphs import ASCIIGraph
from .alerts import GasAlerts
from .api import GasAPI
from .compare import compare_networks
from .export import export_history
from .prediction import predict_gas_price, GasPredictor
from .notifications import get_notifier
from .webhooks import create_webhook_manager
from .web_ui import run_web_ui


async def track_once(
    tracker: GasTracker,
    session: aiohttp.ClientSession,
    args,
    history: GasHistory = None,
) -> dict:
    """Perform a single gas price check."""
    gas_data = await tracker.get_gas_data(session, args.priority)

    # Save to history if enabled
    if args.history and history:
        history.add_record(gas_data)

    # JSON output mode
    if args.json:
        output = {"timestamp": datetime.now().isoformat(), **gas_data}

        # Add tx costs if requested
        if args.show_costs:
            tx_costs = {}
            for tx_type, tx_info in TX_TYPES.items():
                cost = tracker.calculate_tx_cost(
                    gas_data["max_fee"], tx_info["gas"], gas_data["token_price_usd"]
                )
                tx_costs[tx_type] = {
                    "name": tx_info["name"],
                    "gas_units": tx_info["gas"],
                    "cost_native": cost["cost_native"],
                    "cost_usd": cost["cost_usd"],
                }
            output["tx_costs"] = tx_costs

        print(json.dumps(output, indent=2))
        return gas_data

    # Human-readable output
    if args.detailed:
        # Show detailed view with stats and graphs
        stats = None
        recommendation = "No historical data"

        if history:
            records = history.get_records(network=gas_data["network"], limit=100)
            if records:
                recent_records = GasStats.filter_by_timeframe(records, args.stats_hours)
                stats = GasStats.calculate_stats(recent_records)
                recommendation = GasStats.recommend_action(
                    gas_data["base_fee"], stats
                )

                # Show graph
                if args.graph:
                    print(ASCIIGraph.create_bar_chart(records, max_bars=15))

        # Show summary
        print(ASCIIGraph.create_summary_display(gas_data, stats, recommendation))

        # Show tx costs
        if args.show_costs:
            print("💸 Transaction Cost Estimates:")
            print("-" * 60)
            for tx_type, tx_info in TX_TYPES.items():
                cost = tracker.calculate_tx_cost(
                    gas_data["max_fee"], tx_info["gas"], gas_data["token_price_usd"]
                )
                usd_str = (
                    f"${cost['cost_usd']:.2f}" if cost["cost_usd"] else "N/A"
                )
                print(
                    f"  {tx_info['name']:20} ({tx_info['gas']:>6} gas): {usd_str:>10}"
                )
            print("-" * 60 + "\n")

    else:
        # Simple one-line output
        line = f"[{gas_data['network']}] Base: {gas_data['base_fee']:.1f} gwei | "
        line += f"Priority: {gas_data['priority_tip']:.1f} | "
        line += f"Max: {gas_data['max_fee']:.1f}"

        if args.show_usd and gas_data["token_price_usd"]:
            # Show simple transfer cost
            cost = tracker.calculate_tx_cost(
                gas_data["max_fee"], 21000, gas_data["token_price_usd"]
            )
            line += f" | Tx ≈ ${cost['cost_usd']:.2f}"

        print(line)

    return gas_data


async def watch_mode(
    tracker: GasTracker, args, history: GasHistory = None, alerts: GasAlerts = None,
    notifier=None, webhook_manager=None
):
    """Continuous monitoring mode."""
    print(f"👀 Watching {tracker.network_name} gas prices (Ctrl+C to stop)")
    print(f"⏱️  Update interval: {args.watch} seconds\n")

    if alerts and alerts.threshold:
        print(f"🔔 Alert threshold: {alerts.threshold} gwei\n")

    if notifier:
        print(f"🔔 Desktop notifications enabled\n")

    if webhook_manager and webhook_manager.webhook_urls:
        print(f"🔗 Webhooks configured: {len(webhook_manager.webhook_urls)}\n")

    iteration = 0

    try:
        async with aiohttp.ClientSession() as session:
            while True:
                try:
                    # Clear screen for detailed mode
                    if args.detailed and iteration > 0:
                        print("\033[2J\033[H", end="")  # Clear screen and move cursor

                    gas_data = await track_once(tracker, session, args, history)

                    # Check alerts
                    if alerts:
                        alert_msg = alerts.check_alert(gas_data["base_fee"])
                        if alert_msg:
                            alerts.notify(alert_msg, beep=args.beep)

                            # Send desktop notification
                            if notifier:
                                notifier.send_gas_alert(
                                    tracker.network_name,
                                    gas_data["base_fee"],
                                    alerts.threshold
                                )

                            # Send webhook alerts
                            if webhook_manager:
                                await webhook_manager.send_gas_alert(
                                    tracker.network_name,
                                    gas_data["base_fee"],
                                    alerts.threshold,
                                    gas_data.get("token_price_usd")
                                )

                    iteration += 1
                    await asyncio.sleep(args.watch)

                except KeyboardInterrupt:
                    raise
                except Exception as e:
                    print(f"❌ Error: {e}", file=sys.stderr)
                    await asyncio.sleep(args.watch)

    except KeyboardInterrupt:
        print("\n\n👋 Stopped watching")


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="ETH Gas Tracker - Multi-network gas price monitoring",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python -m ethgas.main

  # Watch Ethereum gas prices with alerts
  python -m ethgas.main --watch 10 --alert 30

  # Detailed view with graph and costs
  python -m ethgas.main --detailed --graph --show-costs

  # Monitor Polygon network
  python -m ethgas.main --network polygon --watch 15

  # JSON output for scripting
  python -m ethgas.main --json --show-costs

  # Start API server
  python -m ethgas.main --api --port 8080
        """,
    )

    # Network options
    parser.add_argument(
        "--network",
        default="ethereum",
        choices=list(NETWORKS.keys()),
        help="Network to monitor (default: ethereum)",
    )
    parser.add_argument(
        "--rpc", help="Custom RPC URL (overrides network default)"
    )

    # Gas parameters
    parser.add_argument(
        "--priority",
        type=float,
        default=1.5,
        help="Priority tip in gwei (default: 1.5)",
    )

    # Display options
    parser.add_argument(
        "--show-usd",
        action="store_true",
        help="Show simple transfer cost in USD",
    )
    parser.add_argument(
        "--show-costs",
        action="store_true",
        help="Show costs for different transaction types",
    )
    parser.add_argument(
        "--detailed",
        action="store_true",
        help="Show detailed view with stats and recommendations",
    )
    parser.add_argument(
        "--graph",
        action="store_true",
        help="Show ASCII graph (requires --detailed)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format",
    )

    # Watch mode
    parser.add_argument(
        "--watch",
        type=int,
        metavar="SECONDS",
        help="Watch mode: update every N seconds",
    )

    # Alerts
    parser.add_argument(
        "--alert",
        type=float,
        metavar="GWEI",
        help="Alert when base fee drops below threshold (gwei)",
    )
    parser.add_argument(
        "--beep",
        action="store_true",
        help="Make beep sound on alert",
    )

    # History and stats
    parser.add_argument(
        "--history",
        action="store_true",
        help="Save gas prices to history",
    )
    parser.add_argument(
        "--stats-hours",
        type=int,
        default=24,
        help="Hours of history for statistics (default: 24)",
    )

    # API mode
    parser.add_argument(
        "--api",
        action="store_true",
        help="Start REST API server",
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="API server host (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="API server port (default: 8080)",
    )

    # NEW FEATURES
    # Comparison mode
    parser.add_argument(
        "--compare",
        action="store_true",
        help="Compare gas prices across all networks",
    )
    parser.add_argument(
        "--compare-tx-type",
        default="simple",
        choices=list(TX_TYPES.keys()),
        help="Transaction type for comparison (default: simple)",
    )

    # Export functionality
    parser.add_argument(
        "--export",
        choices=["csv", "excel", "json"],
        help="Export historical data to file",
    )
    parser.add_argument(
        "--export-path",
        help="Custom path for export file",
    )
    parser.add_argument(
        "--export-limit",
        type=int,
        help="Limit number of records to export",
    )

    # Prediction
    parser.add_argument(
        "--predict",
        action="store_true",
        help="Predict future gas prices",
    )
    parser.add_argument(
        "--predict-method",
        default="moving_average",
        choices=["moving_average", "exponential", "linear"],
        help="Prediction method (default: moving_average)",
    )

    # Notifications
    parser.add_argument(
        "--desktop-notify",
        action="store_true",
        help="Enable desktop notifications for alerts",
    )

    # Webhooks
    parser.add_argument(
        "--webhook",
        action="append",
        help="Webhook URL for alerts (can be used multiple times)",
    )
    parser.add_argument(
        "--webhook-file",
        help="File containing webhook URLs (one per line)",
    )

    # Advanced statistics
    parser.add_argument(
        "--advanced-stats",
        action="store_true",
        help="Show advanced statistics (percentiles, volatility, etc.)",
    )

    # Web UI
    parser.add_argument(
        "--web-ui",
        action="store_true",
        help="Start web-based user interface",
    )

    args = parser.parse_args()

    # Web UI mode
    if args.web_ui:
        run_web_ui(host=args.host, port=args.port)
        return

    # API mode
    if args.api:
        api = GasAPI(host=args.host, port=args.port)
        api.run()
        return

    # Comparison mode
    if args.compare:
        result = await compare_networks(
            tx_type=args.compare_tx_type,
            output_format="json" if args.json else "table"
        )
        print(result)
        return

    # Export mode
    if args.export:
        history = GasHistory()
        network_name = NETWORKS[args.network]["name"] if args.network != "ethereum" else None
        try:
            output_path = export_history(
                history,
                format=args.export,
                output_path=args.export_path,
                network=network_name,
                limit=args.export_limit
            )
            print(f"✅ Data exported to: {output_path}")
        except Exception as e:
            print(f"❌ Export failed: {e}", file=sys.stderr)
            sys.exit(1)
        return

    # Prediction mode
    if args.predict:
        history = GasHistory()
        network_name = NETWORKS[args.network]["name"]
        prediction = predict_gas_price(
            history,
            network=network_name,
            method=args.predict_method
        )

        if args.json:
            print(json.dumps(prediction, indent=2))
        else:
            if "error" in prediction:
                print(f"❌ {prediction['error']}")
            else:
                predictor = GasPredictor(history.get_records(network=network_name, limit=100))
                print(predictor.format_prediction(prediction))
        return

    # Get network config
    network = NETWORKS[args.network]
    rpc_url = args.rpc or network["rpc"]

    # Initialize components
    tracker = GasTracker(rpc_url, network["coingecko_id"], network["name"])
    history = GasHistory() if (args.history or args.detailed or args.advanced_stats) else None
    alerts = GasAlerts(threshold=args.alert) if args.alert else None

    # Initialize notifier
    notifier = None
    if args.desktop_notify:
        notifier = get_notifier(use_desktop=True)

    # Initialize webhook manager
    webhook_manager = None
    if args.webhook or args.webhook_file:
        webhook_manager = create_webhook_manager(
            webhook_urls=args.webhook,
            webhook_file=args.webhook_file
        )

    # Show advanced statistics
    if args.advanced_stats:
        network_name = NETWORKS[args.network]["name"]
        records = history.get_records(network=network_name)
        if records:
            filtered = GasStats.filter_by_timeframe(records, args.stats_hours)
            if filtered:
                advanced_stats = GasStats.calculate_advanced_stats(filtered)
                if advanced_stats:
                    print(GasStats.format_advanced_stats(advanced_stats))
                else:
                    print("❌ Not enough data for advanced statistics")
            else:
                print(f"❌ No data found for the last {args.stats_hours} hours")
        else:
            print("❌ No historical data available")
        return

    # Watch mode
    if args.watch:
        await watch_mode(tracker, args, history, alerts, notifier, webhook_manager)
    else:
        # Single check
        async with aiohttp.ClientSession() as session:
            await track_once(tracker, session, args, history)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)
