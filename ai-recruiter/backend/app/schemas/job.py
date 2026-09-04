"""
Schemas for job creation/update/response.
"""
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.job import EmploymentType, JobStatus


class JobCreate(BaseModel):
    title: str = Field(min_length=2, max_length=255)
    description: str = Field(min_length=10)
    location: Optional[str] = None
    employment_type: EmploymentType = EmploymentType.full_time
    experience_required: Optional[float] = Field(default=None, ge=0)
    salary_range: Optional[str] = None
    status: JobStatus = JobStatus.published
    required_skills: Optional[list[str]] = None
    preferred_skills: Optional[list[str]] = None

    # Extended Requirements Breakdown
    relevant_work_experience: Optional[str] = None
    non_technical_skills: Optional[list[str]] = None
    company_experience_requirements: Optional[str] = None

    # Candidate Screening Settings
    min_ats_score: Optional[float] = 60.0
    min_job_match_score: Optional[float] = 60.0
    min_experience: Optional[float] = 0.0
    auto_screening: Optional[bool] = True
    auto_shortlist: Optional[bool] = True

    # Company Details
    company_name: Optional[str] = None
    company_logo: Optional[str] = None
    company_description: Optional[str] = None
    company_website: Optional[str] = None
    company_location: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    linkedin_profile: Optional[str] = None
    github_profile: Optional[str] = None
    other_links: Optional[str] = None


class JobUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=2, max_length=255)
    description: Optional[str] = Field(default=None, min_length=10)
    location: Optional[str] = None
    employment_type: Optional[EmploymentType] = None
    experience_required: Optional[float] = Field(default=None, ge=0)
    salary_range: Optional[str] = None
    status: Optional[JobStatus] = None
    required_skills: Optional[list[str]] = None
    preferred_skills: Optional[list[str]] = None

    # Extended Requirements Breakdown
    relevant_work_experience: Optional[str] = None
    non_technical_skills: Optional[list[str]] = None
    company_experience_requirements: Optional[str] = None

    # Candidate Screening Settings
    min_ats_score: Optional[float] = None
    min_job_match_score: Optional[float] = None
    min_experience: Optional[float] = None
    auto_screening: Optional[bool] = None
    auto_shortlist: Optional[bool] = None

    # Company Details
    company_name: Optional[str] = None
    company_logo: Optional[str] = None
    company_description: Optional[str] = None
    company_website: Optional[str] = None
    company_location: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    linkedin_profile: Optional[str] = None
    github_profile: Optional[str] = None
    other_links: Optional[str] = None


class JobResponse(BaseModel):
    id: uuid.UUID
    recruiter_id: uuid.UUID
    title: str
    description: str
    location: Optional[str] = None
    employment_type: EmploymentType
    experience_required: Optional[float] = None
    salary_range: Optional[str] = None
    status: JobStatus
    required_skills: list[str] = []
    preferred_skills: list[str] = []

    # Extended Requirements Breakdown
    relevant_work_experience: Optional[str] = None
    non_technical_skills: list[str] = []
    company_experience_requirements: Optional[str] = None

    # Screening Settings
    min_ats_score: Optional[float] = 60.0
    min_job_match_score: Optional[float] = 60.0
    min_experience: Optional[float] = 0.0
    auto_screening: Optional[bool] = True
    auto_shortlist: Optional[bool] = True

    # Fraud Scoring
    fraud_risk_score: Optional[float] = 0.0
    fraud_risk_level: Optional[str] = "LOW"
    fraud_reasons: Optional[str] = None

    # Company Details
    company_name: Optional[str] = None
    company_logo: Optional[str] = None
    company_description: Optional[str] = None
    company_website: Optional[str] = None
    company_location: Optional[str] = None
    industry: Optional[str] = None
    company_size: Optional[str] = None
    linkedin_profile: Optional[str] = None
    github_profile: Optional[str] = None
    other_links: Optional[str] = None

    created_at: datetime
    updated_at: datetime
    applications_count: int = 0

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_job(cls, job) -> "JobResponse":
        raw_non_tech = getattr(job, "non_technical_skills", None)
        non_tech_list = []
        if isinstance(raw_non_tech, list):
            non_tech_list = raw_non_tech
        elif isinstance(raw_non_tech, str) and raw_non_tech.strip():
            non_tech_list = [s.strip() for s in raw_non_tech.split(",") if s.strip()]

        app_count = 0
        if hasattr(job, "applications") and job.applications is not None:
            try:
                app_count = len(job.applications)
            except Exception:
                app_count = getattr(job, "applications_count", 0) or 0
        else:
            app_count = getattr(job, "applications_count", 0) or 0

        return cls(
            id=job.id,
            recruiter_id=job.recruiter_id,
            title=job.title,
            description=job.description,
            location=job.location,
            employment_type=job.employment_type,
            experience_required=job.experience_required,
            salary_range=job.salary_range,
            status=job.status,
            required_skills=sorted(js.skill.skill_name for js in job.job_skills if js.required),
            preferred_skills=sorted(js.skill.skill_name for js in job.job_skills if not js.required),
            relevant_work_experience=getattr(job, "relevant_work_experience", None),
            non_technical_skills=non_tech_list,
            company_experience_requirements=getattr(job, "company_experience_requirements", None),
            applications_count=app_count,
            min_ats_score=getattr(job, "min_ats_score", 60.0) or 60.0,
            min_job_match_score=getattr(job, "min_job_match_score", 60.0) or 60.0,
            min_experience=getattr(job, "min_experience", 0.0) or 0.0,
            auto_screening=getattr(job, "auto_screening", True) if getattr(job, "auto_screening", True) is not None else True,
            auto_shortlist=getattr(job, "auto_shortlist", True) if getattr(job, "auto_shortlist", True) is not None else True,
            fraud_risk_score=getattr(job, "fraud_risk_score", 0.0),
            fraud_risk_level=getattr(job, "fraud_risk_level", "LOW"),
            fraud_reasons=getattr(job, "fraud_reasons", None),
            company_name=getattr(job, "company_name", None),
            company_logo=getattr(job, "company_logo", None),
            company_description=getattr(job, "company_description", None),
            company_website=getattr(job, "company_website", None),
            company_location=getattr(job, "company_location", None),
            industry=getattr(job, "industry", None),
            company_size=getattr(job, "company_size", None),
            linkedin_profile=getattr(job, "linkedin_profile", None),
            github_profile=getattr(job, "github_profile", None),
            other_links=getattr(job, "other_links", None),
            created_at=job.created_at,
            updated_at=job.updated_at,
        )



class JobAnalysisRequest(BaseModel):
    description: str = Field(min_length=10)


class JobAnalysisResponse(BaseModel):
    title: Optional[str] = None
    required_skills: list[str] = []
    preferred_skills: list[str] = []
    experience: Optional[str] = None
    responsibilities: list[str] = []
    source: str


class QuestionGenerationRequest(BaseModel):
    num_questions: int = Field(default=6, ge=1, le=15)


class GeneratedQuestion(BaseModel):
    question: str
    type: str
    difficulty: str
    expected_topics: list[str] = []


class QuestionGenerationResponse(BaseModel):
    questions: list[GeneratedQuestion]
    source: str
