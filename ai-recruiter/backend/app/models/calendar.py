"""
calendar.py — Models for recruiter calendar connections (Google/Outlook OAuth)
and scheduled candidate interview events.
"""
import enum
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.db_types import GUID
from app.models.base import TimestampMixin


class CalendarProvider(str, enum.Enum):
    google = "google"
    outlook = "outlook"


class ScheduledInterviewStatus(str, enum.Enum):
    scheduled = "SCHEDULED"
    confirmed = "CONFIRMED"
    in_progress = "IN_PROGRESS"
    rescheduled = "RESCHEDULED"
    cancelled = "CANCELLED"
    completed = "COMPLETED"
    no_show = "NO_SHOW"


class CalendarConnection(Base, TimestampMixin):
    __tablename__ = "calendar_connections"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    recruiter_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    provider: Mapped[CalendarProvider] = mapped_column(
        Enum(CalendarProvider, name="calendar_provider"), nullable=False
    )
    access_token_encrypted: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    refresh_token_encrypted: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    connected: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    account_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    recruiter = relationship("User", backref="calendar_connections")

    def __repr__(self) -> str:
        return f"<CalendarConnection recruiter={self.recruiter_id} provider={self.provider} connected={self.connected}>"


class ScheduledInterview(Base, TimestampMixin):
    __tablename__ = "scheduled_interviews"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    interview_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        GUID(), ForeignKey("interviews.id", ondelete="SET NULL"), nullable=True, index=True
    )
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("candidate_profiles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    recruiter_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    application_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        GUID(), ForeignKey("applications.id", ondelete="CASCADE"), nullable=True, index=True
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    interview_type: Mapped[str] = mapped_column(String(100), default="AI Technical Interview", nullable=False)
    duration_minutes: Mapped[int] = mapped_column(default=30, nullable=False)
    
    start_time_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    end_time_utc: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    timezone: Mapped[str] = mapped_column(String(100), default="UTC", nullable=False)

    status: Mapped[ScheduledInterviewStatus] = mapped_column(
        Enum(ScheduledInterviewStatus, name="scheduled_interview_status"),
        default=ScheduledInterviewStatus.scheduled,
        nullable=False,
        index=True
    )

    meeting_room_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    join_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    recruiter_joined_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    candidate_joined_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    calendar_provider: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    calendar_event_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    calendar_event_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    calendar_sync_status: Mapped[str] = mapped_column(String(50), default="synced", nullable=False) # synced, failed, pending

    reminder_sent: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    reminder_24h_sent: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    reminder_1h_sent: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    invitation_sent: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    calendar_synced: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    cancelled_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    cancellation_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    rescheduled_from_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        GUID(), ForeignKey("scheduled_interviews.id", ondelete="SET NULL"), nullable=True
    )

    candidate = relationship("CandidateProfile", backref="scheduled_interviews")
    recruiter = relationship("User", backref="recruiter_scheduled_interviews")
    job = relationship("Job", backref="scheduled_interviews")
    application = relationship("Application", backref="scheduled_interviews")
    interview = relationship("Interview", backref="scheduled_session")

    @property
    def scheduled_start_utc(self) -> datetime:
        return self.start_time_utc

    @property
    def scheduled_end_utc(self) -> datetime:
        return self.end_time_utc

    def __repr__(self) -> str:
        return f"<ScheduledInterview {self.title} status={self.status} start={self.start_time_utc}>"
