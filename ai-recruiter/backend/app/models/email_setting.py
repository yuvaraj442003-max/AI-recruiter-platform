"""
email_setting.py — Model for recruiter email notification preferences.
"""
import uuid
from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.db_types import GUID
from app.models.base import TimestampMixin


class RecruiterEmailSetting(Base, TimestampMixin):
    __tablename__ = "recruiter_email_settings"

    id: Mapped[uuid.UUID] = mapped_column(GUID(), primary_key=True, default=uuid.uuid4)
    recruiter_id: Mapped[uuid.UUID] = mapped_column(
        GUID(), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True
    )

    app_received: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    candidate_shortlisted: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    candidate_selected: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    interview_invited: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    interview_reminder: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    interview_rescheduled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    interview_cancelled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    candidate_rejected: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False) # disabled by default

    recruiter = relationship("User", backref="email_settings")

    def __repr__(self) -> str:
        return f"<RecruiterEmailSetting recruiter={self.recruiter_id}>"
