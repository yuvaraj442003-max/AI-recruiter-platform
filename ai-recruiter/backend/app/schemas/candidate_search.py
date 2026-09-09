"""
candidate_search.py — Pydantic schemas for Recruiter Candidate Search & Advanced Filtering endpoints.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class SearchFilters(BaseModel):
    skills: Optional[List[str]] = Field(default_factory=list)
    skill_match_mode: Optional[str] = "all"  # "all" or "any"
    minimum_experience: Optional[float] = None
    maximum_experience: Optional[float] = None
    location: Optional[str] = None
    minimum_ats_score: Optional[float] = None
    maximum_ats_score: Optional[float] = None
    minimum_interview_score: Optional[float] = None
    education: Optional[str] = None
    job_role: Optional[str] = None
    qualification_threshold: Optional[float] = 60.0


class CandidateSearchRequest(BaseModel):
    query: Optional[str] = ""
    job_id: Optional[str] = None
    filters: Optional[SearchFilters] = Field(default_factory=SearchFilters)
    qualification_threshold: Optional[float] = 60.0
    page: int = 1
    page_size: int = 20
    sort_by: str = "best_match"  # "best_match", "ats_score", "experience", "interview_score", "newest", "recently_updated"


class CandidateSearchResultItem(BaseModel):
    candidate_id: str
    user_id: Optional[str] = ""
    candidate_name: str
    candidate_email: Optional[str] = ""
    headline: Optional[str] = ""
    job_role: Optional[str] = ""
    location: Optional[str] = ""
    experience_years: float
    matched_skills: List[str] = Field(default_factory=list)
    missing_skills: List[str] = Field(default_factory=list)
    matched_keywords: List[str] = Field(default_factory=list)
    ats_score: float
    job_match_score: float
    interview_score: Optional[float] = None
    ranking_score: float
    education: Optional[str] = ""
    is_qualified: bool = True
    qualification_badge: str = "Qualified"  # "Qualified" or "Below Threshold"
    match_reasons: List[str] = Field(default_factory=list)
    has_resume: bool = False
    resume_filename: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class CandidateSearchSummaryStats(BaseModel):
    total_found: int = 0
    qualified_count: int = 0
    shortlisted_count: int = 0
    invited_count: int = 0
    interviews_scheduled: int = 0


class CandidateSearchResponse(BaseModel):
    total_results: int
    page: int
    page_size: int
    total_pages: int
    qualification_threshold: float = 60.0
    summary_stats: CandidateSearchSummaryStats = Field(default_factory=CandidateSearchSummaryStats)
    filters_applied: Dict[str, Any]
    results: List[CandidateSearchResultItem]

    model_config = ConfigDict(from_attributes=True)


class SavedSearchCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    query: Optional[str] = ""
    job_id: Optional[str] = None
    filters: Dict[str, Any] = Field(default_factory=dict)


class SavedSearchResponse(BaseModel):
    id: str
    recruiter_id: str
    name: str
    query: Optional[str] = ""
    job_id: Optional[str] = None
    filters: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CandidateInviteRequest(BaseModel):
    candidate_id: str
    job_id: str
    message: Optional[str] = ""


class BulkInviteRequest(BaseModel):
    candidate_ids: List[str]
    job_id: str
    message: Optional[str] = ""


class CandidateShortlistRequest(BaseModel):
    candidate_id: str
    job_id: Optional[str] = None
    notes: Optional[str] = ""


class BulkShortlistRequest(BaseModel):
    candidate_ids: List[str]
    job_id: Optional[str] = None
