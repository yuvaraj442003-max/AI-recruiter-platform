"""
sendgrid_provider.py — SendGrid API Email Provider using httpx.
"""
import logging
import os
import uuid
from typing import Dict, Any, Optional

import httpx
from app.core.config import settings
from app.services.email_providers.base import BaseEmailProvider

logger = logging.getLogger("ai_recruiter.email.sendgrid")


class SendGridEmailProvider(BaseEmailProvider):
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: str,
        from_email: Optional[str] = None,
        from_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        api_key = os.getenv("SENDGRID_API_KEY", "")
        sender_addr = from_email or settings.sender_email
        sender_label = from_name or settings.sender_name

        if not api_key:
            logger.warning("SENDGRID_API_KEY missing. Falling back to dev console output.")
            print(f"\n==================== [DEV SENDGRID EMAIL] ====================")
            print(f"To: {to_email}\nSubject: {subject}\n\n{text_content}")
            print(f"==============================================================\n")
            return {"success": True, "provider_message_id": f"sendgrid_mock_{uuid.uuid4()}", "error": None}

        try:
            url = "https://api.sendgrid.com/v3/mail/send"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "personalizations": [{"to": [{"email": to_email}]}],
                "from": {"email": sender_addr, "name": sender_label},
                "subject": subject,
                "content": [
                    {"type": "text/plain", "value": text_content},
                    {"type": "text/html", "value": html_content},
                ],
            }

            resp = httpx.post(url, headers=headers, json=payload, timeout=12.0)
            if resp.status_code in (200, 202):
                msg_id = resp.headers.get("X-Message-Id", f"sg_{uuid.uuid4().hex[:12]}")
                return {"success": True, "provider_message_id": msg_id, "error": None}
            else:
                err_text = resp.text
                logger.error(f"SendGrid API error ({resp.status_code}): {err_text}")
                return {"success": False, "provider_message_id": None, "error": f"HTTP {resp.status_code}: {err_text}"}
        except Exception as exc:
            err_str = str(exc)
            logger.error(f"SendGrid exception sending to {to_email}: {err_str}")
            return {"success": False, "provider_message_id": None, "error": err_str}
