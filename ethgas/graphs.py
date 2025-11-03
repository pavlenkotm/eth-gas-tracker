"""ASCII graph generation for terminal display."""

from typing import List, Dict


class ASCIIGraph:
    """Generates ASCII graphs for gas price visualization."""

    @staticmethod
    def create_sparkline(values: List[float], width: int = 50) -> str:
        """Create a simple sparkline graph."""
        if not values:
            return ""

        # Spark characters from low to high
        sparks = "▁▂▃▄▅▆▇█"

        min_val = min(values)
        max_val = max(values)
        range_val = max_val - min_val

        if range_val == 0:
            return sparks[0] * len(values)

        # Normalize and map to spark characters
        normalized = [(v - min_val) / range_val for v in values]
        indices = [int(n * (len(sparks) - 1)) for n in normalized]

        return "".join(sparks[i] for i in indices)

    @staticmethod
    def create_bar_chart(
        records: List[Dict], max_width: int = 60, max_bars: int = 20
    ) -> str:
        """Create a horizontal bar chart of gas prices over time."""
        if not records:
            return "No data available"

        # Take most recent records
        records = records[:max_bars]
        records.reverse()  # Oldest first for chart

        # Extract base fees
        fees = [r.get("base_fee", 0) for r in records]
        timestamps = [r.get("timestamp", "")[:16] for r in records]  # YYYY-MM-DD HH:MM

        if not fees:
            return "No gas data available"

        max_fee = max(fees)
        lines = []

        lines.append("\n📊 Gas Price History (Base Fee in Gwei)\n")
        lines.append("=" * (max_width + 25))

        for i, (fee, ts) in enumerate(zip(fees, timestamps)):
            bar_width = int((fee / max_fee) * max_width) if max_fee > 0 else 0
            bar = "█" * bar_width
            lines.append(f"{ts} │ {bar} {fee:.1f}")

        lines.append("=" * (max_width + 25))

        return "\n".join(lines)

    @staticmethod
    def create_summary_display(
        current: Dict, stats: Dict, recommendation: str
    ) -> str:
        """Create a comprehensive summary display."""
        lines = []
        lines.append("\n" + "=" * 60)
        lines.append(f"🌐 Network: {current.get('network', 'Unknown')}")
        lines.append("=" * 60)
        lines.append(
            f"⛽ Base Fee:      {current['base_fee']:.2f} gwei"
        )
        lines.append(
            f"⚡ Priority Tip:  {current['priority_tip']:.2f} gwei"
        )
        lines.append(
            f"💎 Max Fee:       {current['max_fee']:.2f} gwei"
        )

        if current.get("token_price_usd"):
            lines.append(
                f"💰 Token Price:   ${current['token_price_usd']:.2f}"
            )

        if stats:
            lines.append("\n" + "-" * 60)
            lines.append("📈 Statistics (Recent History):")
            lines.append(
                f"   Min: {stats['base_fee']['min']:.2f} gwei | "
                f"Avg: {stats['base_fee']['avg']:.2f} gwei | "
                f"Max: {stats['base_fee']['max']:.2f} gwei"
            )

        lines.append("\n" + "-" * 60)
        lines.append(f"🎯 Recommendation: {recommendation}")
        lines.append("=" * 60 + "\n")

        return "\n".join(lines)
