"""
smtp_provider.py — Standard SMTP Email Provider.
"""
import logging
import smtplib
import uuid
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
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
            msg["Subject"] = Header(subject, "utf-8")
            msg["From"] = formataddr((str(Header(sender_label, "utf-8")), sender_addr))
            msg["To"] = to_email

            part1 = MIMEText(text_content, "plain", "utf-8")
            part2 = MIMEText(html_content, "html", "utf-8")
            msg.attach(part1)
            msg.attach(part2)

            smtp_host = settings.SMTP_HOST or "smtp.gmail.com"
            smtp_port = int(settings.SMTP_PORT or 587)

            sent = False
            err_reasons = []

            # 1. Primary attempt using configured port (587 or 465)
            try:
                if smtp_port == 465:
                    with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=12) as server:
                        server.login(smtp_user, smtp_password)
                        server.sendmail(sender_addr, [to_email], msg.as_string())
                else:
                    with smtplib.SMTP(smtp_host, smtp_port, timeout=12) as server:
                        server.starttls()
                        server.login(smtp_user, smtp_password)
                        server.sendmail(sender_addr, [to_email], msg.as_string())
                sent = True
            except Exception as e1:
                err_reasons.append(f"Port {smtp_port} failed: {e1}")

            # 2. Cloud environment fallback: If Port 587 fails (blocked by Railway/cloud firewall), try SSL on Port 465
            if not sent and smtp_port != 465:
                try:
                    logger.info(f"Port {smtp_port} failed on cloud host; attempting fallback via SMTP_SSL on Port 465...")
                    with smtplib.SMTP_SSL(smtp_host, 465, timeout=12) as server:
                        server.login(smtp_user, smtp_password)
                        server.sendmail(sender_addr, [to_email], msg.as_string())
                    sent = True
                except Exception as e2:
                    err_reasons.append(f"Port 465 SSL fallback failed: {e2}")

            if sent:
                msg_id = f"smtp_{uuid.uuid4().hex[:12]}"
                logger.info(f"Delivered email via SMTP to {to_email} ({msg_id})")
                return {"success": True, "provider_message_id": msg_id, "error": None}
            else:
                err_str = "; ".join(err_reasons)
                logger.error(f"SMTP delivery failed to {to_email}: {err_str}")
                try:
                    print(f"\n==================== [FALLBACK CONSOLE EMAIL (SMTP DELIVERY FAILED)] ====================")
                    print(f"To: {to_email}\nSubject: {subject}\n\n{text_content}")
                    print(f"========================================================================================\n")
                except Exception:
                    pass
                return {"success": False, "provider_message_id": None, "error": err_str}
        except Exception as exc:
            err_str = str(exc)
            logger.error(f"SMTP delivery failed to {to_email}: {err_str}")
            try:
                print(f"\n==================== [FALLBACK CONSOLE EMAIL (SMTP DELIVERY FAILED)] ====================")
                print(f"To: {to_email}\nSubject: {subject}\n\n{text_content}")
                print(f"========================================================================================\n")
            except Exception:
                pass
            return {"success": False, "provider_message_id": None, "error": err_str}
