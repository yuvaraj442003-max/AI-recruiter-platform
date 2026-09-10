"""
communication_provider.py — Abstract Communication Interface & Providers.
Provides decoupled messaging abstraction for WhatsApp, SMS, and Voice channels.
Includes TwilioProvider for production and MockCommunicationProvider for development/testing.
"""
import abc
import hmac
import hashlib
import logging
import uuid
from typing import Dict, Any, Optional

import httpx

from app.core.config import settings

logger = logging.getLogger("ai_recruiter.communication")


class BaseCommunicationProvider(abc.ABC):
    """Abstract Base Class for multi-channel communication providers."""

    @abc.abstractmethod
    def send_message(
        self,
        to_number: str,
        message: str,
        channel: str = "whatsapp",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Sends an outbound message to a candidate. Returns message execution details."""
        pass

    @abc.abstractmethod
    def validate_webhook_signature(
        self, url: str, params: Dict[str, Any], signature: str
    ) -> bool:
        """Validates incoming webhook request signature from provider."""
        pass


class TwilioProvider(BaseCommunicationProvider):
    """Twilio Provider supporting WhatsApp, SMS, and Voice interactions."""

    def __init__(self):
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.whatsapp_from = settings.TWILIO_WHATSAPP_NUMBER or "whatsapp:+14155238886"
        self.sms_from = settings.TWILIO_SMS_NUMBER or ""
        self.voice_from = settings.TWILIO_VOICE_NUMBER or ""

    def send_message(
        self,
        to_number: str,
        message: str,
        channel: str = "whatsapp",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        if not self.account_sid or not self.auth_token:
            logger.warning("Twilio credentials missing. Falling back to internal mock dispatch.")
            return MockCommunicationProvider().send_message(to_number, message, channel, metadata)

        url = f"https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}/Messages.json"
        
        # Format destination phone number for Twilio
        formatted_to = to_number
        if channel == "whatsapp":
            if not formatted_to.startswith("whatsapp:"):
                formatted_to = f"whatsapp:{formatted_to}"
            from_number = self.whatsapp_from if self.whatsapp_from.startswith("whatsapp:") else f"whatsapp:{self.whatsapp_from}"
        else:
            from_number = self.sms_from or self.whatsapp_from.replace("whatsapp:", "")

        data = {
            "From": from_number,
            "To": formatted_to,
            "Body": message,
        }

        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.post(
                    url,
                    data=data,
                    auth=(self.account_sid, self.auth_token),
                )
                res_data = response.json()
                if response.status_code in (200, 201):
                    logger.info(f"Twilio message sent successfully to {formatted_to} [SID: {res_data.get('sid')}]")
                    return {
                        "status": "sent",
                        "provider_message_id": res_data.get("sid"),
                        "channel": channel,
                        "raw_response": res_data,
                    }
                else:
                    logger.error(f"Twilio API Error ({response.status_code}): {res_data}")
                    return {
                        "status": "failed",
                        "error": res_data.get("message", "Twilio sending failed"),
                        "channel": channel,
                    }
        except Exception as e:
            logger.exception(f"Twilio HTTP exception: {e}")
            return {"status": "failed", "error": str(e), "channel": channel}

    def validate_webhook_signature(
        self, url: str, params: Dict[str, Any], signature: str
    ) -> bool:
        if not self.auth_token or not signature:
            return True  # Bypass in local dev mode if token not set
        
        # Twilio signature calculation: URL + sorted key-value params hashed with Auth Token
        data_str = url + "".join(f"{k}{params[k]}" for k in sorted(params.keys()))
        mac = hmac.new(self.auth_token.encode("utf-8"), data_str.encode("utf-8"), hashlib.sha1)
        import base64
        expected_sig = base64.b64encode(mac.digest()).decode("utf-8")
        return hmac.compare_digest(expected_sig, signature)


class MockCommunicationProvider(BaseCommunicationProvider):
    """Mock Provider for safe offline local development and automated testing."""

    def send_message(
        self,
        to_number: str,
        message: str,
        channel: str = "whatsapp",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        msg_id = f"MOCK_{uuid.uuid4().hex[:12].upper()}"
        logger.info(f"[MOCK-{channel.upper()}] Outbound message to {to_number}:\n\"{message}\"\n[ID: {msg_id}]")
        return {
            "status": "sent",
            "provider_message_id": msg_id,
            "channel": channel,
            "mock": True,
        }

    def validate_webhook_signature(
        self, url: str, params: Dict[str, Any], signature: str
    ) -> bool:
        return True


def get_communication_provider() -> BaseCommunicationProvider:
    """Factory function returning active provider based on environment config."""
    if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN:
        return TwilioProvider()
    return MockCommunicationProvider()
