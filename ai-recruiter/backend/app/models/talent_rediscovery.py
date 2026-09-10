"""
talent_rediscovery.py — Database models for Talent Pool Auto-Rediscovery & Silver Medalist Matching System.
Stores background rediscovery runs, candidate rediscovery rankings, Silver Medalist indicators,
historical application context, and multi-dimensional match breakdowns.
"""
import enum
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Enum, Float, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.db_types import GUID
from app.models.base import TimestampMixin


class RediscoveryRunStatus(str, enum.Enum):
    pending = "PENDING"
    queued = "QUEUED"
    processing = "PROCESSING"
    completed = "COMPLETED"
    failed = "FAILED"


class TalentRediscoveryRun(Base, TimestampMixin):
    __tablename__ = "talent_rediscovery_runs"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    job_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[RediscoveryRunStatus] = mapped_column(
        Enum(RediscoveryRunStatus, name="rediscovery_run_status_enum"),
        default=RediscoveryRunStatus.pending,
        nullable=False,
    )
    total_candidates: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    processed_candidates: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    matched_candidates: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    job: Mapped["Job"] = relationship("Job")

    def __repr__(self) -> str:
        return f"<TalentRediscoveryRun job={self.job_id} status={self.status} processed={self.processed_candidates}/{self.total_candidates}>"


class TalentRediscoveryResult(Base, TimestampMixin):
    __tablename__ = "talent_rediscovery_results"
    __table_args__ = (
        UniqueConstraint("job_id", "candidate_id", name="uq_rediscovery_job_candidate"),
    )

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    job_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("candidate_profiles.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Multi-dimensional Match Scores (0 - 100)
    overall_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False, index=True)
    skills_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    experience_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    semantic_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    responsibility_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    keyword_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    location_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)
    education_score: Mapped[float] = mapped_column(Float, default=0.0, nullable=False)

    rank: Mapped[int] = mapped_column(Integer, default=0, nullable=False, index=True)

    # Silver Medalist Indicators
    is_silver_medalist: Mapped[bool] = mapped_column(default=False, nullable=False, index=True)
    previous_job_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        GUID(), ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True
    )
    previous_job_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    previous_application_status: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    previous_ats_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    # Skills & Keywords match breakdowns (JSON string arrays)
    matched_skills: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    missing_skills: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    matched_keywords: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    missing_keywords: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    match_explanation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="rediscovered", nullable=False)  # rediscovered, shortlisted, contacted, rejected

    job: Mapped["Job"] = relationship("Job", foreign_keys=[job_id])
    candidate: Mapped["CandidateProfile"] = relationship("CandidateProfile")
    previous_job: Mapped[Optional["Job"]] = relationship("Job", foreign_keys=[previous_job_id])

    def __repr__(self) -> str:
        return f"<TalentRediscoveryResult job={self.job_id} candidate={self.candidate_id} score={self.overall_score}% silver={self.is_silver_medalist}>"
