"""
Schemas for the admin panel.
"""
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.user import UserRole


class AdminUserOut(BaseModel):
    id: uuid.UUID
    name: str
    email: str
    role: UserRole
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AdminSkillOut(BaseModel):
    id: uuid.UUID
    skill_name: str
    category: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class AdminSkillCreate(BaseModel):
    skill_name: str = Field(min_length=1, max_length=150)
    category: Optional[str] = None


class AdminJobOut(BaseModel):
    id: uuid.UUID
    title: str
    status: str
    recruiter_name: Optional[str] = None
    applications_count: int
    created_at: datetime


class SkillCountOut(BaseModel):
    skill: str
    count: int


class SystemStats(BaseModel):
    total_users: int
    total_recruiters: int
    total_candidates: int
    total_admins: int
    total_jobs: int
    published_jobs: int
    total_applications: int
    applications_by_status: dict[str, int]
    avg_match_score: Optional[float] = None
    total_interviews: int
    completed_interviews: int
    interview_completion_rate: Optional[float] = None
    avg_interview_score: Optional[float] = None
    most_requested_skills: list[SkillCountOut]
    most_common_candidate_skills: list[SkillCountOut]


class AuditLogOut(BaseModel):
    id: uuid.UUID
    user_id: Optional[uuid.UUID] = None
    action: str
    details: Optional[str] = None
    ip_address: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
