"""ETH Gas Tracker - Multi-network gas price monitoring."""

__version__ = "1.0.0"
__author__ = "pavlenkotm"

from .tracker import GasTracker
from .networks import NETWORKS, TX_TYPES
from .history import GasHistory
from .stats import GasStats
from .graphs import ASCIIGraph
from .alerts import GasAlerts
from .api import GasAPI

__all__ = [
    "GasTracker",
    "NETWORKS",
    "TX_TYPES",
    "GasHistory",
    "GasStats",
    "ASCIIGraph",
    "GasAlerts",
    "GasAPI",
]
