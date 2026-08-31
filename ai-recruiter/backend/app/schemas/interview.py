"""
Schemas for the interview flow: creation, questions, answers, and the
final report.
"""
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.interview import InterviewStatus, InterviewType


class InterviewCreate(BaseModel):
    candidate_id: uuid.UUID
    job_id: uuid.UUID
    interview_type: InterviewType = InterviewType.mixed
    num_questions: int = Field(default=6, ge=1, le=15)


class InterviewQuestionOut(BaseModel):
    id: uuid.UUID
    question: str
    question_type: str
    difficulty: str
    expected_topics: list[str] = []
    order_number: int
    answered: bool = False
    # Only populated for the recruiter/report view, not while a candidate is mid-interview.
    answer_text: Optional[str] = None
    answer_score: Optional[float] = None


class InterviewResponse(BaseModel):
    id: uuid.UUID
    candidate_id: uuid.UUID
    job_id: uuid.UUID
    candidate_name: Optional[str] = None
    job_title: Optional[str] = None
    interview_type: InterviewType
    status: InterviewStatus
    overall_score: Optional[float] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    questions: list[InterviewQuestionOut] = []


class AnswerSubmit(BaseModel):
    question_id: uuid.UUID
    answer_text: str = Field(min_length=1, max_length=8000)


class AnswerResponse(BaseModel):
    id: uuid.UUID
    question_id: uuid.UUID
    answer_text: str
    answer_source: str
    answer_score: Optional[float] = None
    strengths: list[str] = []
    improvements: list[str] = []
    interview_status: InterviewStatus


class TranscriptionResponse(BaseModel):
    text: str


class ReportQuestionAnswer(BaseModel):
    question: str
    type: str
    difficulty: str
    expected_topics: list[str] = []
    answer_text: Optional[str] = None
    answer_score: Optional[float] = None
    strengths: list[str] = []
    improvements: list[str] = []


class ReportEvaluation(BaseModel):
    technical_score: Optional[float] = None
    communication_score: Optional[float] = None
    relevance_score: Optional[float] = None
    problem_solving_score: Optional[float] = None
    overall_score: Optional[float] = None
    strengths: list[str] = []
    weaknesses: list[str] = []
    recommendation: Optional[str] = None
    source: Optional[str] = None


class InterviewReport(BaseModel):
    interview_id: uuid.UUID
    candidate_name: Optional[str] = None
    job_title: Optional[str] = None
    status: InterviewStatus
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    questions: list[ReportQuestionAnswer] = []
    evaluation: Optional[ReportEvaluation] = None
    human_review_required: bool = True
