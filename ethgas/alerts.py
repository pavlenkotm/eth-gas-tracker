"""Gas price alert system."""

import sys
from typing import Optional


class GasAlerts:
    """Manages gas price alerts and notifications."""

    def __init__(self, threshold: Optional[float] = None):
        self.threshold = threshold
        self.alert_triggered = False

    def check_alert(self, current_fee: float) -> Optional[str]:
        """Check if current gas fee triggers an alert."""
        if self.threshold is None:
            return None

        if current_fee <= self.threshold and not self.alert_triggered:
            self.alert_triggered = True
            return f"🔔 ALERT: Gas fee {current_fee:.2f} gwei is below threshold {self.threshold:.2f} gwei!"
        elif current_fee > self.threshold:
            self.alert_triggered = False

        return None

    @staticmethod
    def beep():
        """Make a terminal beep sound."""
        sys.stdout.write("\a")
        sys.stdout.flush()

    def notify(self, message: str, beep: bool = True) -> None:
        """Send a notification message."""
        print(f"\n{'=' * 60}")
        print(message)
        print("=" * 60 + "\n")
        if beep:
            self.beep()
