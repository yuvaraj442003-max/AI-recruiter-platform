"""
coding.py — Pydantic schemas for questions, test cases, coding assessments,
attempts, code execution runs, submissions, and evaluation reports.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


# --- Test Cases ---
class CodingTestCaseCreate(BaseModel):
    input_data: str
    expected_output: str
    is_hidden: bool = False
    points: int = 10


class CodingTestCaseResponse(BaseModel):
    id: UUID
    question_id: UUID
    input_data: Optional[str] = None
    expected_output: Optional[str] = None
    is_hidden: bool
    points: int

    class Config:
        from_attributes = True


# --- Questions ---
class CodingQuestionCreate(BaseModel):
    title: str
    description: str
    difficulty: str = "Medium"  # Easy, Medium, Hard
    category: str = "Algorithms"
    programming_languages: List[str] = ["python", "javascript", "java", "cpp", "csharp"]
    starter_code: Optional[Dict[str, str]] = None
    expected_output: Optional[str] = None
    constraints: Optional[str] = None
    explanation: Optional[str] = None
    test_cases: List[CodingTestCaseCreate] = []


class CodingQuestionResponse(BaseModel):
    id: UUID
    title: str
    description: str
    difficulty: str
    category: str
    programming_languages: List[str] = []
    starter_code: Dict[str, str] = {}
    expected_output: Optional[str] = None
    constraints: Optional[str] = None
    explanation: Optional[str] = None
    test_cases: List[CodingTestCaseResponse] = []
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Assessments ---
class AssessmentQuestionItem(BaseModel):
    question_id: UUID
    question_order: int = 1
    points: float = 20.0


class CodingAssessmentCreate(BaseModel):
    job_id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    duration_minutes: int = 60
    passing_score: float = 60.0
    total_score: float = 100.0
    max_attempts: int = 1
    allowed_languages: List[str] = ["python", "javascript", "java", "cpp", "csharp"]
    questions: List[AssessmentQuestionItem] = []


class CodingAssessmentResponse(BaseModel):
    id: UUID
    job_id: Optional[UUID] = None
    title: str
    description: Optional[str] = None
    duration_minutes: int
    passing_score: float
    total_score: float
    max_attempts: int
    allowed_languages: List[str] = []
    questions: List[Dict[str, Any]] = []
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# --- Execution & Submissions ---
class RunCodeRequest(BaseModel):
    question_id: UUID
    language: str
    source_code: str


class RunCodeResponse(BaseModel):
    status: str
    passed: int
    total: int
    execution_time: float
    output: Optional[str] = None
    test_case_details: List[Dict[str, Any]] = []


class SubmitCodeRequest(BaseModel):
    question_id: UUID
    language: str
    source_code: str


# --- Attempts & Results ---
class CandidateCodingAttemptResponse(BaseModel):
    id: UUID
    candidate_id: UUID
    assessment_id: UUID
    status: str
    started_at: Optional[datetime] = None
    submitted_at: Optional[datetime] = None
    score: Optional[float] = None
    percentage: Optional[float] = None
    passed: bool = False
    time_taken: Optional[int] = None
    remaining_seconds: Optional[int] = None
    assessment: Optional[CodingAssessmentResponse] = None

    class Config:
        from_attributes = True


class CodingResultReportResponse(BaseModel):
    attempt_id: UUID
    candidate_id: UUID
    candidate_name: str
    assessment_id: UUID
    assessment_title: str
    job_id: Optional[UUID] = None
    status: str
    started_at: Optional[datetime] = None
    submitted_at: Optional[datetime] = None
    time_taken_minutes: Optional[float] = None
    duration_minutes: int
    score: float
    percentage: float
    passing_score: float
    passed: bool
    ats_score: Optional[float] = None
    coding_score: Optional[float] = None
    interview_score: Optional[float] = None
    overall_score: Optional[float] = None
    submissions: List[Dict[str, Any]] = []
