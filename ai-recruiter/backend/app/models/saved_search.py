"""
saved_search.py — Models for saved candidate searches, search history, direct invitations, and shortlists.
"""
import uuid
from typing import Optional

from sqlalchemy import ForeignKey, String, Text, JSON
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.db_types import GUID
from app.models.base import TimestampMixin


class SavedCandidateSearch(Base, TimestampMixin):
    __tablename__ = "saved_candidate_searches"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    recruiter_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    query: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    job_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        GUID(), ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True
    )
    filters: Mapped[Optional[dict]] = mapped_column(JSON().with_variant(JSONB, "postgresql"), nullable=True)

    recruiter = relationship("User", foreign_keys=[recruiter_id])
    job = relationship("Job", foreign_keys=[job_id])

    def __repr__(self) -> str:
        return f"<SavedCandidateSearch {self.name} recruiter={self.recruiter_id}>"


class CandidateSearchHistory(Base, TimestampMixin):
    __tablename__ = "candidate_search_history"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    recruiter_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    query: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    filters: Mapped[Optional[dict]] = mapped_column(JSON().with_variant(JSONB, "postgresql"), nullable=True)

    recruiter = relationship("User", foreign_keys=[recruiter_id])

    def __repr__(self) -> str:
        return f"<CandidateSearchHistory query={self.query} recruiter={self.recruiter_id}>"


class CandidateInvitation(Base, TimestampMixin):
    __tablename__ = "candidate_invitations"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    recruiter_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("candidate_profiles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    job_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False, index=True
    )
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="invited", nullable=False)  # invited, accepted, declined

    recruiter = relationship("User", foreign_keys=[recruiter_id])
    candidate = relationship("CandidateProfile", foreign_keys=[candidate_id])
    job = relationship("Job", foreign_keys=[job_id])

    def __repr__(self) -> str:
        return f"<CandidateInvitation candidate={self.candidate_id} job={self.job_id} status={self.status}>"


class CandidateShortlist(Base, TimestampMixin):
    __tablename__ = "candidate_shortlists"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    recruiter_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    candidate_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("candidate_profiles.id", ondelete="CASCADE"), nullable=False, index=True
    )
    job_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        GUID(), ForeignKey("jobs.id", ondelete="SET NULL"), nullable=True, index=True
    )
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    recruiter = relationship("User", foreign_keys=[recruiter_id])
    candidate = relationship("CandidateProfile", foreign_keys=[candidate_id])
    job = relationship("Job", foreign_keys=[job_id])

    def __repr__(self) -> str:
        return f"<CandidateShortlist candidate={self.candidate_id} recruiter={self.recruiter_id}>"
