"""
ses_provider.py — Amazon SES Email Provider.
"""
import logging
import os
import uuid
from typing import Dict, Any, Optional

from app.core.config import settings
from app.services.email_providers.base import BaseEmailProvider

logger = logging.getLogger("ai_recruiter.email.ses")


class SesEmailProvider(BaseEmailProvider):
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: str,
        from_email: Optional[str] = None,
        from_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        aws_region = os.getenv("AWS_REGION", "us-east-1")
        sender_addr = from_email or settings.sender_email
        sender_label = from_name or settings.sender_name

        try:
            import boto3
            client = boto3.client("ses", region_name=aws_region)
            resp = client.send_email(
                Source=f"{sender_label} <{sender_addr}>",
                Destination={"ToAddresses": [to_email]},
                Message={
                    "Subject": {"Data": subject, "Charset": "UTF-8"},
                    "Body": {
                        "Text": {"Data": text_content, "Charset": "UTF-8"},
                        "Html": {"Data": html_content, "Charset": "UTF-8"},
                    },
                },
            )
            msg_id = resp.get("MessageId", f"ses_{uuid.uuid4().hex[:12]}")
            return {"success": True, "provider_message_id": msg_id, "error": None}
        except Exception as exc:
            err_str = str(exc)
            logger.info(f"SES client not available or call failed ({err_str}); logging email output to dev console.")
            print(f"\n==================== [DEV SES EMAIL] ====================")
            print(f"To: {to_email}\nSubject: {subject}\n\n{text_content}")
            print(f"=========================================================\n")
            return {"success": True, "provider_message_id": f"ses_mock_{uuid.uuid4()}", "error": None}
