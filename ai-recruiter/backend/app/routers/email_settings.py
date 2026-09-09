"""
email_settings.py — API Router for Recruiter Email Preferences & Delivery Audit Logs.
"""
from typing import List, Optional
from pydantic import BaseModel
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_role
from app.models.email_log import EmailLog
from app.models.email_setting import RecruiterEmailSetting
from app.models.user import User, UserRole
from app.schemas.common import APIResponse

router = APIRouter(prefix="/notifications", tags=["Email & Notifications"])


class EmailSettingUpdate(BaseModel):
    app_received: Optional[bool] = True
    candidate_shortlisted: Optional[bool] = True
    interview_invited: Optional[bool] = True
    interview_reminder: Optional[bool] = True
    interview_rescheduled: Optional[bool] = True
    interview_cancelled: Optional[bool] = True
    candidate_rejected: Optional[bool] = False


@router.get("/email-settings")
def get_email_settings(
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.admin)),
    db: Session = Depends(get_db),
):
    setting = db.scalar(select(RecruiterEmailSetting).where(RecruiterEmailSetting.recruiter_id == current_user.id))
    if not setting:
        setting = RecruiterEmailSetting(recruiter_id=current_user.id)
        db.add(setting)
        db.commit()
        db.refresh(setting)

    return APIResponse(
        success=True,
        message="Email notification settings",
        data={
            "app_received": setting.app_received,
            "candidate_shortlisted": setting.candidate_shortlisted,
            "interview_invited": setting.interview_invited,
            "interview_reminder": setting.interview_reminder,
            "interview_rescheduled": setting.interview_rescheduled,
            "interview_cancelled": setting.interview_cancelled,
            "candidate_rejected": setting.candidate_rejected,
        },
    )


@router.put("/email-settings")
def update_email_settings(
    payload: EmailSettingUpdate,
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.admin)),
    db: Session = Depends(get_db),
):
    setting = db.scalar(select(RecruiterEmailSetting).where(RecruiterEmailSetting.recruiter_id == current_user.id))
    if not setting:
        setting = RecruiterEmailSetting(recruiter_id=current_user.id)
        db.add(setting)

    for field, val in payload.model_dump(exclude_unset=True).items():
        setattr(setting, field, val)

    db.commit()
    db.refresh(setting)
    return APIResponse(
        success=True,
        message="Email settings updated successfully",
        data={
            "app_received": setting.app_received,
            "candidate_shortlisted": setting.candidate_shortlisted,
            "interview_invited": setting.interview_invited,
            "interview_reminder": setting.interview_reminder,
            "interview_rescheduled": setting.interview_rescheduled,
            "interview_cancelled": setting.interview_cancelled,
            "candidate_rejected": setting.candidate_rejected,
        },
    )


@router.get("/logs")
def list_email_logs(
    limit: int = Query(default=50, le=200),
    current_user: User = Depends(require_role(UserRole.recruiter, UserRole.admin)),
    db: Session = Depends(get_db),
):
    logs = db.scalars(
        select(EmailLog).order_by(EmailLog.created_at.desc()).limit(limit)
    ).all()

    return APIResponse(
        success=True,
        message="Email Logs",
        data=[
            {
                "id": str(l.id),
                "to_email": l.to_email,
                "subject": l.subject,
                "email_type": l.email_type,
                "status": l.status,
                "retry_count": l.retry_count,
                "created_at": l.created_at,
                "sent_at": l.sent_at,
                "failed_at": l.failed_at,
                "error_message": l.error_message,
            }
            for l in logs
        ],
    )
