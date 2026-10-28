"""
weekly_challenge.py — Pydantic schemas for weekly aptitude & coding challenges,
runner requests, submissions, leaderboards, and admin management.
"""
import uuid
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class WeeklyAptitudeQuestionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    subtopic: str
    question: str
    options: List[str]
    difficulty: str
    company_tag: Optional[str] = None


class WeeklyAptitudeQuestionReviewOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    subtopic: str
    question: str
    options: List[str]
    correct_option_index: int
    user_selected_index: Optional[int] = None
    is_correct: bool
    explanation: Optional[str] = None


class WeeklyAptitudeSetOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    week_code: str
    year: int
    week_number: int
    title: str
    description: Optional[str] = None
    duration_minutes: int
    passing_percentage: float
    total_questions: int
    is_active: bool
    user_completed: bool = False
    user_score_percentage: Optional[float] = None
    user_passed: Optional[bool] = None


class WeeklyAptitudeSubmissionRequest(BaseModel):
    answers: Dict[str, Optional[int]] = Field(default_factory=dict, description="Mapping of question UUID strings to selected option index (0-3)")
    time_taken_seconds: int = 0
    is_anonymous: bool = False


class WeeklyAptitudeAttemptResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    attempt_id: uuid.UUID
    week_code: str
    total_questions: int
    correct_count: int
    wrong_count: int
    unanswered_count: int
    score_percentage: float
    time_taken_seconds: int
    is_passed: bool
    feedback_message: str
    percentile_estimate: float
    questions_review: List[WeeklyAptitudeQuestionReviewOut] = []


class WeeklyCodingQuestionItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    description: str
    difficulty: str
    category: str
    starter_code: Optional[Dict[str, str]] = None
    expected_output: Optional[str] = None
    constraints: Optional[str] = None
    public_test_cases: List[Dict[str, Any]] = []


class WeeklyCodingChallengeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    week_code: str
    year: int
    week_number: int
    title: str
    description: Optional[str] = None
    duration_minutes: int
    passing_score: float
    total_score: float
    difficulty: str
    allowed_languages: List[str]
    questions: List[WeeklyCodingQuestionItem] = []
    user_completed: bool = False
    user_score: Optional[float] = None
    user_passed: Optional[bool] = None


class WeeklyCodingRunRequest(BaseModel):
    question_id: str
    language: str
    source_code: str


class WeeklyCodingSubmitRequest(BaseModel):
    submissions: Dict[str, Dict[str, str]] = Field(
        ...,
        description="Map of question_id -> { 'language': str, 'source_code': str }"
    )
    time_taken_seconds: int = 0
    is_anonymous: bool = False


class LeaderboardEntry(BaseModel):
    rank: int
    candidate_name: str
    is_current_user: bool = False
    score: float
    time_taken_seconds: int
    is_passed: bool
    completed_at: Optional[str] = None


class WeeklyLeaderboardResponse(BaseModel):
    week_code: str
    challenge_type: str  # "aptitude" or "coding"
    total_participants: int
    current_user_rank: Optional[int] = None
    entries: List[LeaderboardEntry] = []


class WeeklyScheduleStatusOut(BaseModel):
    current_week_code: str
    week_label: str
    cadence: str
    next_update_utc: str
    days_remaining: int
    hours_remaining: int
    status_badge: str
    is_active_this_week: bool
    total_coding_topics: int = 12
    total_coding_problems: int = 0
    total_aptitude_topics: int = 16
    total_aptitude_questions: int = 0
    aptitude_weekly_focus: Optional[Dict[str, Any]] = None


class ProgrammingTopicOut(BaseModel):
    id: str
    slug: str
    name: str
    category: str
    icon: str
    description: str
    popular: bool = False
    language: str = "dsa"  # "java", "python", "dsa"
    study_guide_slug: Optional[str] = None
    subtopics: List[str] = []
    problem_count: int = 0
    difficulty_distribution: Dict[str, int] = Field(default_factory=dict)


class AptitudePreparationTopicOut(BaseModel):
    id: str
    slug: str
    name: str
    icon: str
    description: str
    subtopics: List[str] = []
    company_focus: List[str] = []
    question_count: int = 0
    section: Optional[str] = None
    chapters: Optional[str] = None
    chapter_ref: Optional[str] = None
    is_current_week: bool = False
    scheduled_week: Optional[str] = None


class WeeklyOverviewResponse(BaseModel):
    current_week_code: str
    week_label: str
    aptitude: Optional[WeeklyAptitudeSetOut] = None
    coding: Optional[WeeklyCodingChallengeOut] = None
    overall_readiness_pct: float = 0.0
    schedule: Optional[WeeklyScheduleStatusOut] = None
    coding_topics_summary: List[Dict[str, Any]] = Field(default_factory=list)
    aptitude_topics_summary: List[Dict[str, Any]] = Field(default_factory=list)
    aptitude_weekly_focus: Optional[Dict[str, Any]] = None


# Admin schemas for question management
class AptitudeQuestionAdminCreate(BaseModel):
    topic_slug: str = "quantitative-aptitude"
    subtopic: str
    question: str
    options: List[str]
    correct_option_index: int
    explanation: Optional[str] = None
    difficulty: str = "medium"  # easy, medium, hard
    company_tag: Optional[str] = "General"
    status: str = "approved"  # approved, pending_review


class AptitudeQuestionAdminUpdate(BaseModel):
    subtopic: Optional[str] = None
    question: Optional[str] = None
    options: Optional[List[str]] = None
    correct_option_index: Optional[int] = None
    explanation: Optional[str] = None
    difficulty: Optional[str] = None
    company_tag: Optional[str] = None
    status: Optional[str] = None


class CodingQuestionAdminCreate(BaseModel):
    title: str
    description: str
    difficulty: str = "Medium"  # Easy, Medium, Hard
    category: str = "Algorithms"
    programming_languages: List[str] = ["python", "javascript", "java", "cpp"]
    starter_code: Optional[Dict[str, str]] = None
    constraints: Optional[str] = None
    explanation: Optional[str] = None
    status: str = "approved"
    public_test_cases: List[Dict[str, Any]] = []
    hidden_test_cases: List[Dict[str, Any]] = []


class CodingQuestionAdminUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    difficulty: Optional[str] = None
    category: Optional[str] = None
    programming_languages: Optional[List[str]] = None
    starter_code: Optional[Dict[str, str]] = None
    constraints: Optional[str] = None
    explanation: Optional[str] = None
    status: Optional[str] = None
