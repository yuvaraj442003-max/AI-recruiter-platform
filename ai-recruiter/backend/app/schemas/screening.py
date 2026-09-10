"""
screening.py — Pydantic schemas for AI Candidate Pre-Screening.
Handles API request/response serialization for screening sessions, score breakdowns, and webhooks.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional
import uuid

from pydantic import BaseModel, Field


class ScreeningQuestionResponse(BaseModel):
    id: uuid.UUID
    question: str
    question_type: str
    expected_answer: Optional[str] = None
    weight: float
    sequence: int

    class Config:
        from_attributes = True


class ScreeningAnswerResponse(BaseModel):
    id: uuid.UUID
    screening_question_id: uuid.UUID
    candidate_answer: str
    extracted_value: Optional[str] = None
    ai_score: float
    ai_reason: Optional[str] = None
    answered_at: datetime

    class Config:
        from_attributes = True


class ScreeningResultResponse(BaseModel):
    id: uuid.UUID
    technical_score: float
    experience_score: float
    location_score: float
    salary_score: float
    availability_score: float
    communication_score: float
    overall_score: float
    recommendation: str
    ai_summary: Optional[str] = None
    recruiter_override: Optional[str] = None
    override_reason: Optional[str] = None

    class Config:
        from_attributes = True


class ScreeningSessionResponse(BaseModel):
    id: uuid.UUID
    application_id: uuid.UUID
    candidate_id: uuid.UUID
    job_id: uuid.UUID
    recruiter_id: uuid.UUID
    status: str
    channel: str
    current_question_index: int
    total_questions: int
    screening_score: Optional[float] = None
    recommendation: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ScreeningSessionDetailResponse(ScreeningSessionResponse):
    questions: List[ScreeningQuestionResponse] = []
    answers: List[ScreeningAnswerResponse] = []
    result: Optional[ScreeningResultResponse] = None


class ScreeningConsentRequest(BaseModel):
    whatsapp_opt_in: bool = True
    sms_opt_in: bool = True
    voice_opt_in: bool = True
    opted_out_all: bool = False
    opt_out_reason: Optional[str] = None


class ScreeningConsentResponse(BaseModel):
    candidate_id: uuid.UUID
    whatsapp_opt_in: bool
    sms_opt_in: bool
    voice_opt_in: bool
    opted_out_all: bool

    class Config:
        from_attributes = True


class CandidateAnswerSubmission(BaseModel):
    answer: str = Field(..., min_length=1, description="Raw candidate reply")
