"""
Company model — represents a registered company/employer entity.
"""
import uuid
from typing import Optional

from sqlalchemy import Boolean, String, Text
from app.core.db_types import GUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class Company(Base, TimestampMixin):
    __tablename__ = "companies"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    industry: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    company_size: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    location: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    logo_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    registration_number: Mapped[Optional[str]] = mapped_column(String(100), nullable=True) # CIN / EIN / CRN
    cin_gstin: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    country: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    domain: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    official_email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    verification_status: Mapped[str] = mapped_column(String(50), default="unverified", nullable=False) # unverified, domain_verified, government_verified
    ssl_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    ssl_details: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    verification_notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    def __repr__(self) -> str:
        return f"<Company {self.name} status={self.verification_status}>"

