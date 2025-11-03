"""Statistical analysis of gas prices."""

from typing import List, Dict, Optional
from datetime import datetime, timedelta


class GasStats:
    """Calculates statistics from historical gas data."""

    @staticmethod
    def calculate_stats(records: List[Dict]) -> Optional[Dict]:
        """Calculate min, max, average gas prices from records."""
        if not records:
            return None

        base_fees = [r["base_fee"] for r in records if "base_fee" in r]
        max_fees = [r["max_fee"] for r in records if "max_fee" in r]

        if not base_fees:
            return None

        return {
            "count": len(base_fees),
            "base_fee": {
                "min": min(base_fees),
                "max": max(base_fees),
                "avg": sum(base_fees) / len(base_fees),
            },
            "max_fee": {
                "min": min(max_fees) if max_fees else None,
                "max": max(max_fees) if max_fees else None,
                "avg": sum(max_fees) / len(max_fees) if max_fees else None,
            },
        }

    @staticmethod
    def filter_by_timeframe(records: List[Dict], hours: int) -> List[Dict]:
        """Filter records to only include those from the last N hours."""
        cutoff = datetime.now() - timedelta(hours=hours)
        filtered = []

        for record in records:
            try:
                timestamp = datetime.fromisoformat(record["timestamp"])
                if timestamp >= cutoff:
                    filtered.append(record)
            except (KeyError, ValueError):
                continue

        return filtered

    @staticmethod
    def recommend_action(current_base_fee: float, stats: Dict) -> str:
        """Recommend whether to send transaction now based on stats."""
        if not stats or "base_fee" not in stats:
            return "Insufficient data for recommendation"

        avg = stats["base_fee"]["avg"]
        min_fee = stats["base_fee"]["min"]

        if current_base_fee <= min_fee * 1.1:  # Within 10% of minimum
            return "⭐ EXCELLENT - Near historical minimum!"
        elif current_base_fee <= avg * 0.8:  # 20% below average
            return "✅ GOOD - Below average, good time to transact"
        elif current_base_fee <= avg * 1.2:  # Within 20% of average
            return "🟡 MODERATE - Around average, consider waiting"
        else:
            return "🔴 HIGH - Above average, consider waiting"
