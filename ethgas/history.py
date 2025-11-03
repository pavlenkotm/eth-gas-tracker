"""Historical gas price tracking and storage."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional


class GasHistory:
    """Manages historical gas price data."""

    def __init__(self, data_dir: str = ".ethgas"):
        self.data_dir = Path.home() / data_dir
        self.data_dir.mkdir(exist_ok=True)
        self.history_file = self.data_dir / "history.jsonl"

    def add_record(self, gas_data: Dict) -> None:
        """Add a gas price record to history."""
        record = {
            "timestamp": datetime.now().isoformat(),
            **gas_data,
        }

        with open(self.history_file, "a") as f:
            f.write(json.dumps(record) + "\n")

    def get_records(
        self, network: Optional[str] = None, limit: Optional[int] = None
    ) -> List[Dict]:
        """Get historical records, optionally filtered by network."""
        if not self.history_file.exists():
            return []

        records = []
        with open(self.history_file, "r") as f:
            for line in f:
                if line.strip():
                    record = json.loads(line)
                    if network is None or record.get("network") == network:
                        records.append(record)

        # Return most recent first
        records.reverse()

        if limit:
            return records[:limit]
        return records

    def clear_history(self) -> None:
        """Clear all historical data."""
        if self.history_file.exists():
            self.history_file.unlink()
