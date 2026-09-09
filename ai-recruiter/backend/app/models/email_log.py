"""
EmailLog model — tracks all outgoing system emails (verification, password reset, interview invites, status updates).
"""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, String, Text, func
from app.core.db_types import GUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class EmailLog(Base):
    __tablename__ = "email_logs"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    to_email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    email_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True) # verification, password_reset, interview_invitation, status_update, shortlisted, application_received, reminder
    status: Mapped[str] = mapped_column(String(20), default="Pending", nullable=False, index=True) # Pending, Sent, Failed, Retrying
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Added fields for robust delivery & tracking
    provider_message_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    idempotency_key: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, unique=True, index=True)
    retry_count: Mapped[int] = mapped_column(default=0, nullable=False)
    candidate_id: Mapped[Optional[uuid.UUID]] = mapped_column(GUID(), nullable=True, index=True)
    job_id: Mapped[Optional[uuid.UUID]] = mapped_column(GUID(), nullable=True, index=True)
    interview_id: Mapped[Optional[uuid.UUID]] = mapped_column(GUID(), nullable=True, index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    sent_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    failed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    def __repr__(self) -> str:
        return f"<EmailLog to={self.to_email} type={self.email_type} status={self.status}>"

