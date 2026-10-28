"""
aptitude_generator.py — Pydantic schemas for the AI-Based Aptitude Question Generator,
Test Studio Review, and Candidate Taking/Evaluation.
"""
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator


class AptitudeOptionCreate(BaseModel):
    option_letter: str = Field(..., pattern=r"^[A-D]$", description="Option letter: A, B, C, or D")
    option_text: str = Field(..., min_length=1, description="Option description text")
    is_correct: bool = False


class AptitudeOptionOut(BaseModel):
    id: Optional[uuid.UUID] = None
    option_letter: str
    option_text: str
    is_correct: bool = False
    order_index: int = 0


class AptitudeQuestionGeneratedItem(BaseModel):
    """Schema for AI generator validation."""
    topic_name: str = Field(..., min_length=2, description="Topic name e.g. Percentages")
    subtopic: str = Field(default="Applied Problem Solving")
    question: str = Field(..., min_length=10, description="Full question statement")
    options: List[str] = Field(..., min_length=4, max_length=4, description="Four answer options")
    correct_option_index: int = Field(..., ge=0, le=3, description="Index 0..3 of correct option")
    explanation: str = Field(..., min_length=10, description="Step-by-step mathematical/logical reasoning")
    difficulty: str = Field(default="medium", description="easy, medium, or hard")
    marks: float = Field(default=1.0, ge=0.5, le=10.0)

    @field_validator("options")
    @classmethod
    def validate_unique_options(cls, v: List[str]) -> List[str]:
        cleaned = [opt.strip() for opt in v]
        if len(set(cleaned)) < 3:
            raise ValueError("Options must be distinct choices.")
        return cleaned


class AptitudeGenerateRequest(BaseModel):
    title: str = Field(..., min_length=3, max_length=255, description="Name of the aptitude test")
    topics: List[str] = Field(..., min_length=1, description="List of topics e.g. ['Percentages', 'Time and Work']")
    num_questions: int = Field(default=10, ge=1, le=50, description="5, 10, 20, 30 questions")
    difficulty: str = Field(default="mixed", description="easy, medium, hard, or mixed")
    duration_minutes: Optional[int] = Field(default=None, ge=1, le=180, description="Test duration in minutes")
    marks_per_question: float = Field(default=1.0, ge=0.5, le=10.0, description="Marks per question")

    @field_validator("topics")
    @classmethod
    def validate_topics(cls, v: List[str]) -> List[str]:
        cleaned = [t.strip() for t in v if t and t.strip()]
        if not cleaned:
            raise ValueError("At least one non-empty topic must be provided.")
        return cleaned


class AptitudeQuestionUpdate(BaseModel):
    question: Optional[str] = Field(default=None, min_length=5)
    options: Optional[List[str]] = Field(default=None, min_length=4, max_length=4)
    correct_option_index: Optional[int] = Field(default=None, ge=0, le=3)
    explanation: Optional[str] = None
    difficulty: Optional[str] = None
    topic_name: Optional[str] = None
    marks: Optional[float] = Field(default=None, ge=0.5, le=10.0)


class AptitudeQuestionDetail(BaseModel):
    id: uuid.UUID
    test_id: Optional[uuid.UUID] = None
    topic_name: Optional[str] = None
    subtopic: str
    question: str
    options: List[AptitudeOptionOut]
    correct_option_index: int
    explanation: Optional[str] = None
    difficulty: str
    marks: float
    status: str


class AptitudeTestDetail(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str] = None
    category: str
    topics: List[str] = []
    difficulty: str
    duration_minutes: int
    total_questions: int
    marks_per_question: float
    total_marks: float
    passing_percentage: float
    status: str  # draft, published, archived
    is_active: bool
    created_at: datetime
    questions: List[AptitudeQuestionDetail] = []
    attempts_count: int = 0


class AptitudeTestSummary(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str] = None
    category: str
    topics: List[str] = []
    difficulty: str
    duration_minutes: int
    total_questions: int
    marks_per_question: float
    total_marks: float
    passing_percentage: float
    status: str
    is_active: bool
    created_at: datetime
    attempts_count: int = 0


class CandidateTakingOption(BaseModel):
    id: uuid.UUID
    option_letter: str
    option_text: str


class CandidateTakingQuestion(BaseModel):
    id: uuid.UUID
    question_number: int
    topic_name: Optional[str] = None
    subtopic: str
    question: str
    difficulty: str
    marks: float
    options: List[CandidateTakingOption]


class CandidateTakingTestResponse(BaseModel):
    test_id: uuid.UUID
    attempt_id: uuid.UUID
    title: str
    duration_minutes: int
    total_questions: int
    total_marks: float
    passing_percentage: float
    remaining_seconds: int
    questions: List[CandidateTakingQuestion]


class CandidateAnswerItem(BaseModel):
    question_id: uuid.UUID
    selected_option_id: Optional[uuid.UUID] = None
    selected_option_index: Optional[int] = None
    selected_option_letter: Optional[str] = None


class CandidateAptitudeSubmitRequest(BaseModel):
    attempt_id: uuid.UUID
    answers: List[CandidateAnswerItem] = []
    time_taken_seconds: int = 0


class CandidateAnswerReviewItem(BaseModel):
    question_id: uuid.UUID
    question_text: str
    topic_name: Optional[str] = None
    difficulty: str
    marks: float
    marks_awarded: float
    options: List[AptitudeOptionOut]
    correct_option_letter: str
    user_selected_letter: Optional[str] = None
    is_correct: bool
    explanation: Optional[str] = None


class CandidateTestResultResponse(BaseModel):
    result_id: uuid.UUID
    attempt_id: uuid.UUID
    test_id: uuid.UUID
    test_title: str
    total_questions: int
    correct_count: int
    wrong_count: int
    unanswered_count: int
    score: float
    total_marks: float
    percentage: float
    passed: bool
    time_taken_seconds: int
    percentile_estimate: float
    feedback_message: str
    topic_breakdown: Dict[str, Any] = {}
    review_items: List[CandidateAnswerReviewItem] = []
