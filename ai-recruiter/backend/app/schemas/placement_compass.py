"""
placement_compass.py — Pydantic Schemas for Placement Compass Suite.
Inspired by AdmissionCompass.in tailored for campus placements & recruitment.
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class CompanyPredictionRequest(BaseModel):
    cgpa: float = Field(..., ge=0.0, le=10.0, description="Candidate CGPA (out of 10)")
    aptitude_score: float = Field(..., ge=0.0, le=100.0, description="Current aptitude percentage (0-100)")
    coding_level: str = Field("intermediate", description="Coding level: beginner, intermediate, advanced")
    branch: Optional[str] = Field("Computer Science / IT", description="Degree branch")
    target_role: Optional[str] = Field("Software Engineer", description="Target role")


class CompanyItem(BaseModel):
    id: str
    name: str
    category: str  # "dream", "target", "safe"
    logo_emoji: str
    industry: str
    ctc_range: str
    min_cgpa: float
    min_aptitude: float
    difficulty: str  # "High", "Medium", "Moderate"
    hiring_status: str
    rounds_count: int
    interview_rounds: List[str]
    core_skills: List[str]
    match_percentage: int
    skill_gaps: List[str]
    locations: List[str]


class CompanyPredictionResponse(BaseModel):
    candidate_cgpa: float
    candidate_aptitude: float
    total_evaluated: int
    safe_matches: List[CompanyItem]
    target_matches: List[CompanyItem]
    dream_matches: List[CompanyItem]
    summary_guidance: str


class CompanyComparisonRequest(BaseModel):
    company_ids: List[str] = Field(..., min_items=2, max_items=3)


class CompensationBreakdown(BaseModel):
    total_ctc: str
    base_salary: str
    variable_bonus: str
    joining_bonus: str
    stocks_esops: str


class ComparisonCompanyDetail(BaseModel):
    id: str
    name: str
    logo_emoji: str
    tier: str
    compensation: CompensationBreakdown
    work_policy: str
    selection_process: Dict[str, Any]
    tech_stack: List[str]
    culture_rating: float
    work_life_balance: float
    pros: List[str]
    cons: List[str]
    reddit_summary: str
    glassdoor_summary: str


class CompanyComparisonResponse(BaseModel):
    companies: List[ComparisonCompanyDetail]


class PlacementDriveEvent(BaseModel):
    id: str
    company_name: str
    logo_emoji: str
    role_title: str
    ctc: str
    drive_type: str  # "Campus Drive", "National OA", "Off-Campus Slot"
    event_date: str
    event_time: str
    registration_deadline: str
    eligibility_criteria: str
    google_calendar_url: str
    ics_download_filename: str
    description: str


class MockTestEntry(BaseModel):
    id: Optional[str] = None
    test_name: str
    date: str
    quantitative_score: float
    logical_score: float
    verbal_score: float
    technical_score: Optional[float] = 0.0
    total_percentage: float
    max_score: float = 100.0
    notes: Optional[str] = ""


class MockTrajectoryResponse(BaseModel):
    total_attempts: int
    average_score: float
    latest_score: float
    highest_score: float
    readiness_level: str
    company_benchmarks_cleared: List[str]
    attempts: List[MockTestEntry]


class DocumentChecklistItem(BaseModel):
    id: str
    title: str
    description: str
    is_ready: bool
    importance: str  # "Critical", "Important", "Recommended"
    category: str  # "Academics", "Identity", "Portfolio", "Legal"


class DocumentChecklistResponse(BaseModel):
    total_documents: int
    ready_count: int
    readiness_percentage: float
    checklist: List[DocumentChecklistItem]


# =====================================================================
# SCHOOL STUDENT CAREER GUIDANCE SCHEMAS (AFTER 10TH & 12TH)
# =====================================================================

class ExamItem(BaseModel):
    name: str
    level: str  # "National", "State", "University"
    official_portal: Optional[str] = ""
    description: Optional[str] = ""


class SchoolCareerPath(BaseModel):
    id: str
    title: str
    category: str  # "engineering", "medical", "arts_science", "diploma_polytechnic", "law", "agriculture", "architecture", "design", "management", "defence", "govt_jobs"
    grade_level: str  # "after_10th", "after_12th_pcm", "after_12th_pcb", "after_12th_commerce", "after_12th_arts", "after_10th_or_12th"
    icon_emoji: str
    tagline: str
    duration: str
    eligibility: str
    entrance_exams: List[ExamItem]
    top_colleges: List[str]
    admission_procedure: str
    estimated_fees: Dict[str, str]
    scholarships: List[str]
    career_opportunities: List[str]
    starting_salary_range: str
    future_study_options: List[str]
    key_skills_needed: List[str]


class CareerRecommendationRequest(BaseModel):
    current_grade: str = Field(..., description="'10th', '12th_pcm', '12th_pcb', '12th_commerce', '12th_arts'")
    percentage: float = Field(..., ge=30.0, le=100.0, description="Marks / Percentage obtained or expected")
    interests: List[str] = Field(default_factory=list, description="List of interest tags, e.g. ['coding', 'healthcare']")
    budget_preference: Optional[str] = "any"  # "govt_merit", "budget_friendly", "any"
    preferred_location: Optional[str] = "All India"


class CareerRecommendationItem(BaseModel):
    path: SchoolCareerPath
    match_percentage: int
    fit_reasons: List[str]
    action_plan: List[str]


class CareerRecommendationResponse(BaseModel):
    current_grade: str
    percentage: float
    total_matches: int
    top_recommendations: List[CareerRecommendationItem]
    stream_guidance: str


class CareerPathComparisonRequest(BaseModel):
    path_ids: List[str] = Field(..., min_items=2, max_items=3)


class CareerPathComparisonResponse(BaseModel):
    paths: List[SchoolCareerPath]


class SchoolEntranceExamEvent(BaseModel):
    id: str
    exam_name: str
    target_courses: List[str]
    conducting_body: str
    registration_start: str
    registration_deadline: str
    exam_date: str
    official_url: str
    google_calendar_url: str
    eligibility_summary: str
    syllabus_highlights: str
    target_stage: Optional[str] = None
    stage_badge: Optional[str] = None
    admission_type: Optional[str] = None
    model_config = {"extra": "allow"}


class RelevantExamDetail(BaseModel):
    exam_name: str
    exam_category: str
    conducting_body: str
    selection_stages: str
    official_portal: str
    registration_window: str
    exam_date: str
    exam_pattern: str
    how_to_prepare: str
    model_config = {"extra": "allow"}


class CareerPositionItem(BaseModel):
    id: str
    position_title: str
    sector: str
    qualification_stage: str
    qualification_badge: str
    position_description: str
    salary_range: str
    recruiting_organizations: List[str]
    relevant_entrance_exams: List[Dict[str, Any]]
    future_career_growth: List[str]
    government_perks_quotas: str
    model_config = {"extra": "allow"}



# =====================================================================
# TOP COLLEGE COMPARISON SCHEMAS
# =====================================================================

class CollegePlacementStats(BaseModel):
    highest_package: str
    average_package: str
    median_package: str
    placement_percentage: str
    top_recruiters: List[str]


class CollegeExamSchedule(BaseModel):
    application_start: str
    last_date: str
    exam_date: str
    result_date: str


class TopCollegeItem(BaseModel):
    id: str
    name: str
    category: str  # "engineering", "medical", "arts_science", "polytechnic_diploma", "law", "agriculture", "architecture", "design", "management", "defence_govt"
    logo_emoji: str
    location: str
    nirf_ranking: str
    accreditation: str
    flagship_courses: List[str]
    eligibility_criteria: str
    entrance_exams: List[str]
    exam_schedule: CollegeExamSchedule
    admission_counselling_process: str
    tuition_fees_per_year: str
    hostel_mess_fees_per_year: str
    scholarships_available: List[str]
    placement_stats: CollegePlacementStats
    campus_facilities: List[str]
    pros: List[str]
    cons: List[str]


class CollegeComparisonRequest(BaseModel):
    college_ids: List[str] = Field(..., min_items=2, max_items=3)


class CollegeComparisonResponse(BaseModel):
    colleges: List[TopCollegeItem]


class CourseComparisonItem(BaseModel):
    id: str
    course_name: str
    category: str
    duration: str
    eligibility: str
    entrance_exams: List[str]
    avg_starting_salary: str
    top_roles: List[str]
    future_scopes: List[str]
    why_choose: str


class CourseComparisonRequest(BaseModel):
    course_ids: List[str] = Field(..., min_items=2, max_items=3)


class CourseComparisonResponse(BaseModel):
    courses: List[CourseComparisonItem]
