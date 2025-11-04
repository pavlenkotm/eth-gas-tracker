"""Desktop notification system for gas price alerts."""
import sys
import platform
from typing import Optional


class DesktopNotifier:
    """Send desktop notifications across different platforms."""

    def __init__(self):
        """Initialize notifier with platform detection."""
        self.platform = platform.system()
        self.notifier = None
        self._init_notifier()

    def _init_notifier(self):
        """Initialize appropriate notifier for the platform."""
        try:
            from plyer import notification
            self.notifier = notification
        except ImportError:
            print("⚠ Warning: plyer not installed. Desktop notifications disabled.")
            print("Install with: pip install plyer")
            self.notifier = None

    def send_notification(self,
                         title: str,
                         message: str,
                         app_name: str = "ETH Gas Tracker",
                         timeout: int = 10) -> bool:
        """
        Send a desktop notification.

        Args:
            title: Notification title
            message: Notification message
            app_name: Application name
            timeout: Duration in seconds (default: 10)

        Returns:
            True if successful, False otherwise
        """
        if not self.notifier:
            return False

        try:
            self.notifier.notify(
                title=title,
                message=message,
                app_name=app_name,
                timeout=timeout
            )
            return True
        except Exception as e:
            print(f"⚠ Notification error: {e}")
            return False

    def send_gas_alert(self,
                      network: str,
                      current_price: float,
                      threshold: float,
                      priority: str = "normal") -> bool:
        """
        Send a gas price alert notification.

        Args:
            network: Network name
            current_price: Current gas price in gwei
            threshold: Alert threshold in gwei
            priority: Alert priority ('low', 'normal', 'high')

        Returns:
            True if successful
        """
        icon_map = {
            "low": "💚",
            "normal": "💛",
            "high": "🔥"
        }
        icon = icon_map.get(priority, "⚠")

        title = f"{icon} Gas Price Alert - {network}"
        message = (
            f"Current: {current_price:.2f} gwei\n"
            f"Threshold: {threshold:.2f} gwei\n"
            f"Status: Below threshold!"
        )

        return self.send_notification(title, message)

    def send_prediction_alert(self,
                             network: str,
                             predicted_price: float,
                             confidence: float,
                             trend: str) -> bool:
        """
        Send a price prediction alert.

        Args:
            network: Network name
            predicted_price: Predicted price in gwei
            confidence: Confidence percentage
            trend: Price trend

        Returns:
            True if successful
        """
        trend_icons = {
            "increasing": "📈",
            "decreasing": "📉",
            "stable": "➡️"
        }
        icon = trend_icons.get(trend, "📊")

        title = f"{icon} Gas Price Prediction - {network}"
        message = (
            f"Predicted: {predicted_price:.2f} gwei\n"
            f"Confidence: {confidence:.1f}%\n"
            f"Trend: {trend.title()}"
        )

        return self.send_notification(title, message)

    def send_comparison_alert(self,
                             cheapest_network: str,
                             price_usd: float,
                             comparison_count: int) -> bool:
        """
        Send a network comparison alert.

        Args:
            cheapest_network: Name of cheapest network
            price_usd: Transaction cost in USD
            comparison_count: Number of networks compared

        Returns:
            True if successful
        """
        title = "🏆 Cheapest Network Found"
        message = (
            f"{cheapest_network} is the cheapest!\n"
            f"Cost: ${price_usd:.4f}\n"
            f"Compared {comparison_count} networks"
        )

        return self.send_notification(title, message)


class ConsoleNotifier:
    """Fallback console-based notifier."""

    @staticmethod
    def send_notification(title: str, message: str, **kwargs) -> bool:
        """Print notification to console."""
        print("\n" + "=" * 60)
        print(f"📢 {title}")
        print("-" * 60)
        print(message)
        print("=" * 60 + "\n")
        return True

    @staticmethod
    def send_gas_alert(network: str, current_price: float, threshold: float, priority: str = "normal") -> bool:
        """Print gas alert to console."""
        icon_map = {"low": "💚", "normal": "💛", "high": "🔥"}
        icon = icon_map.get(priority, "⚠")

        title = f"{icon} Gas Price Alert - {network}"
        message = (
            f"Current: {current_price:.2f} gwei\n"
            f"Threshold: {threshold:.2f} gwei\n"
            f"Status: Below threshold!"
        )
        return ConsoleNotifier.send_notification(title, message)


def get_notifier(use_desktop: bool = True) -> object:
    """
    Get appropriate notifier instance.

    Args:
        use_desktop: Try to use desktop notifications if True

    Returns:
        DesktopNotifier or ConsoleNotifier instance
    """
    if use_desktop:
        notifier = DesktopNotifier()
        if notifier.notifier:
            return notifier

    return ConsoleNotifier()


# Convenience functions
def notify_gas_price(network: str,
                    current_price: float,
                    threshold: float,
                    use_desktop: bool = True) -> bool:
    """
    Convenience function to send gas price notification.

    Args:
        network: Network name
        current_price: Current gas price in gwei
        threshold: Alert threshold in gwei
        use_desktop: Use desktop notifications if available

    Returns:
        True if successful
    """
    notifier = get_notifier(use_desktop)
    return notifier.send_gas_alert(network, current_price, threshold)


def notify_prediction(network: str,
                     predicted_price: float,
                     confidence: float,
                     trend: str,
                     use_desktop: bool = True) -> bool:
    """
    Convenience function to send prediction notification.

    Args:
        network: Network name
        predicted_price: Predicted price in gwei
        confidence: Confidence percentage
        trend: Price trend
        use_desktop: Use desktop notifications if available

    Returns:
        True if successful
    """
    notifier = get_notifier(use_desktop)
    if hasattr(notifier, 'send_prediction_alert'):
        return notifier.send_prediction_alert(network, predicted_price, confidence, trend)
    else:
        message = f"Predicted: {predicted_price:.2f} gwei\nConfidence: {confidence:.1f}%\nTrend: {trend}"
        return notifier.send_notification(f"Prediction - {network}", message)
