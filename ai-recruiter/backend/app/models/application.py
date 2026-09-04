"""
Application model — a candidate's application to a job, carrying the
computed match score and a JSON-serialized explanation of that score.
"""
import enum
import uuid
from typing import Optional

from sqlalchemy import Boolean, DateTime, Enum, Float, ForeignKey, String, Text, UniqueConstraint, func
from app.core.db_types import GUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ApplicationStatus(str, enum.Enum):
    applied = "applied"
    under_review = "under_review"
    shortlisted = "shortlisted"
    interview = "interview"
    selected = "selected"
    rejected = "rejected"


class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (UniqueConstraint("candidate_id", "job_id", name="uq_candidate_job_application"),)

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("candidate_profiles.id", ondelete="CASCADE"), nullable=False
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False
    )
    status: Mapped[ApplicationStatus] = mapped_column(
        Enum(ApplicationStatus, name="application_status"), default=ApplicationStatus.applied, nullable=False
    )
    match_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    match_breakdown: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON string

    # Detailed ATS Screening & Match Sub-Scores
    ats_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    job_match_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    skills_match_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    experience_match_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    education_match_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    location_match_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    keyword_match_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    responsibility_match_score: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    matched_skills: Mapped[Optional[str]] = mapped_column(Text, nullable=True)      # JSON list string
    missing_skills: Mapped[Optional[str]] = mapped_column(Text, nullable=True)      # JSON list string
    matched_keywords: Mapped[Optional[str]] = mapped_column(Text, nullable=True)    # JSON list string
    missing_keywords: Mapped[Optional[str]] = mapped_column(Text, nullable=True)    # JSON list string

    recommendation: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    screening_status: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    is_eligible: Mapped[Optional[bool]] = mapped_column(Boolean, default=False, nullable=True)
    is_shortlisted: Mapped[Optional[bool]] = mapped_column(Boolean, default=False, nullable=True)
    screened_at: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True), nullable=True)
    screening_version: Mapped[Optional[str]] = mapped_column(String(50), default="v1.0", nullable=True)

    # Recruiter Override tracking
    recruiter_override: Mapped[Optional[bool]] = mapped_column(Boolean, default=False, nullable=True)
    override_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Recruiter Upload & Source Tracking
    uploaded_by_recruiter_id: Mapped[Optional[str]] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    source: Mapped[Optional[str]] = mapped_column(String(100), default="direct_candidate", nullable=True)

    applied_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    candidate: Mapped["CandidateProfile"] = relationship()
    job: Mapped["Job"] = relationship(back_populates="applications")

    def __repr__(self) -> str:
        return f"<Application candidate={self.candidate_id} job={self.job_id} score={self.match_score}>"
