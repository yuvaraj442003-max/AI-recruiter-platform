"""
Schemas for the recruiter and candidate analytics dashboards.
"""
from typing import Optional

from pydantic import BaseModel


class ApplicationsByJob(BaseModel):
    job_title: str
    count: int


class SkillCount(BaseModel):
    skill: str
    count: int


class InterviewScoreEntry(BaseModel):
    job_title: Optional[str] = None
    overall_score: float


class JobPerformance(BaseModel):
    job_title: str
    status: str
    applications: int
    avg_match_score: Optional[float] = None
    interviews_completed: int


class RecruiterAnalytics(BaseModel):
    total_jobs: int
    published_jobs: int
    total_applications: int
    total_candidates: int
    shortlisted_count: int
    interview_count: int
    selected_count: int
    hired_count: Optional[int] = 0
    conversion_rate: Optional[float] = 0.0
    avg_match_score: Optional[float] = None
    avg_interview_score: Optional[float] = None
    hiring_funnel: dict[str, int]
    funnel_stages: Optional[dict[str, int]] = None
    match_score_distribution: Optional[dict[str, int]] = None
    missing_skills_analysis: Optional[list[SkillCount]] = None
    applications_by_job: list[ApplicationsByJob]
    top_skills: list[SkillCount]
    interview_scores: list[InterviewScoreEntry]
    job_performance: list[JobPerformance]


class CandidateAnalytics(BaseModel):
    profile_completion: int
    resume_uploaded: bool
    skills: list[str]
    applications_count: int
    applications_by_status: dict[str, int]
    shortlisted_count: Optional[int] = 0
    selected_count: Optional[int] = 0
    interviews_count: int
    interview_status: str
    latest_interview_score: Optional[float] = None
    recommended_jobs_count: int
