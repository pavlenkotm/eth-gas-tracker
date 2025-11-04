"""Statistical analysis of gas prices."""

import statistics
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

    @staticmethod
    def calculate_advanced_stats(records: List[Dict]) -> Optional[Dict]:
        """
        Calculate advanced statistics including percentiles, volatility, and standard deviation.

        Args:
            records: List of gas price records

        Returns:
            Dictionary with advanced statistics
        """
        if not records:
            return None

        base_fees = [r["base_fee"] for r in records if "base_fee" in r]
        max_fees = [r["max_fee"] for r in records if "max_fee" in r]
        priority_tips = [r.get("priority_tip", 0) for r in records]

        if not base_fees:
            return None

        # Basic stats
        basic_stats = GasStats.calculate_stats(records)

        # Advanced stats for base fee
        advanced = {
            "count": len(base_fees),
            "base_fee": {
                **basic_stats["base_fee"],
                "median": statistics.median(base_fees),
                "stdev": statistics.stdev(base_fees) if len(base_fees) > 1 else 0,
                "variance": statistics.variance(base_fees) if len(base_fees) > 1 else 0,
                "percentile_25": statistics.quantiles(base_fees, n=4)[0] if len(base_fees) >= 4 else min(base_fees),
                "percentile_50": statistics.median(base_fees),
                "percentile_75": statistics.quantiles(base_fees, n=4)[2] if len(base_fees) >= 4 else max(base_fees),
                "percentile_90": statistics.quantiles(base_fees, n=10)[8] if len(base_fees) >= 10 else max(base_fees),
                "percentile_95": statistics.quantiles(base_fees, n=20)[18] if len(base_fees) >= 20 else max(base_fees),
            }
        }

        # Calculate coefficient of variation (volatility measure)
        avg = advanced["base_fee"]["avg"]
        stdev = advanced["base_fee"]["stdev"]
        advanced["base_fee"]["coefficient_of_variation"] = (stdev / avg * 100) if avg > 0 else 0

        # Volatility classification
        cv = advanced["base_fee"]["coefficient_of_variation"]
        if cv < 10:
            volatility = "Low"
        elif cv < 25:
            volatility = "Moderate"
        elif cv < 50:
            volatility = "High"
        else:
            volatility = "Very High"

        advanced["base_fee"]["volatility"] = volatility

        # Advanced stats for max fee
        if max_fees:
            advanced["max_fee"] = {
                **basic_stats["max_fee"],
                "median": statistics.median(max_fees),
                "stdev": statistics.stdev(max_fees) if len(max_fees) > 1 else 0,
                "percentile_75": statistics.quantiles(max_fees, n=4)[2] if len(max_fees) >= 4 else max(max_fees),
                "percentile_95": statistics.quantiles(max_fees, n=20)[18] if len(max_fees) >= 20 else max(max_fees),
            }

        # Priority tip stats
        if priority_tips:
            advanced["priority_tip"] = {
                "min": min(priority_tips),
                "max": max(priority_tips),
                "avg": sum(priority_tips) / len(priority_tips),
                "median": statistics.median(priority_tips),
                "stdev": statistics.stdev(priority_tips) if len(priority_tips) > 1 else 0,
            }

        return advanced

    @staticmethod
    def calculate_volatility(records: List[Dict], window: int = 10) -> Optional[float]:
        """
        Calculate rolling volatility (coefficient of variation).

        Args:
            records: List of gas price records
            window: Rolling window size

        Returns:
            Volatility percentage
        """
        if len(records) < window:
            return None

        base_fees = [r["base_fee"] for r in records if "base_fee" in r]
        if len(base_fees) < window:
            return None

        # Use last N records
        recent = base_fees[-window:]
        avg = statistics.mean(recent)
        stdev = statistics.stdev(recent) if len(recent) > 1 else 0

        return (stdev / avg * 100) if avg > 0 else 0

    @staticmethod
    def calculate_price_ranges(records: List[Dict]) -> Optional[Dict]:
        """
        Calculate price ranges and quartiles for visualization.

        Args:
            records: List of gas price records

        Returns:
            Dictionary with price range information
        """
        if not records:
            return None

        base_fees = [r["base_fee"] for r in records if "base_fee" in r]
        if not base_fees:
            return None

        sorted_fees = sorted(base_fees)
        n = len(sorted_fees)

        if n < 4:
            return {
                "min": min(base_fees),
                "max": max(base_fees),
                "range": max(base_fees) - min(base_fees)
            }

        q1, median, q3 = statistics.quantiles(sorted_fees, n=4)
        iqr = q3 - q1

        # Calculate outlier boundaries (1.5 * IQR method)
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        outliers = [f for f in base_fees if f < lower_bound or f > upper_bound]

        return {
            "min": min(base_fees),
            "q1": q1,
            "median": median,
            "q3": q3,
            "max": max(base_fees),
            "iqr": iqr,
            "range": max(base_fees) - min(base_fees),
            "lower_outlier_bound": lower_bound,
            "upper_outlier_bound": upper_bound,
            "outlier_count": len(outliers),
            "outliers": outliers[:10]  # Limit to 10 for display
        }

    @staticmethod
    def calculate_hourly_patterns(records: List[Dict]) -> Dict[int, Dict]:
        """
        Calculate average gas prices by hour of day.

        Args:
            records: List of gas price records

        Returns:
            Dictionary mapping hour (0-23) to statistics
        """
        hourly_data = {}

        for record in records:
            try:
                timestamp = datetime.fromisoformat(record["timestamp"])
                hour = timestamp.hour
                base_fee = record.get("base_fee", 0)

                if hour not in hourly_data:
                    hourly_data[hour] = []
                hourly_data[hour].append(base_fee)
            except (KeyError, ValueError):
                continue

        # Calculate stats for each hour
        hourly_stats = {}
        for hour, fees in hourly_data.items():
            hourly_stats[hour] = {
                "avg": statistics.mean(fees),
                "min": min(fees),
                "max": max(fees),
                "median": statistics.median(fees),
                "count": len(fees)
            }

        return hourly_stats

    @staticmethod
    def format_advanced_stats(stats: Dict) -> str:
        """
        Format advanced statistics as human-readable text.

        Args:
            stats: Advanced statistics dictionary

        Returns:
            Formatted string
        """
        if not stats:
            return "No statistics available"

        lines = []
        lines.append("=" * 80)
        lines.append("ADVANCED GAS PRICE STATISTICS")
        lines.append("=" * 80)
        lines.append(f"Sample Size: {stats['count']} records")
        lines.append("")

        # Base fee stats
        bf = stats["base_fee"]
        lines.append("BASE FEE STATISTICS (gwei):")
        lines.append("-" * 80)
        lines.append(f"  Minimum:              {bf['min']:>10.2f}")
        lines.append(f"  25th Percentile:      {bf['percentile_25']:>10.2f}")
        lines.append(f"  Median (50th):        {bf['median']:>10.2f}")
        lines.append(f"  Average (Mean):       {bf['avg']:>10.2f}")
        lines.append(f"  75th Percentile:      {bf['percentile_75']:>10.2f}")
        lines.append(f"  90th Percentile:      {bf['percentile_90']:>10.2f}")
        lines.append(f"  95th Percentile:      {bf['percentile_95']:>10.2f}")
        lines.append(f"  Maximum:              {bf['max']:>10.2f}")
        lines.append("")
        lines.append(f"  Range:                {bf['max'] - bf['min']:>10.2f}")
        lines.append(f"  Standard Deviation:   {bf['stdev']:>10.2f}")
        lines.append(f"  Variance:             {bf['variance']:>10.2f}")
        lines.append(f"  Coefficient of Var:   {bf['coefficient_of_variation']:>10.2f}%")
        lines.append(f"  Volatility:           {bf['volatility']}")

        lines.append("=" * 80)

        return "\n".join(lines)
