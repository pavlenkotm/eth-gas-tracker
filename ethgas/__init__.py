"""ETH Gas Tracker - Multi-network gas price monitoring."""

__version__ = "2.0.0"
__author__ = "pavlenkotm"

from .tracker import GasTracker
from .networks import NETWORKS, TX_TYPES
from .history import GasHistory
from .stats import GasStats
from .graphs import ASCIIGraph
from .alerts import GasAlerts
from .api import GasAPI
from .compare import NetworkComparator, compare_networks
from .export import DataExporter, export_history
from .prediction import GasPredictor, predict_gas_price
from .notifications import DesktopNotifier, notify_gas_price
from .webhooks import WebhookManager, send_gas_alert_webhook
from .web_ui import WebUI, run_web_ui

__all__ = [
    "GasTracker",
    "NETWORKS",
    "TX_TYPES",
    "GasHistory",
    "GasStats",
    "ASCIIGraph",
    "GasAlerts",
    "GasAPI",
    "NetworkComparator",
    "compare_networks",
    "DataExporter",
    "export_history",
    "GasPredictor",
    "predict_gas_price",
    "DesktopNotifier",
    "notify_gas_price",
    "WebhookManager",
    "send_gas_alert_webhook",
    "WebUI",
    "run_web_ui",
]
