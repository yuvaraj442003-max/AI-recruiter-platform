"""
brevo_provider.py — Brevo (formerly Sendinblue) Transactional API Email Provider using httpx.
Zero-port-blocking HTTP REST email delivery for Railway, Vercel, Render & production deployments.
"""
import logging
import os
import uuid
from typing import Dict, Any, Optional

import httpx
from app.core.config import settings
from app.services.email_providers.base import BaseEmailProvider

logger = logging.getLogger("ai_recruiter.email.brevo")


class BrevoEmailProvider(BaseEmailProvider):
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: str,
        from_email: Optional[str] = None,
        from_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        api_key = os.getenv("BREVO_API_KEY") or getattr(settings, "BREVO_API_KEY", "") or ""
        sender_addr = (
            from_email
            or os.getenv("BREVO_FROM_EMAIL")
            or getattr(settings, "BREVO_FROM_EMAIL", "")
            or settings.sender_email
            or "noreply@airecruiter.com"
        )
        sender_label = (
            from_name
            or os.getenv("BREVO_FROM_NAME")
            or getattr(settings, "BREVO_FROM_NAME", "")
            or settings.sender_name
            or "AI Recruiter Team"
        )

        if not api_key:
            logger.warning("BREVO_API_KEY missing in environment/settings. Falling back to dev console output.")
            print(f"\n==================== [DEV BREVO MOCK EMAIL] ====================")
            print(f"To: {to_email}\nSubject: {subject}\n\n{text_content}")
            print(f"===============================================================\n")
            return {"success": True, "provider_message_id": f"brevo_mock_{uuid.uuid4()}", "error": None}

        try:
            url = "https://api.brevo.com/v3/smtp/email"
            headers = {
                "api-key": api_key,
                "accept": "application/json",
                "content-type": "application/json",
            }
            payload = {
                "sender": {
                    "name": sender_label,
                    "email": sender_addr,
                },
                "to": [
                    {
                        "email": to_email,
                    }
                ],
                "subject": subject,
                "htmlContent": html_content,
                "textContent": text_content,
            }

            resp = httpx.post(url, headers=headers, json=payload, timeout=12.0)
            if resp.status_code in (200, 201, 202):
                data = resp.json()
                msg_id = data.get("messageId", f"brevo_{uuid.uuid4().hex[:12]}")
                logger.info(f"Brevo email delivered successfully to {to_email} (messageId: {msg_id})")
                return {"success": True, "provider_message_id": msg_id, "error": None}
            else:
                err_text = resp.text
                logger.error(f"Brevo API error ({resp.status_code}): {err_text}")
                return {"success": False, "provider_message_id": None, "error": f"HTTP {resp.status_code}: {err_text}"}
        except Exception as exc:
            err_str = str(exc)
            logger.error(f"Brevo exception sending to {to_email}: {err_str}")
            return {"success": False, "provider_message_id": None, "error": err_str}
