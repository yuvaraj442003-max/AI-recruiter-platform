"""
reminder_service.py — Background Scheduled Job Engine for Interview Reminders.
Polls upcoming scheduled interviews and dispatches 24h & 1h reminder emails to candidates.
"""
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.core.database import SessionLocal
from app.models.calendar import ScheduledInterview, ScheduledInterviewStatus
from app.models.candidate import CandidateProfile
from app.models.job import Job
from app.models.user import User
from app.services.email_service import EmailService, render_template

logger = logging.getLogger("ai_recruiter.reminders")


def check_and_send_interview_reminders(db: Optional[Session] = None) -> Dict[str, int]:
    """
    Checks upcoming scheduled interviews and triggers 24h & 1h notification emails.
    Can be run periodically via background worker or cron task.
    """
    close_db = False
    if db is None:
        db = SessionLocal()
        close_db = True

    sent_24h_count = 0
    sent_1h_count = 0

    try:
        now = datetime.now(timezone.utc)
        target_24h_start = now + timedelta(hours=23)
        target_24h_end = now + timedelta(hours=25)

        target_1h_start = now + timedelta(minutes=45)
        target_1h_end = now + timedelta(minutes=75)

        # 1. Check 24-Hour Reminders
        interviews_24h = db.scalars(
            select(ScheduledInterview)
            .where(
                ScheduledInterview.status == ScheduledInterviewStatus.scheduled,
                ScheduledInterview.reminder_24h_sent == False,
                ScheduledInterview.start_time_utc >= target_24h_start,
                ScheduledInterview.start_time_utc <= target_24h_end,
            )
        ).all()

        for session in interviews_24h:
            if _dispatch_reminder(db, session, reminder_type="24h"):
                session.reminder_24h_sent = True
                sent_24h_count += 1

        # 2. Check 1-Hour Reminders
        interviews_1h = db.scalars(
            select(ScheduledInterview)
            .where(
                ScheduledInterview.status == ScheduledInterviewStatus.scheduled,
                ScheduledInterview.reminder_1h_sent == False,
                ScheduledInterview.start_time_utc >= target_1h_start,
                ScheduledInterview.start_time_utc <= target_1h_end,
            )
        ).all()

        for session in interviews_1h:
            if _dispatch_reminder(db, session, reminder_type="1h"):
                session.reminder_1h_sent = True
                sent_1h_count += 1

        db.commit()
    except Exception as err:
        logger.error(f"Error checking interview reminders: {err}")
    finally:
        if close_db:
            db.close()

    return {"sent_24h": sent_24h_count, "sent_1h": sent_1h_count}


def _dispatch_reminder(db: Session, session: ScheduledInterview, reminder_type: str) -> bool:
    candidate = db.scalar(select(CandidateProfile).where(CandidateProfile.id == session.candidate_id))
    cand_user = db.scalar(select(User).where(User.id == candidate.user_id)) if candidate else None
    job = db.scalar(select(Job).where(Job.id == session.job_id))

    if not cand_user or not cand_user.email:
        return False

    recruiter_id = session.recruiter_id
    if not EmailService.is_event_enabled_for_recruiter(db, recruiter_id, "interview_reminder"):
        logger.info("Interview reminder disabled in recruiter settings.")
        return False

    cand_name = cand_user.name
    job_title = job.title if job else "Position"
    comp_name = job.company_name if (job and job.company_name) else "AI Recruiter"

    date_str = session.start_time_utc.strftime("%B %d, %Y")
    time_str = f"{session.start_time_utc.strftime('%I:%M %p')} {session.timezone}"

    from app.core.config import settings
    link = f"{settings.FRONTEND_URL.rstrip('/')}/live-interview-room.html?interview_id={session.interview_id or session.id}"

    subject = f"Reminder: {job_title} Interview {'Tomorrow' if reminder_type == '24h' else 'Starting Soon'}"
    context = {
        "candidate_name": cand_name,
        "job_title": job_title,
        "company_name": comp_name,
        "interview_date": date_str,
        "interview_time": time_str,
        "duration": session.duration_minutes,
        "interview_link": link,
    }
    html_content = render_template("interview_reminder.html", context)
    text_content = f"Hello {cand_name},\n\nReminder for your upcoming interview for {job_title} on {date_str} at {time_str}.\nJoin Link: {link}\n"

    idempotency = f"remind_{reminder_type}_{session.id}"
    return EmailService.send_queued_email(
        to_email=cand_user.email,
        subject=subject,
        email_type=f"reminder_{reminder_type}",
        html_content=html_content,
        text_content=text_content,
        idempotency_key=idempotency,
        candidate_id=session.candidate_id,
        job_id=session.job_id,
        interview_id=session.interview_id,
    )
