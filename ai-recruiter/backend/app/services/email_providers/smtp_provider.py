"""
smtp_provider.py — Standard SMTP Email Provider.
"""
import logging
import smtplib
import uuid
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Dict, Any, Optional

from app.core.config import settings
from app.services.email_providers.base import BaseEmailProvider

logger = logging.getLogger("ai_recruiter.email.smtp")


class SmtpEmailProvider(BaseEmailProvider):
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: str,
        from_email: Optional[str] = None,
        from_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        smtp_user = settings.smtp_user_credential
        smtp_password = settings.SMTP_PASSWORD

        sender_addr = from_email or settings.sender_email
        sender_label = from_name or settings.sender_name

        if not smtp_user or not smtp_password:
            logger.info("SMTP credentials missing; writing email output to dev console.")
            try:
                print(f"\n==================== [DEV CONSOLE EMAIL] ====================")
                print(f"To: {to_email}\nSubject: {subject}\n\n{text_content}")
                print(f"===========================================================\n")
            except Exception:
                safe_subj = subject.encode('ascii', errors='backslashreplace').decode('ascii')
                safe_text = text_content.encode('ascii', errors='backslashreplace').decode('ascii')
                print(f"\n==================== [DEV CONSOLE EMAIL] ====================")
                print(f"To: {to_email}\nSubject: {safe_subj}\n\n{safe_text}")
                print(f"===========================================================\n")
            return {
                "success": True,
                "provider_message_id": f"dev_console_{uuid.uuid4()}",
                "error": None
            }

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = f"{sender_label} <{sender_addr}>"
            msg["To"] = to_email

            part1 = MIMEText(text_content, "plain")
            part2 = MIMEText(html_content, "html")
            msg.attach(part1)
            msg.attach(part2)

            smtp_host = settings.SMTP_HOST or "smtp.gmail.com"
            smtp_port = int(settings.SMTP_PORT or 587)

            if smtp_port == 465:
                with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=15) as server:
                    server.login(smtp_user, smtp_password)
                    server.sendmail(sender_addr, [to_email], msg.as_string())
            else:
                with smtplib.SMTP(smtp_host, smtp_port, timeout=15) as server:
                    server.starttls()
                    server.login(smtp_user, smtp_password)
                    server.sendmail(sender_addr, [to_email], msg.as_string())

            msg_id = f"smtp_{uuid.uuid4().hex[:12]}"
            logger.info(f"Delivered email via SMTP to {to_email} ({msg_id})")
            return {"success": True, "provider_message_id": msg_id, "error": None}
        except Exception as exc:
            err_str = str(exc)
            logger.error(f"SMTP delivery failed to {to_email}: {err_str}")
            return {"success": False, "provider_message_id": None, "error": err_str}
