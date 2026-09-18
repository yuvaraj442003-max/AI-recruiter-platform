"""
email_service.py — Multi-provider Email Service Engine.
Supports SMTP, SendGrid, and Amazon SES providers, Jinja2/HTML template rendering,
background queueing, idempotency (duplicate prevention), recruiter email preferences,
and exponential backoff retry tracking.
"""
import os
import logging
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal
from app.models.email_log import EmailLog
from app.models.email_setting import RecruiterEmailSetting
from app.models.user import User
from app.services.email_providers.base import BaseEmailProvider
from app.services.email_providers.smtp_provider import SmtpEmailProvider
from app.services.email_providers.sendgrid_provider import SendGridEmailProvider
from app.services.email_providers.ses_provider import SesEmailProvider

logger = logging.getLogger("ai_recruiter.email")

_executor = ThreadPoolExecutor(max_workers=4)
TEMPLATES_DIR = Path(__file__).parent.parent / "templates" / "email"


def _send_smtp_email(
    to_email: str,
    subject: str,
    html_content: str,
    text_content: str,
    email_type: str = "general",
    db: Optional[Session] = None,
) -> bool:
    """Backward compatibility helper mapping to EmailService.send_queued_email."""
    return EmailService.send_queued_email(
        to_email=to_email,
        subject=subject,
        email_type=email_type,
        html_content=html_content,
        text_content=text_content,
    )


def get_email_provider() -> BaseEmailProvider:
    provider_name = os.getenv("EMAIL_PROVIDER", getattr(settings, "EMAIL_PROVIDER", "smtp")).lower()
    if provider_name == "sendgrid":
        return SendGridEmailProvider()
    elif provider_name in ("ses", "aws_ses"):
        return SesEmailProvider()
    return SmtpEmailProvider()


def render_template(template_name: str, context: Dict[str, Any]) -> str:
    template_path = TEMPLATES_DIR / template_name
    if not template_path.exists():
        logger.warning(f"Email template {template_name} not found at {template_path}. Using fallback.")
        return "<p>" + "<br>".join([f"<strong>{k}:</strong> {v}" for k, v in context.items()]) + "</p>"

    html = template_path.read_text(encoding="utf-8")
    for key, val in context.items():
        html = html.replace(f"{{{{{key}}}}}", str(val if val is not None else ""))
    return html


class EmailService:
    @staticmethod
    def is_event_enabled_for_recruiter(db: Session, recruiter_id: Optional[Any], event_key: str) -> bool:
        if not recruiter_id:
            return True
        setting = db.scalar(select(RecruiterEmailSetting).where(RecruiterEmailSetting.recruiter_id == recruiter_id))
        if not setting:
            return True # default enabled
        return getattr(setting, event_key, True)

    @classmethod
    def send_queued_email(
        cls,
        to_email: str,
        subject: str,
        email_type: str,
        html_content: str,
        text_content: str,
        idempotency_key: Optional[str] = None,
        candidate_id: Optional[Any] = None,
        job_id: Optional[Any] = None,
        interview_id: Optional[Any] = None,
        max_retries: int = 3,
    ) -> bool:
        """
        Dispatches email asynchronously via background thread pool with idempotency check
        and exponential backoff retry logic.
        """
        def _bg_task():
            db: Session = SessionLocal()
            try:
                # Idempotency / Duplicate send prevention
                if idempotency_key:
                    existing = db.scalar(select(EmailLog).where(EmailLog.idempotency_key == idempotency_key))
                    if existing and existing.status == "Sent":
                        logger.info(f"Duplicate email prevented by idempotency_key '{idempotency_key}'")
                        return

                email_log = EmailLog(
                    to_email=to_email,
                    subject=subject,
                    email_type=email_type,
                    status="Pending",
                    idempotency_key=idempotency_key or f"{email_type}_{uuid.uuid4().hex[:12]}",
                    candidate_id=candidate_id,
                    job_id=job_id,
                    interview_id=interview_id,
                )
                db.add(email_log)
                db.commit()
                db.refresh(email_log)

                provider = get_email_provider()
                attempt = 0
                sent = False
                last_err = None

                while attempt < max_retries and not sent:
                    attempt += 1
                    email_log.retry_count = attempt
                    result = provider.send_email(to_email, subject, html_content, text_content)

                    if result.get("success"):
                        sent = True
                        email_log.status = "Sent"
                        email_log.provider_message_id = result.get("provider_message_id")
                        email_log.sent_at = datetime.now(timezone.utc)
                        email_log.error_message = None
                    else:
                        last_err = result.get("error", "Unknown delivery error")
                        email_log.status = "Retrying" if attempt < max_retries else "Failed"
                        email_log.error_message = last_err
                        email_log.failed_at = datetime.now(timezone.utc)
                    
                    db.commit()
                    if not sent and attempt < max_retries:
                        time.sleep(2 ** attempt) # Exponential backoff: 2s, 4s, 8s

                if not sent:
                    logger.error(f"Email delivery permanently failed to {to_email} after {max_retries} attempts: {last_err}")
            except Exception as e:
                logger.error(f"Background email worker error: {e}")
            finally:
                db.close()

        _executor.submit(_bg_task)
        return True


# --- High-level System Event Wrappers ---

def send_verification_email(
    to_email: str, name: str, otp_code: str, db: Optional[Session] = None, base_url: Optional[str] = None
) -> str:
    subject = "Your AI Recruiter Verification Code"

    context = {"name": name, "otp_code": otp_code, "company_name": "AI Recruiter"}
    html_content = render_template("email_otp.html", context)
    text_content = (
        f"Hello {name},\n\n"
        f"Thank you for registering with AI Recruiter!\n"
        f"Your account verification code is: {otp_code}\n\n"
        f"This code will expire in 10 minutes.\n"
    )

    EmailService.send_queued_email(
        to_email=to_email,
        subject=subject,
        email_type="verification_otp",
        html_content=html_content,
        text_content=text_content,
        idempotency_key=f"verify_otp_{to_email}_{otp_code}",
    )
    return otp_code


def send_reset_password_email(
    to_email: str, name: str, token: str, db: Optional[Session] = None, base_url: Optional[str] = None
) -> str:
    url_base = base_url or settings.FRONTEND_URL or "http://localhost:8000"
    reset_url = f"{url_base.rstrip('/')}/reset-password.html?token={token}"
    subject = "Reset Your AI Recruiter Password"

    context = {"name": name, "reset_url": reset_url, "company_name": "AI Recruiter"}
    html_content = render_template("reset_password.html", context)
    text_content = (
        f"Hello {name},\n\n"
        f"We received a request to reset your password for your AI Recruiter account.\n"
        f"Reset your password here: {reset_url}\n\n"
        f"This link will expire in 2 hours.\n"
    )

    EmailService.send_queued_email(
        to_email=to_email,
        subject=subject,
        email_type="password_reset",
        html_content=html_content,
        text_content=text_content,
        idempotency_key=f"reset_{token}",
    )
    return reset_url


def send_shortlisted_email(
    to_email: str,
    candidate_name: str,
    job_title: str,
    company_name: str,
    candidate_id: Optional[Any] = None,
    job_id: Optional[Any] = None,
    recruiter_id: Optional[Any] = None,
    db: Optional[Session] = None,
) -> bool:
    if db and recruiter_id:
        if not EmailService.is_event_enabled_for_recruiter(db, recruiter_id, "candidate_shortlisted"):
            logger.info("Shortlisted email disabled in recruiter notification settings.")
            return False

    subject = f"You have been shortlisted for {job_title}"
    context = {
        "candidate_name": candidate_name,
        "job_title": job_title,
        "company_name": company_name,
    }
    html_content = render_template("shortlisted.html", context)
    text_content = f"Hello {candidate_name},\n\nCongratulations!\n\nYou have been shortlisted for the {job_title} position at {company_name}.\nOur team will contact you with next steps.\n\nThank you,\nAI Recruiter"

    idempotency = f"shortlist_{candidate_id}_{job_id}" if candidate_id and job_id else None
    return EmailService.send_queued_email(
        to_email=to_email,
        subject=subject,
        email_type="shortlisted",
        html_content=html_content,
        text_content=text_content,
        idempotency_key=idempotency,
        candidate_id=candidate_id,
        job_id=job_id,
    )


def send_interview_invitation_email(
    to_email: str,
    candidate_name: str,
    company_name: str,
    job_title: str,
    interview_date: str,
    interview_time: str,
    location_or_link: str,
    duration: int = 30,
    interview_type: str = "AI Technical Interview",
    instructions: str = "Please make sure you have a working camera, microphone, and stable internet connection.",
    candidate_id: Optional[Any] = None,
    job_id: Optional[Any] = None,
    interview_id: Optional[Any] = None,
    recruiter_id: Optional[Any] = None,
    db: Optional[Session] = None,
) -> bool:
    if db and recruiter_id:
        if not EmailService.is_event_enabled_for_recruiter(db, recruiter_id, "interview_invited"):
            logger.info("Interview invitation email disabled in recruiter settings.")
            return False

    subject = f"Interview Invitation - {job_title}"
    context = {
        "candidate_name": candidate_name,
        "company_name": company_name,
        "job_title": job_title,
        "interview_date": interview_date,
        "interview_time": interview_time,
        "duration": duration,
        "interview_type": interview_type,
        "interview_link": location_or_link,
    }
    html_content = render_template("interview_invitation.html", context)
    text_content = f"Hello {candidate_name},\n\nYou have been invited to an interview for the {job_title} position.\n\nDate: {interview_date}\nTime: {interview_time}\nDuration: {duration} minutes\nInterview Type: {interview_type}\n\nJoin Link: {location_or_link}\n"

    idempotency = f"invite_{interview_id}_{interview_date}_{interview_time}" if interview_id else None
    return EmailService.send_queued_email(
        to_email=to_email,
        subject=subject,
        email_type="interview_invitation",
        html_content=html_content,
        text_content=text_content,
        idempotency_key=idempotency,
        candidate_id=candidate_id,
        job_id=job_id,
        interview_id=interview_id,
    )


def send_interview_rescheduled_email(
    to_email: str,
    candidate_name: str,
    job_title: str,
    company_name: str,
    new_date: str,
    new_time: str,
    duration: int = 30,
    interview_link: str = "",
    candidate_id: Optional[Any] = None,
    job_id: Optional[Any] = None,
    interview_id: Optional[Any] = None,
    recruiter_id: Optional[Any] = None,
    db: Optional[Session] = None,
) -> bool:
    if db and recruiter_id:
        if not EmailService.is_event_enabled_for_recruiter(db, recruiter_id, "interview_rescheduled"):
            return False

    subject = f"Interview Rescheduled - {job_title}"
    context = {
        "candidate_name": candidate_name,
        "job_title": job_title,
        "company_name": company_name,
        "interview_date": new_date,
        "interview_time": new_time,
        "duration": duration,
        "interview_link": interview_link,
    }
    html_content = render_template("interview_rescheduled.html", context)
    text_content = f"Hello {candidate_name},\n\nYour interview has been rescheduled.\n\nNew Date: {new_date}\nNew Time: {new_time}\n"

    idempotency = f"resched_{interview_id}_{new_date}_{new_time}" if interview_id else None
    return EmailService.send_queued_email(
        to_email=to_email,
        subject=subject,
        email_type="interview_rescheduled",
        html_content=html_content,
        text_content=text_content,
        idempotency_key=idempotency,
        candidate_id=candidate_id,
        job_id=job_id,
        interview_id=interview_id,
    )


def send_interview_cancelled_email(
    to_email: str,
    candidate_name: str,
    job_title: str,
    company_name: str,
    candidate_id: Optional[Any] = None,
    job_id: Optional[Any] = None,
    interview_id: Optional[Any] = None,
    recruiter_id: Optional[Any] = None,
    db: Optional[Session] = None,
) -> bool:
    if db and recruiter_id:
        if not EmailService.is_event_enabled_for_recruiter(db, recruiter_id, "interview_cancelled"):
            return False

    subject = f"Interview Cancelled - {job_title}"
    context = {
        "candidate_name": candidate_name,
        "job_title": job_title,
        "company_name": company_name,
    }
    html_content = render_template("interview_cancelled.html", context)
    text_content = f"Hello {candidate_name},\n\nYour scheduled interview for {job_title} has been cancelled.\nThe recruitment team will contact you regarding next steps."

    idempotency = f"cancel_{interview_id}" if interview_id else None
    return EmailService.send_queued_email(
        to_email=to_email,
        subject=subject,
        email_type="interview_cancelled",
        html_content=html_content,
        text_content=text_content,
        idempotency_key=idempotency,
        candidate_id=candidate_id,
        job_id=job_id,
        interview_id=interview_id,
    )


def send_application_received_email(
    to_email: str,
    candidate_name: str,
    job_title: str,
    company_name: str,
    candidate_id: Optional[Any] = None,
    job_id: Optional[Any] = None,
    db: Optional[Session] = None,
) -> bool:
    subject = f"Application Received - {job_title}"
    context = {
        "candidate_name": candidate_name,
        "job_title": job_title,
        "company_name": company_name,
    }
    html_content = render_template("application_received.html", context)
    text_content = f"Hello {candidate_name},\n\nThank you for applying for the {job_title} position at {company_name}.\nYour application has been successfully received."

    idempotency = f"app_recv_{candidate_id}_{job_id}" if candidate_id and job_id else None
    return EmailService.send_queued_email(
        to_email=to_email,
        subject=subject,
        email_type="application_received",
        html_content=html_content,
        text_content=text_content,
        idempotency_key=idempotency,
        candidate_id=candidate_id,
        job_id=job_id,
    )


def send_application_status_email(
    to_email: str,
    candidate_name: str,
    job_title: str,
    company_name: str,
    new_status: str,
    notes: Optional[str] = None,
    candidate_id: Optional[Any] = None,
    job_id: Optional[Any] = None,
    recruiter_id: Optional[Any] = None,
    db: Optional[Session] = None,
) -> bool:
    clean_status = new_status.replace("_", " ").title()

    if db and recruiter_id:
        if clean_status == "Rejected" and not EmailService.is_event_enabled_for_recruiter(db, recruiter_id, "candidate_rejected"):
            logger.info("Candidate rejected email disabled in recruiter notification settings.")
            return False

    subject = f"Application Update: {job_title} at {company_name}"
    context = {
        "candidate_name": candidate_name,
        "job_title": job_title,
        "company_name": company_name,
        "status_label": clean_status,
        "status_description": f"Your application status has been updated to {clean_status}."
    }
    html_content = render_template("application_status.html", context)
    text_content = f"Hello {candidate_name},\n\nYour application status for {job_title} at {company_name} is now: {clean_status}."

    idempotency = f"status_{candidate_id}_{job_id}_{clean_status}" if candidate_id and job_id else None
    return EmailService.send_queued_email(
        to_email=to_email,
        subject=subject,
        email_type="status_update",
        html_content=html_content,
        text_content=text_content,
        idempotency_key=idempotency,
        candidate_id=candidate_id,
        job_id=job_id,
    )
