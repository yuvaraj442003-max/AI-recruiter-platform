"""
base.py — Abstract Base Class for Email Providers.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseEmailProvider(ABC):
    """Abstract interface that all email delivery providers (SMTP, SendGrid, Amazon SES) must implement."""

    @abstractmethod
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: str,
        from_email: Optional[str] = None,
        from_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Sends an email.
        Must return a dict: {"success": bool, "provider_message_id": Optional[str], "error": Optional[str]}
        """
        pass
