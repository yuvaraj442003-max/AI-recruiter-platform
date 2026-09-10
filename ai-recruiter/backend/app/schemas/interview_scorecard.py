"""
interview_scorecard.py — Schemas for AI Executive Candidate Scorecard & Interview Intelligence.
"""
import uuid
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class InterviewScoreCategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    category: str
    score: float
    confidence: str
    weight: float
    evidence_summary: Optional[str] = None


class InterviewKeyMomentOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    timestamp_start: int
    timestamp_end: int
    title: str
    category: str
    importance: str
    summary: str
    transcript_reference: Optional[str] = None
    confidence: float


class InterviewChapterOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    timestamp_start: int
    timestamp_end: int
    summary: Optional[str] = None
    sequence: int


class InterviewQuestionEvaluationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    question_id: Optional[uuid.UUID] = None
    question_text: str
    candidate_answer: str
    technical_score: float
    accuracy_score: float
    completeness_score: float
    clarity_score: float
    relevance_score: float
    overall_score: float
    evaluation_summary: Optional[str] = None
    timestamp_start: Optional[int] = None
    timestamp_end: Optional[int] = None


class RecruiterDecisionUpdate(BaseModel):
    decision: str = Field(..., description="Strong Candidate, Shortlist, Hold, or Reject")
    notes: Optional[str] = Field(default=None, description="Optional recruiter notes")


class InterviewScorecardOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    interview_id: uuid.UUID
    candidate_id: uuid.UUID
    job_id: uuid.UUID
    candidate_name: Optional[str] = None
    job_title: Optional[str] = None
    overall_score: float
    recommendation: str
    executive_summary: Optional[str] = None
    confidence: str
    strengths: List[str] = []
    weaknesses: List[str] = []
    recruiter_decision: Optional[str] = None
    recruiter_notes: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    categories: List[InterviewScoreCategoryOut] = []
    key_moments: List[InterviewKeyMomentOut] = []
    chapters: List[InterviewChapterOut] = []
    question_evaluations: List[InterviewQuestionEvaluationOut] = []
    created_at: datetime
