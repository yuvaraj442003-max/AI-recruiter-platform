"""
resend_provider.py — Resend API Email Provider using httpx.
Zero-port-blocking HTTP email delivery for Railway & Vercel deployments.
"""
import logging
import os
import uuid
from typing import Dict, Any, Optional

import httpx
from app.core.config import settings
from app.services.email_providers.base import BaseEmailProvider

logger = logging.getLogger("ai_recruiter.email.resend")


class ResendEmailProvider(BaseEmailProvider):
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: str,
        from_email: Optional[str] = None,
        from_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        api_key = os.getenv("RESEND_API_KEY", "")
        sender_addr = from_email or os.getenv("RESEND_FROM_EMAIL") or settings.sender_email or "onboarding@resend.dev"
        sender_label = from_name or settings.sender_name or "AI Recruiter Team"

        if not api_key:
            logger.warning("RESEND_API_KEY missing. Falling back to dev console output.")
            print(f"\n==================== [DEV RESEND EMAIL] ====================")
            print(f"To: {to_email}\nSubject: {subject}\n\n{text_content}")
            print(f"===========================================================\n")
            return {"success": True, "provider_message_id": f"resend_mock_{uuid.uuid4()}", "error": None}

        try:
            url = "https://api.resend.com/emails"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "from": f"{sender_label} <{sender_addr}>" if sender_label else sender_addr,
                "to": [to_email],
                "subject": subject,
                "html": html_content,
                "text": text_content,
            }

            resp = httpx.post(url, headers=headers, json=payload, timeout=12.0)
            if resp.status_code in (200, 201, 202):
                data = resp.json()
                msg_id = data.get("id", f"resend_{uuid.uuid4().hex[:12]}")
                return {"success": True, "provider_message_id": msg_id, "error": None}
            else:
                err_text = resp.text
                logger.error(f"Resend API error ({resp.status_code}): {err_text}")
                return {"success": False, "provider_message_id": None, "error": f"HTTP {resp.status_code}: {err_text}"}
        except Exception as exc:
            err_str = str(exc)
            logger.error(f"Resend exception sending to {to_email}: {err_str}")
            return {"success": False, "provider_message_id": None, "error": err_str}
