"""
student.py — Pydantic schemas for the College Student Placement & Preparation Ecosystem.
"""
import uuid
from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Student Academic Profile
# ---------------------------------------------------------------------------

class StudentAcademicProfileUpdate(BaseModel):
    is_student: Optional[bool] = True
    college_name: Optional[str] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    graduation_year: Optional[int] = None
    cgpa: Optional[float] = None
    current_semester: Optional[int] = None
    target_role: Optional[str] = None
    twelfth_school: Optional[str] = None
    twelfth_board: Optional[str] = None
    twelfth_year: Optional[int] = None
    twelfth_percentage: Optional[float] = None
    tenth_school: Optional[str] = None
    tenth_board: Optional[str] = None
    tenth_year: Optional[int] = None
    tenth_percentage: Optional[float] = None


class StudentAcademicProfileResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    email: str
    is_student: bool
    college_name: Optional[str] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    graduation_year: Optional[int] = None
    cgpa: Optional[float] = None
    current_semester: Optional[int] = None
    target_role: Optional[str] = None
    headline: Optional[str] = None
    skills: List[str] = []
    resume_path: Optional[str] = None
    portfolio_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    github_url: Optional[str] = None
    twelfth_school: Optional[str] = None
    twelfth_board: Optional[str] = None
    twelfth_year: Optional[int] = None
    twelfth_percentage: Optional[float] = None
    tenth_school: Optional[str] = None
    tenth_board: Optional[str] = None
    tenth_year: Optional[int] = None
    tenth_percentage: Optional[float] = None


class StudentReadinessStats(BaseModel):
    overall_readiness_score: int = Field(..., description="0-100 composite placement readiness")
    aptitude_score_avg: float
    tests_completed: int
    coding_challenges_completed: int
    mock_interviews_completed: int
    roadmap_progress_percentage: float
    streak_days: int
    weak_areas: List[str] = []
    strong_areas: List[str] = []
    recommended_actions: List[Dict[str, str]] = []


# ---------------------------------------------------------------------------
# Aptitude Preparation & Practice Tests
# ---------------------------------------------------------------------------

class AptitudeTopicOut(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    description: Optional[str] = None
    icon: str
    question_count: int = 0


class AptitudeTopicCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=150)
    slug: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    icon: str = Field(default="📊", max_length=50)
    order_index: int = Field(default=0)


class AptitudeTopicUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=150)
    slug: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    icon: Optional[str] = Field(None, max_length=50)
    order_index: Optional[int] = None


class AptitudeQuestionCreateStandalone(BaseModel):
    topic_id: Optional[uuid.UUID] = None
    topic_name: Optional[str] = None
    subtopic: str = Field(..., min_length=2, max_length=150)
    question: str = Field(..., min_length=5)
    options: List[str] = Field(..., min_length=4, max_length=4)
    correct_option_index: int = Field(..., ge=0, le=3)
    explanation: Optional[str] = None
    difficulty: str = Field(default="medium")
    marks: float = Field(default=1.0)
    company_tag: Optional[str] = Field(default="General")
    status: str = Field(default="approved")
    check_duplicates: bool = Field(default=True)
    duplicate_threshold: float = Field(default=0.88)


class AptitudeVectorSearchRequest(BaseModel):
    query: str = Field(..., min_length=1)
    limit: int = Field(default=10, ge=1, le=50)
    difficulty: Optional[str] = None
    topic_name: Optional[str] = None
    company_tag: Optional[str] = None
    score_threshold: Optional[float] = None


class AptitudeQuestionTakingOut(BaseModel):
    id: uuid.UUID
    subtopic: str
    question: str
    options: List[str]
    difficulty: str
    company_tag: Optional[str] = None


class AptitudeQuestionReviewOut(BaseModel):
    id: uuid.UUID
    subtopic: str
    question: str
    options: List[str]
    correct_option_index: int
    user_selected_index: Optional[int] = None
    is_correct: bool
    explanation: Optional[str] = None


class AptitudeTestOut(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str] = None
    category: str
    company_name: Optional[str] = None
    duration_minutes: int
    total_questions: int
    passing_percentage: float


class AptitudeSubmissionRequest(BaseModel):
    test_id: Optional[str] = None
    topic_name: Optional[str] = None
    time_taken_seconds: int = 0
    # Map of question_id (string) -> selected_option_index (int or None: 0, 1, 2, 3)
    answers: Dict[str, Optional[int]] = Field(default_factory=dict)
    question_ids: Optional[List[str]] = None


class AptitudeAttemptResult(BaseModel):
    attempt_id: uuid.UUID
    total_questions: int
    correct_count: int
    wrong_count: int
    unanswered_count: int
    score_percentage: float
    time_taken_seconds: int
    is_passed: bool
    feedback_message: str
    percentile_estimate: float
    questions_review: List[AptitudeQuestionReviewOut] = []


# ---------------------------------------------------------------------------
# Study Materials & Learning Roadmaps
# ---------------------------------------------------------------------------

class StudyMaterialListItem(BaseModel):
    id: uuid.UUID
    title: str
    slug: str
    category: str
    content_type: str
    description: Optional[str] = None
    company_tag: Optional[str] = None
    difficulty: str
    estimated_read_time: str
    tags: List[str] = []


class StudyMaterialDetail(StudyMaterialListItem):
    content_markdown: str


class LearningRoadmapOut(BaseModel):
    id: uuid.UUID
    title: str
    slug: str
    role_target: str
    description: Optional[str] = None
    icon: str
    estimated_weeks: int
    milestones: List[Dict[str, Any]]
    progress_percentage: float = 0.0
    completed_milestones: List[str] = []
    scores: Dict[str, Any] = {}


class RoadmapProgressUpdateRequest(BaseModel):
    completed_milestone_ids: List[str]


class MilestoneQuizQuestionOut(BaseModel):
    id: str
    question: str
    options: List[str]
    topic: Optional[str] = None
    difficulty: str = "medium"
    marks: float = 1.0


class MilestoneQuizStartResponse(BaseModel):
    milestone_id: str
    milestone_title: str
    subject: str
    topics: List[str]
    subtopics: List[str] = []
    duration_minutes: int
    total_questions: int
    passing_percentage: float = 60.0
    questions: List[MilestoneQuizQuestionOut]
    session_id: Optional[str] = None


class MilestoneQuizSubmitRequest(BaseModel):
    session_id: Optional[str] = None
    answers: Dict[str, int] = {}  # question_id -> selected_option_index (0..3)
    time_taken_seconds: int = 0


class MilestoneQuizReviewItem(BaseModel):
    question_id: str
    question: str
    options: List[str]
    correct_option_index: int
    user_selected_index: Optional[int] = None
    is_correct: bool
    explanation: Optional[str] = None


class MilestoneQuizResultResponse(BaseModel):
    milestone_id: str
    milestone_title: str
    total_questions: int
    correct_count: int
    wrong_count: int
    unanswered_count: int
    score: float
    total_marks: float
    percentage: float
    passed: bool
    time_taken_seconds: int
    feedback_message: str
    review_items: List[MilestoneQuizReviewItem]
    is_milestone_completed: bool
    updated_roadmap_progress: float


class AvailableTopicItem(BaseModel):
    id: str
    name: str
    category: str
    icon: str
    description: str
    popular: bool = False
    subtopics_preview: List[str] = []


class StudentTopicsPreferenceRequest(BaseModel):
    selected_topics: List[str]
    custom_topics: List[str] = []


class StudentTopicsPreferenceResponse(BaseModel):
    selected_topics: List[str]
    custom_topics: List[str]
    all_active_topics: List[str]
    daily_streak: int = 1
    last_assessment_date: Optional[str] = None
    total_assessments_taken: int = 0


class DailyAssessmentStartResponse(BaseModel):
    assessment_id: str
    session_id: str
    date_str: str
    topics_covered: List[str]
    duration_minutes: int
    total_questions: int
    passing_percentage: float = 60.0
    questions: List[MilestoneQuizQuestionOut]


class DailyAssessmentSubmitRequest(BaseModel):
    session_id: str
    answers: Dict[str, int] = {}
    time_taken_seconds: int = 0


class DailyAssessmentResultResponse(BaseModel):
    assessment_id: str
    total_questions: int
    correct_count: int
    wrong_count: int
    unanswered_count: int
    score: float
    total_marks: float
    percentage: float
    passed: bool
    daily_streak: int
    time_taken_seconds: int
    feedback_message: str
    topics_covered: List[str]
    review_items: List[MilestoneQuizReviewItem]


class PersonalizedLearningFeedResponse(BaseModel):
    selected_topics: List[str]
    custom_topics: List[str]
    matched_materials: List[StudyMaterialListItem]
    practice_questions_sample: List[MilestoneQuizQuestionOut]
    active_filter_topic: Optional[str] = None
    featured_guide_slug: Optional[str] = None


# ---------------------------------------------------------------------------
# Recruiter Student Career Guidance & Learning Activity Monitoring Schemas
# ---------------------------------------------------------------------------

class StudentAptitudeAttemptItem(BaseModel):
    id: str
    title: str
    score_percentage: float
    is_passed: bool
    total_questions: int
    correct_count: int
    wrong_count: int
    time_taken_seconds: int
    date: str


class StudentLearningMonitorItem(BaseModel):
    user_id: str
    name: str
    email: str
    college_name: str
    degree: str
    branch: str
    graduation_year: Optional[int] = None
    cgpa: Optional[float] = None
    target_role: str
    preparing_topics: List[str] = []
    topics_count: int = 0
    tests_count: int = 0
    avg_score: float = 0.0
    latest_score: float = 0.0
    best_score: float = 0.0
    passed_count: int = 0
    failed_count: int = 0
    pass_rate: float = 0.0
    total_time_spent_mins: float = 0.0
    roadmap_progress: float = 0.0
    roadmaps_enrolled: int = 0
    milestones_completed_count: int = 0
    daily_streak: int = 0
    last_active_date: Optional[str] = None
    is_consistent: bool = False
    consistency_label: str = "Needs Engagement"
    consistency_badge: str = "secondary"
    trend: str = "none"  # "improving" | "declining" | "steady" | "none"
    trend_label: str = "Not Started"
    trend_badge: str = "secondary"
    performance_status: str = "Needs Improvement"  # "Performing Well" | "Moderate Progress" | "Needs Improvement"
    status_badge: str = "danger"
    rating_stars: str = "⭐"
    weak_areas: List[str] = []
    strong_areas: List[str] = []
    recent_attempts: List[StudentAptitudeAttemptItem] = []


class RecruiterStudentMonitorSummary(BaseModel):
    total_students: int = 0
    active_learners_count: int = 0
    avg_aptitude_score: float = 0.0
    avg_roadmap_progress: float = 0.0
    performing_well_count: int = 0
    moderate_count: int = 0
    needs_improvement_count: int = 0
    consistent_learners_count: int = 0
    top_preparing_topics: List[Dict[str, Any]] = []


class RecruiterStudentMonitorResponse(BaseModel):
    summary: RecruiterStudentMonitorSummary
    students: List[StudentLearningMonitorItem]


