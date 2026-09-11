"""
User model — shared by recruiters, candidates, and admins.
Role-specific data (e.g. CandidateProfile) is added as separate
tables in later phases and linked via user_id.
"""
import enum
import uuid
from typing import Optional

from datetime import datetime
from sqlalchemy import Boolean, DateTime, Enum, String, Text
from app.core.db_types import GUID
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.models.base import TimestampMixin


class UserRole(str, enum.Enum):
    recruiter = "recruiter"
    candidate = "candidate"
    admin = "admin"
    company_admin = "company_admin"
    superadmin = "superadmin"


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role"), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    verification_status: Mapped[str] = mapped_column(String(50), default="approved", nullable=False) # approved, pending_admin_review, rejected
    verification_reasons: Mapped[Optional[str]] = mapped_column(Text, nullable=True) # JSON list or string

    is_email_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    verification_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    verification_token_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    reset_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    reset_token_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    @property
    def full_name(self) -> str:
        return self.name or ""

    def __repr__(self) -> str:
        return f"<User {self.email} ({self.role}) status={self.verification_status}>"


