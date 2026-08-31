"""
Recruiter & Company Profile model.
"""
import uuid
from typing import Optional

from sqlalchemy import ForeignKey, String, Text
from app.core.db_types import GUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class RecruiterProfile(Base, TimestampMixin):
    __tablename__ = "recruiter_profiles"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False
    )

    company_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        GUID(), ForeignKey("companies.id", ondelete="SET NULL"), nullable=True
    )

    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    recruiter_linkedin_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    company_linkedin_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    profile_photo: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    job_title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    company_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    company_logo: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    company_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    industry: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    company_size: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    linkedin_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    github_url: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    other_links: Mapped[Optional[str]] = mapped_column(Text, nullable=True)


    user: Mapped["User"] = relationship()
    company: Mapped[Optional["Company"]] = relationship()

    def __repr__(self) -> str:
        return f"<RecruiterProfile user_id={self.user_id} company={self.company_name}>"
