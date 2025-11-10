"""Gas price prediction based on historical data."""
import statistics
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dateutil import parser as date_parser


class GasPredictor:
    """Predict future gas prices using historical data."""

    def __init__(self, historical_records: List[Dict]):
        """Initialize predictor with historical data."""
        self.records = historical_records
        self._prepare_data()

    def _prepare_data(self):
        """Prepare and sort data by timestamp."""
        # Parse timestamps and sort
        for record in self.records:
            if isinstance(record.get("timestamp"), str):
                record["timestamp_parsed"] = date_parser.parse(record["timestamp"])
            elif isinstance(record.get("timestamp"), datetime):
                record["timestamp_parsed"] = record["timestamp"]

        self.records.sort(key=lambda x: x.get("timestamp_parsed", datetime.min))

    def get_trend(self, hours: int = 24) -> str:
        """
        Determine price trend over specified timeframe.

        Args:
            hours: Lookback period in hours

        Returns:
            Trend description: 'increasing', 'decreasing', or 'stable'
        """
        if len(self.records) < 2:
            return "insufficient_data"

        cutoff = datetime.now() - timedelta(hours=hours)
        recent_records = [
            r for r in self.records
            if r.get("timestamp_parsed", datetime.min) >= cutoff
        ]

        if len(recent_records) < 2:
            return "insufficient_data"

        # Get prices from first and second half
        mid_point = len(recent_records) // 2
        first_half = recent_records[:mid_point]
        second_half = recent_records[mid_point:]

        first_avg = statistics.mean(r.get("base_fee", 0) for r in first_half)
        second_avg = statistics.mean(r.get("base_fee", 0) for r in second_half)

        # Calculate percentage change
        if first_avg == 0:
            return "stable"

        change_pct = ((second_avg - first_avg) / first_avg) * 100

        if change_pct > 10:
            return "increasing"
        elif change_pct < -10:
            return "decreasing"
        else:
            return "stable"

    def predict_next_hour(self, method: str = "moving_average") -> Dict:
        """
        Predict gas price for next hour.

        Args:
            method: Prediction method ('moving_average', 'exponential', or 'linear')

        Returns:
            Dictionary with predicted values
        """
        if len(self.records) < 3:
            return {
                "error": "Insufficient data for prediction (need at least 3 records)",
                "confidence": 0
            }

        if method == "moving_average":
            return self._predict_moving_average()
        elif method == "exponential":
            return self._predict_exponential()
        elif method == "linear":
            return self._predict_linear()
        else:
            return {"error": f"Unknown prediction method: {method}"}

    def _predict_moving_average(self, window: int = 10) -> Dict:
        """Simple moving average prediction."""
        recent = self.records[-window:]
        base_fees = [r.get("base_fee", 0) for r in recent]
        priority_tips = [r.get("priority_tip", 0) for r in recent]

        predicted_base = statistics.mean(base_fees)
        predicted_priority = statistics.mean(priority_tips)
        predicted_max = predicted_base + predicted_priority

        # Calculate confidence based on volatility
        stdev = statistics.stdev(base_fees) if len(base_fees) > 1 else 0
        avg = statistics.mean(base_fees)
        volatility = (stdev / avg * 100) if avg > 0 else 100

        # Lower volatility = higher confidence
        confidence = max(0, min(100, 100 - volatility))

        return {
            "method": "moving_average",
            "predicted_base_fee": round(predicted_base, 2),
            "predicted_priority_tip": round(predicted_priority, 2),
            "predicted_max_fee": round(predicted_max, 2),
            "confidence": round(confidence, 1),
            "trend": self.get_trend(),
            "sample_size": len(recent)
        }

    def _predict_exponential(self, alpha: float = 0.3) -> Dict:
        """Exponential weighted moving average (gives more weight to recent data)."""
        if len(self.records) < 2:
            return {"error": "Insufficient data"}

        base_fees = [r.get("base_fee", 0) for r in self.records]
        priority_tips = [r.get("priority_tip", 0) for r in self.records]

        # Calculate EMA
        ema_base = base_fees[0]
        for fee in base_fees[1:]:
            ema_base = alpha * fee + (1 - alpha) * ema_base

        ema_priority = priority_tips[0]
        for tip in priority_tips[1:]:
            ema_priority = alpha * tip + (1 - alpha) * ema_priority

        predicted_max = ema_base + ema_priority

        # Calculate confidence
        recent_base = base_fees[-10:]
        stdev = statistics.stdev(recent_base) if len(recent_base) > 1 else 0
        avg = statistics.mean(recent_base)
        volatility = (stdev / avg * 100) if avg > 0 else 100
        confidence = max(0, min(100, 100 - volatility))

        return {
            "method": "exponential_moving_average",
            "predicted_base_fee": round(ema_base, 2),
            "predicted_priority_tip": round(ema_priority, 2),
            "predicted_max_fee": round(predicted_max, 2),
            "confidence": round(confidence, 1),
            "trend": self.get_trend(),
            "alpha": alpha
        }

    def _predict_linear(self) -> Dict:
        """Simple linear regression prediction."""
        if len(self.records) < 5:
            return {"error": "Insufficient data for linear regression"}

        # Use last 20 records for trend
        recent = self.records[-20:]
        n = len(recent)

        # Simple linear regression: y = mx + b
        base_fees = [r.get("base_fee", 0) for r in recent]
        x = list(range(n))

        # Calculate slope and intercept
        x_mean = statistics.mean(x)
        y_mean = statistics.mean(base_fees)

        numerator = sum((x[i] - x_mean) * (base_fees[i] - y_mean) for i in range(n))
        denominator = sum((x[i] - x_mean) ** 2 for i in range(n))

        if denominator == 0:
            return {"error": "Cannot calculate linear trend"}

        slope = numerator / denominator
        intercept = y_mean - slope * x_mean

        # Predict next value
        next_x = n
        predicted_base = slope * next_x + intercept
        predicted_base = max(0, predicted_base)  # Can't be negative

        # Priority tip prediction (use simple average)
        priority_tips = [r.get("priority_tip", 0) for r in recent]
        predicted_priority = statistics.mean(priority_tips)
        predicted_max = predicted_base + predicted_priority

        # Calculate R-squared for confidence
        y_pred = [slope * xi + intercept for xi in x]
        ss_res = sum((base_fees[i] - y_pred[i]) ** 2 for i in range(n))
        ss_tot = sum((base_fees[i] - y_mean) ** 2 for i in range(n))
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
        confidence = max(0, min(100, r_squared * 100))

        return {
            "method": "linear_regression",
            "predicted_base_fee": round(predicted_base, 2),
            "predicted_priority_tip": round(predicted_priority, 2),
            "predicted_max_fee": round(predicted_max, 2),
            "confidence": round(confidence, 1),
            "trend": self.get_trend(),
            "slope": round(slope, 4),
            "r_squared": round(r_squared, 4)
        }

    def get_optimal_time_window(self, hours_ahead: int = 24) -> Optional[Dict]:
        """
        Predict the best time window to make a transaction.

        Args:
            hours_ahead: How many hours ahead to analyze

        Returns:
            Dictionary with optimal time prediction
        """
        if len(self.records) < hours_ahead:
            return None

        # Analyze hourly patterns from historical data
        hourly_avg = {}
        for record in self.records:
            dt = record.get("timestamp_parsed")
            if not dt:
                continue

            hour = dt.hour
            base_fee = record.get("base_fee", 0)

            if hour not in hourly_avg:
                hourly_avg[hour] = []
            hourly_avg[hour].append(base_fee)

        # Calculate average for each hour
        hourly_stats = {}
        for hour, fees in hourly_avg.items():
            hourly_stats[hour] = {
                "avg": statistics.mean(fees),
                "min": min(fees),
                "max": max(fees)
            }

        # Find cheapest hour
        if not hourly_stats:
            return None

        cheapest_hour = min(hourly_stats.keys(), key=lambda h: hourly_stats[h]["avg"])
        most_expensive_hour = max(hourly_stats.keys(), key=lambda h: hourly_stats[h]["avg"])

        current_hour = datetime.now().hour
        hours_until_cheapest = (cheapest_hour - current_hour) % 24

        return {
            "cheapest_hour": cheapest_hour,
            "cheapest_hour_avg_gwei": round(hourly_stats[cheapest_hour]["avg"], 2),
            "most_expensive_hour": most_expensive_hour,
            "most_expensive_hour_avg_gwei": round(hourly_stats[most_expensive_hour]["avg"], 2),
            "current_hour": current_hour,
            "hours_until_cheapest": hours_until_cheapest,
            "recommendation": f"Wait {hours_until_cheapest} hours" if hours_until_cheapest > 0 else "Now is a good time"
        }

    def format_prediction(self, prediction: Dict) -> str:
        """Format prediction as human-readable text."""
        if "error" in prediction:
            return f"❌ Prediction Error: {prediction['error']}"

        lines = []
        lines.append("=" * 60)
        lines.append(f"GAS PRICE PREDICTION ({prediction.get('method', 'unknown').replace('_', ' ').title()})")
        lines.append("=" * 60)
        lines.append(f"Predicted Base Fee:      {prediction['predicted_base_fee']:>8.2f} gwei")
        lines.append(f"Predicted Priority Tip:  {prediction['predicted_priority_tip']:>8.2f} gwei")
        lines.append(f"Predicted Max Fee:       {prediction['predicted_max_fee']:>8.2f} gwei")
        lines.append("-" * 60)
        lines.append(f"Confidence:              {prediction['confidence']:>8.1f}%")
        lines.append(f"Trend:                   {prediction['trend'].upper()}")

        if "sample_size" in prediction:
            lines.append(f"Sample Size:             {prediction['sample_size']:>8}")

        lines.append("=" * 60)

        return "\n".join(lines)


def predict_gas_price(history_manager,
                     network: Optional[str] = None,
                     method: str = "moving_average") -> Dict:
    """
    Convenience function for gas price prediction.

    Args:
        history_manager: GasHistory instance
        network: Filter by network (optional)
        method: Prediction method

    Returns:
        Prediction dictionary
    """
    records = history_manager.get_records(network=network, limit=100)

    if not records:
        return {"error": "No historical data available"}

    predictor = GasPredictor(records)
    return predictor.predict_next_hour(method=method)
