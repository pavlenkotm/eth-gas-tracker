"""Webhook alert system for external integrations."""
import json
import asyncio
from typing import Dict, List, Optional
from datetime import datetime
import aiohttp


class WebhookManager:
    """Manage webhook notifications for various platforms."""

    def __init__(self, webhook_urls: Optional[List[str]] = None):
        """
        Initialize webhook manager.

        Args:
            webhook_urls: List of webhook URLs to send alerts to
        """
        self.webhook_urls = webhook_urls or []

    async def send_webhook(self,
                          url: str,
                          payload: Dict,
                          headers: Optional[Dict] = None) -> bool:
        """
        Send webhook POST request.

        Args:
            url: Webhook URL
            payload: JSON payload to send
            headers: Optional custom headers

        Returns:
            True if successful, False otherwise
        """
        if not headers:
            headers = {"Content-Type": "application/json"}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, headers=headers, timeout=10) as response:
                    if response.status in [200, 201, 202, 204]:
                        return True
                    else:
                        print(f"⚠ Webhook failed with status {response.status}: {url}")
                        return False
        except asyncio.TimeoutError:
            print(f"⚠ Webhook timeout: {url}")
            return False
        except Exception as e:
            print(f"⚠ Webhook error: {e}")
            return False

    async def send_to_all(self, payload: Dict, platform: str = "generic") -> Dict[str, bool]:
        """
        Send webhook to all configured URLs.

        Args:
            payload: Payload to send
            platform: Platform type for formatting

        Returns:
            Dictionary mapping URL to success status
        """
        if not self.webhook_urls:
            return {}

        tasks = []
        for url in self.webhook_urls:
            formatted_payload = self._format_payload(payload, platform, url)
            tasks.append(self.send_webhook(url, formatted_payload))

        results = await asyncio.gather(*tasks, return_exceptions=True)

        return {
            url: result if not isinstance(result, Exception) else False
            for url, result in zip(self.webhook_urls, results)
        }

    def _format_payload(self, payload: Dict, platform: str, url: str) -> Dict:
        """Format payload for specific platform."""
        # Auto-detect platform from URL
        if "slack.com" in url:
            return self._format_slack(payload)
        elif "discord.com" in url or "discordapp.com" in url:
            return self._format_discord(payload)
        elif "webhook.office.com" in url:
            return self._format_teams(payload)
        else:
            return payload

    def _format_slack(self, payload: Dict) -> Dict:
        """Format payload for Slack webhooks."""
        title = payload.get("title", "Gas Price Alert")
        message = payload.get("message", "")
        fields = payload.get("fields", {})

        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": title
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message
                }
            }
        ]

        # Add fields as context
        if fields:
            field_texts = [f"*{k}:* {v}" for k, v in fields.items()]
            blocks.append({
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": text}
                    for text in field_texts
                ]
            })

        return {"blocks": blocks}

    def _format_discord(self, payload: Dict) -> Dict:
        """Format payload for Discord webhooks."""
        title = payload.get("title", "Gas Price Alert")
        message = payload.get("message", "")
        fields = payload.get("fields", {})
        color = payload.get("color", 3447003)  # Blue by default

        embed = {
            "title": title,
            "description": message,
            "color": color,
            "timestamp": datetime.utcnow().isoformat(),
            "fields": [
                {"name": k, "value": str(v), "inline": True}
                for k, v in fields.items()
            ]
        }

        return {"embeds": [embed]}

    def _format_teams(self, payload: Dict) -> Dict:
        """Format payload for Microsoft Teams webhooks."""
        title = payload.get("title", "Gas Price Alert")
        message = payload.get("message", "")
        fields = payload.get("fields", {})

        facts = [{"name": k, "value": str(v)} for k, v in fields.items()]

        return {
            "@type": "MessageCard",
            "@context": "https://schema.org/extensions",
            "summary": title,
            "title": title,
            "text": message,
            "sections": [{"facts": facts}] if facts else []
        }

    async def send_gas_alert(self,
                            network: str,
                            current_price: float,
                            threshold: float,
                            token_price: Optional[float] = None) -> Dict[str, bool]:
        """
        Send gas price alert webhook.

        Args:
            network: Network name
            current_price: Current gas price in gwei
            threshold: Alert threshold in gwei
            token_price: Token price in USD (optional)

        Returns:
            Dictionary of webhook results
        """
        fields = {
            "Network": network,
            "Current Price": f"{current_price:.2f} gwei",
            "Threshold": f"{threshold:.2f} gwei",
            "Status": "✅ Below threshold"
        }

        if token_price:
            fields["Token Price"] = f"${token_price:.2f}"

        payload = {
            "title": f"💰 Gas Price Alert - {network}",
            "message": f"Gas price has dropped below your threshold!",
            "fields": fields,
            "color": 3066993  # Green
        }

        return await self.send_to_all(payload)

    async def send_prediction_alert(self,
                                   network: str,
                                   predicted_price: float,
                                   confidence: float,
                                   trend: str) -> Dict[str, bool]:
        """
        Send prediction alert webhook.

        Args:
            network: Network name
            predicted_price: Predicted gas price in gwei
            confidence: Prediction confidence percentage
            trend: Price trend

        Returns:
            Dictionary of webhook results
        """
        trend_emoji = {
            "increasing": "📈",
            "decreasing": "📉",
            "stable": "➡️"
        }.get(trend, "📊")

        payload = {
            "title": f"{trend_emoji} Gas Price Prediction - {network}",
            "message": f"Next hour prediction with {confidence:.1f}% confidence",
            "fields": {
                "Network": network,
                "Predicted Price": f"{predicted_price:.2f} gwei",
                "Confidence": f"{confidence:.1f}%",
                "Trend": trend.title()
            },
            "color": 15844367  # Gold
        }

        return await self.send_to_all(payload)

    async def send_comparison_alert(self,
                                   cheapest_network: str,
                                   price_usd: float,
                                   all_networks: Dict[str, float]) -> Dict[str, bool]:
        """
        Send network comparison alert.

        Args:
            cheapest_network: Name of cheapest network
            price_usd: Transaction cost in USD
            all_networks: Dictionary of network names to USD costs

        Returns:
            Dictionary of webhook results
        """
        # Sort networks by price
        sorted_networks = sorted(all_networks.items(), key=lambda x: x[1])
        top_3 = sorted_networks[:3]

        fields = {
            "Cheapest Network": cheapest_network,
            "Cost": f"${price_usd:.4f}",
        }

        # Add top 3
        for idx, (net, cost) in enumerate(top_3, 1):
            fields[f"#{idx}"] = f"{net}: ${cost:.4f}"

        payload = {
            "title": "🏆 Network Comparison Complete",
            "message": f"{cheapest_network} is the cheapest option!",
            "fields": fields,
            "color": 3447003  # Blue
        }

        return await self.send_to_all(payload)

    async def send_custom(self,
                         title: str,
                         message: str,
                         fields: Optional[Dict] = None,
                         color: Optional[int] = None) -> Dict[str, bool]:
        """
        Send custom webhook.

        Args:
            title: Alert title
            message: Alert message
            fields: Optional fields dictionary
            color: Optional color code

        Returns:
            Dictionary of webhook results
        """
        payload = {
            "title": title,
            "message": message,
            "fields": fields or {},
            "color": color or 3447003
        }

        return await self.send_to_all(payload)


def create_webhook_manager(webhook_urls: Optional[List[str]] = None,
                          webhook_file: Optional[str] = None) -> WebhookManager:
    """
    Create webhook manager from URLs or file.

    Args:
        webhook_urls: List of webhook URLs
        webhook_file: Path to file containing webhook URLs (one per line)

    Returns:
        WebhookManager instance
    """
    urls = webhook_urls or []

    if webhook_file:
        try:
            with open(webhook_file, 'r') as f:
                file_urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                urls.extend(file_urls)
        except FileNotFoundError:
            print(f"⚠ Webhook file not found: {webhook_file}")
        except Exception as e:
            print(f"⚠ Error reading webhook file: {e}")

    return WebhookManager(urls)


# Convenience functions
async def send_gas_alert_webhook(webhook_urls: List[str],
                                 network: str,
                                 current_price: float,
                                 threshold: float,
                                 token_price: Optional[float] = None) -> Dict[str, bool]:
    """Convenience function to send gas alert."""
    manager = WebhookManager(webhook_urls)
    return await manager.send_gas_alert(network, current_price, threshold, token_price)
