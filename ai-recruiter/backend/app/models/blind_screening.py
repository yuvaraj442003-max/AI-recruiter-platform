"""
blind_screening.py — Database models for Blind Screening Mode.
Stores job-level blind screening configurations, candidate anonymization mappings (e.g. CAND-10452),
recruiter decisions, and identity reveal states.
"""
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.db_types import GUID
from app.models.base import TimestampMixin


class BlindScreeningConfig(Base, TimestampMixin):
    __tablename__ = "blind_screening_configs"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    job_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, unique=True
    )
    enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # Granular Field Visibility Controls (True = Hidden, False = Visible)
    hide_name: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    hide_photo: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    hide_age: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    hide_gender: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    hide_location: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    hide_college: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    hide_email: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    hide_phone: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    hide_address: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    hide_social_links: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    reveal_policy: Mapped[str] = mapped_column(String(50), default="reveal_after_shortlist", nullable=False)  # reveal_after_shortlist, manual, reveal_after_interview

    job: Mapped["Job"] = relationship("Job")

    def __repr__(self) -> str:
        return f"<BlindScreeningConfig job={self.job_id} enabled={self.enabled} policy={self.reveal_policy}>"


class BlindScreeningCandidate(Base, TimestampMixin):
    __tablename__ = "blind_screening_candidates"
    __table_args__ = (
        UniqueConstraint("job_id", "candidate_id", name="uq_blind_job_candidate"),
        UniqueConstraint("job_id", "candidate_code", name="uq_blind_job_code"),
    )

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    job_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("candidate_profiles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    candidate_code: Mapped[str] = mapped_column(String(50), nullable=False, index=True)  # e.g. CAND-10452

    screening_status: Mapped[str] = mapped_column(String(50), default="pending", nullable=False)
    recruiter_decision: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)  # shortlist, hold, reject, next_round

    revealed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    revealed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    revealed_by_user_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    job: Mapped["Job"] = relationship("Job")
    candidate: Mapped["CandidateProfile"] = relationship("CandidateProfile")

    def __repr__(self) -> str:
        return f"<BlindScreeningCandidate code={self.candidate_code} job={self.job_id} revealed={self.revealed}>"
