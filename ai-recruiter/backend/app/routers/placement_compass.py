"""
placement_compass.py — API Router for Placement Compass Suite.
Inspired by AdmissionCompass.in, customized for campus placements, recruitment prediction,
and multi-offer career planning.
"""
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from pydantic import BaseModel

from app.core.deps import get_optional_user
from app.models.user import User
from app.schemas.common import APIResponse
from app.schemas.placement_compass import (
    CompanyComparisonRequest,
    CompanyComparisonResponse,
    CompanyItem,
    CompanyPredictionRequest,
    CompanyPredictionResponse,
    DocumentChecklistResponse,
    MockTestEntry,
    MockTrajectoryResponse,
    PlacementDriveEvent,
    SchoolCareerPath,
    CareerRecommendationRequest,
    CareerRecommendationResponse,
    CareerPathComparisonRequest,
    CareerPathComparisonResponse,
    SchoolEntranceExamEvent,
    CareerPositionItem,
    TopCollegeItem,
    CollegeComparisonRequest,
    CollegeComparisonResponse,
    CourseComparisonItem,
    CourseComparisonRequest,
    CourseComparisonResponse,
)
from app.services import placement_compass_service

router = APIRouter(prefix="/placement-compass", tags=["Placement Compass Suite"])


class DocumentToggleRequest(BaseModel):
    doc_id: str
    is_ready: bool


@router.post("/predict", response_model=APIResponse[CompanyPredictionResponse])
def predict_company_chances(
    req: CompanyPredictionRequest,
    current_user: Optional[User] = Depends(get_optional_user),
):
    """Predicts Safe, Target, and Dream companies based on CGPA, aptitude and coding skills."""
    res = placement_compass_service.predict_company_matches(
        cgpa=req.cgpa,
        aptitude_score=req.aptitude_score,
        coding_level=req.coding_level,
        branch=req.branch,
        target_role=req.target_role,
    )
    return APIResponse(
        success=True,
        message="Placement predictor evaluation completed successfully",
        data=CompanyPredictionResponse(**res),
    )


@router.get("/companies", response_model=APIResponse[List[Dict[str, Any]]])
def get_benchmark_companies():
    """Returns all benchmark companies for selection and 3-way matrix comparison."""
    comps = placement_compass_service.list_all_companies()
    return APIResponse(
        success=True,
        message="Benchmark company directory fetched",
        data=comps,
    )


@router.post("/compare", response_model=APIResponse[CompanyComparisonResponse])
def compare_selected_companies(req: CompanyComparisonRequest):
    """Generates side-by-side comparison matrix for up to 3 companies."""
    if len(req.company_ids) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please select at least 2 companies to compare.",
        )
    companies = placement_compass_service.compare_companies(req.company_ids)
    return APIResponse(
        success=True,
        message="Side-by-side company matrix generated",
        data=CompanyComparisonResponse(companies=companies),
    )


@router.get("/drives", response_model=APIResponse[List[PlacementDriveEvent]])
def get_upcoming_placement_drives():
    """Returns active and upcoming placement drives with Google Calendar sync URLs."""
    drives = placement_compass_service.get_placement_drives()
    return APIResponse(
        success=True,
        message="Placement drive timeline loaded",
        data=[PlacementDriveEvent(**d) for d in drives],
    )


@router.get("/drives/{drive_id}/ics")
def download_placement_drive_ics(drive_id: str):
    """Generates an RFC 5545 .ics calendar invite for one-click import into Outlook/Apple Calendar."""
    drives = placement_compass_service.get_placement_drives()
    drive = next((d for d in drives if d["id"] == drive_id), None)
    if not drive:
        raise HTTPException(status_code=404, detail="Placement drive event not found")

    dt_str = drive["event_date"].replace("-", "")
    ics_body = (
        "BEGIN:VCALENDAR\r\n"
        "VERSION:2.0\r\n"
        "PRODID:-//AI Recruiter Platform//Placement Compass//EN\r\n"
        "CALSCALE:GREGORIAN\r\n"
        "METHOD:PUBLISH\r\n"
        "BEGIN:VEVENT\r\n"
        f"UID:{drive['id']}@airecruiter.local\r\n"
        f"SUMMARY:Placement Drive: {drive['company_name']} ({drive['role_title']})\r\n"
        f"DESCRIPTION:{drive['description']}\\nCTC: {drive['ctc']}\\nEligibility: {drive['eligibility_criteria']}\r\n"
        f"DTSTART:{dt_str}T090000Z\r\n"
        f"DTEND:{dt_str}T130000Z\r\n"
        "LOCATION:Campus Placement Portal / Online OA\r\n"
        "STATUS:CONFIRMED\r\n"
        "END:VEVENT\r\n"
        "END:VCALENDAR\r\n"
    )

    return Response(
        content=ics_body,
        media_type="text/calendar",
        headers={
            "Content-Disposition": f"attachment; filename=\"{drive['ics_download_filename']}\""
        },
    )


@router.get("/mock-tests", response_model=APIResponse[MockTrajectoryResponse])
def get_mock_test_trajectory(current_user: Optional[User] = Depends(get_optional_user)):
    """Returns candidate's mock test score progression and cleared company benchmarks."""
    candidate_id = str(current_user.id) if current_user else "default_candidate"
    trajectory = placement_compass_service.get_candidate_mock_trajectory(candidate_id)
    return APIResponse(
        success=True,
        message="Mock trajectory history loaded",
        data=MockTrajectoryResponse(**trajectory),
    )


@router.post("/mock-tests", response_model=APIResponse[MockTrajectoryResponse])
def log_mock_test_score(
    entry: MockTestEntry,
    current_user: Optional[User] = Depends(get_optional_user),
):
    """Logs a new mock test score and recalculates readiness benchmarks."""
    candidate_id = str(current_user.id) if current_user else "default_candidate"
    updated = placement_compass_service.add_candidate_mock_test(candidate_id, entry.model_dump())
    return APIResponse(
        success=True,
        message="Mock test attempt recorded successfully",
        data=MockTrajectoryResponse(**updated),
    )


@router.get("/documents", response_model=APIResponse[DocumentChecklistResponse])
def get_document_checklist(current_user: Optional[User] = Depends(get_optional_user)):
    """Returns candidate pre-placement and BGV document readiness checklist."""
    candidate_id = str(current_user.id) if current_user else "default_candidate"
    res = placement_compass_service.get_candidate_document_checklist(candidate_id)
    return APIResponse(
        success=True,
        message="Document readiness checklist loaded",
        data=DocumentChecklistResponse(**res),
    )


@router.post("/documents/toggle", response_model=APIResponse[DocumentChecklistResponse])
def toggle_document_status(
    req: DocumentToggleRequest,
    current_user: Optional[User] = Depends(get_optional_user),
):
    """Toggles status of a document item in the candidate's pre-placement vault."""
    candidate_id = str(current_user.id) if current_user else "default_candidate"
    res = placement_compass_service.toggle_candidate_document_status(candidate_id, req.doc_id, req.is_ready)
    return APIResponse(
        success=True,
        message="Document status updated",
        data=DocumentChecklistResponse(**res),
    )


@router.get("/reviews/{company_id}", response_model=APIResponse[Dict[str, Any]])
def get_dual_source_reviews(company_id: str):
    """Returns segregated Reddit/Blind vs Glassdoor/AmbitionBox feedback for a company."""
    insights = placement_compass_service.get_company_review_insights(company_id)
    return APIResponse(
        success=True,
        message="Company review insights loaded",
        data=insights,
    )


# =====================================================================
# SCHOOL CAREER GUIDANCE ENDPOINTS (AFTER 10TH & 12TH)
# =====================================================================

@router.get("/school/paths", response_model=APIResponse[List[SchoolCareerPath]])
def get_school_career_paths(
    category: Optional[str] = Query(None, description="Category filter (engineering, medical, arts_science, diploma_polytechnic, law, agriculture, etc.)"),
    grade_level: Optional[str] = Query(None, description="Grade filter (after_10th, after_12th_pcm, after_12th_pcb, after_12th_commerce, after_12th_arts)")
):
    """Returns directory of school career paths with eligibility, exams, fees & salaries."""
    paths = placement_compass_service.list_school_career_paths(category, grade_level)
    return APIResponse(
        success=True,
        message="School career paths directory retrieved",
        data=[SchoolCareerPath(**p) for p in paths]
    )


@router.get("/school/paths/{path_id}", response_model=APIResponse[SchoolCareerPath])
def get_single_school_career_path(path_id: str):
    """Returns in-depth guide for a specific career path."""
    p = placement_compass_service.get_school_career_path(path_id)
    if not p:
        raise HTTPException(status_code=404, detail="Career pathway not found")
    return APIResponse(
        success=True,
        message="Career pathway details loaded",
        data=SchoolCareerPath(**p)
    )


@router.post("/school/compare", response_model=APIResponse[CareerPathComparisonResponse])
def compare_school_career_paths(req: CareerPathComparisonRequest):
    """Generates side-by-side comparison for 2 or 3 school career paths."""
    if len(req.path_ids) < 2:
        raise HTTPException(status_code=400, detail="Please select at least 2 career paths to compare.")
    paths = placement_compass_service.compare_school_career_paths(req.path_ids)
    return APIResponse(
        success=True,
        message="Career paths comparative matrix generated",
        data=CareerPathComparisonResponse(paths=[SchoolCareerPath(**p) for p in paths])
    )


@router.post("/school/recommend", response_model=APIResponse[CareerRecommendationResponse])
def recommend_school_career_paths(req: CareerRecommendationRequest):
    """AI recommender matching student grade, marks, and interests to ideal career pathways."""
    res = placement_compass_service.recommend_school_career_paths(
        current_grade=req.current_grade,
        percentage=req.percentage,
        interests=req.interests,
        budget_preference=req.budget_preference,
        preferred_location=req.preferred_location
    )
    return APIResponse(
        success=True,
        message="AI career recommendations calculated",
        data=CareerRecommendationResponse(**res)
    )


@router.get("/school/exams", response_model=APIResponse[List[SchoolEntranceExamEvent]])
def get_school_entrance_exams(
    group: Optional[str] = Query(None, description="Filter by student academic group (e.g. computer_science, biology, commerce, arts, vocational, sslc_10th)"),
    stage: Optional[str] = Query(None, description="Filter by qualification stage (after_10th, after_12th)"),
    search: Optional[str] = Query(None, description="Search keyword for exam name, conducting body, degree course, or career"),
    status: Optional[str] = Query(None, description="Filter by application status (open, approaching, upcoming, merit)"),
):
    """Returns calendar of major school entrance exams with 1-click Google Calendar sync, filtered by academic group, stage, search keyword, or application status."""
    exams = placement_compass_service.get_school_entrance_exams_list(group=group, stage=stage, search=search, status=status)
    return APIResponse(
        success=True,
        message="School entrance exams calendar retrieved",
        data=[SchoolEntranceExamEvent(**e) for e in exams]
    )


@router.get("/positions", response_model=APIResponse[List[CareerPositionItem]])
def get_career_positions_directory(
    sector: Optional[str] = Query(None, description="Filter by career sector"),
    stage: Optional[str] = Query(None, description="Filter by qualification stage"),
    group: Optional[str] = Query(None, description="Filter by academic group (e.g. computer_science, biology, commerce, arts, sslc_10th)"),
    search: Optional[str] = Query(None, description="Search term across title, sector, or exams"),
):
    """Returns directory of career positions with all corresponding entrance examinations, optionally filtered by academic group."""
    positions = placement_compass_service.get_all_career_positions(sector=sector, stage=stage, search=search, group=group)
    return APIResponse(
        success=True,
        message="Career positions and entrance examinations retrieved",
        data=[CareerPositionItem(**p) for p in positions]
    )


@router.get("/positions/{position_id}", response_model=APIResponse[CareerPositionItem])
def get_career_position_by_id(position_id: str):
    """Returns comprehensive details for a single career position with all its entrance examinations."""
    pos = placement_compass_service.get_career_position_detail(position_id)
    if not pos:
        raise HTTPException(status_code=404, detail="Career position not found")
    return APIResponse(
        success=True,
        message="Career position details retrieved",
        data=CareerPositionItem(**pos)
    )


# =====================================================================
# TOP COLLEGE & COURSE COMPARISON ENDPOINTS
# =====================================================================

@router.get("/colleges", response_model=APIResponse[List[TopCollegeItem]])
def get_top_colleges(
    category: Optional[str] = Query(None, description="Category filter (engineering, medical, arts_science, polytechnic_diploma, law, agriculture, architecture, design, management, defence_govt)")
):
    """Returns top colleges directory across all 10 major career streams."""
    colleges = placement_compass_service.list_top_colleges(category)
    return APIResponse(
        success=True,
        message="Top colleges directory retrieved",
        data=[TopCollegeItem(**c) for c in colleges]
    )


@router.get("/colleges/{college_id}", response_model=APIResponse[TopCollegeItem])
def get_single_college(college_id: str):
    """Returns detailed profile for a specific premier college or university."""
    c = placement_compass_service.get_top_college(college_id)
    if not c:
        raise HTTPException(status_code=404, detail="College not found")
    return APIResponse(
        success=True,
        message="College profile retrieved",
        data=TopCollegeItem(**c)
    )


@router.post("/colleges/compare", response_model=APIResponse[CollegeComparisonResponse])
def compare_selected_colleges(req: CollegeComparisonRequest):
    """Compares up to 3 colleges on rankings, fees, exams, eligibility, placements & facilities."""
    if len(req.college_ids) < 2:
        raise HTTPException(status_code=400, detail="Please select at least 2 colleges to compare.")
    colleges = placement_compass_service.compare_top_colleges(req.college_ids)
    return APIResponse(
        success=True,
        message="Top colleges side-by-side comparison generated",
        data=CollegeComparisonResponse(colleges=[TopCollegeItem(**c) for c in colleges])
    )


@router.get("/courses", response_model=APIResponse[List[CourseComparisonItem]])
def get_comparable_courses():
    """Returns directory of popular courses for comparison."""
    courses = placement_compass_service.list_comparable_courses()
    return APIResponse(
        success=True,
        message="Comparable courses retrieved",
        data=[CourseComparisonItem(**cr) for cr in courses]
    )


@router.post("/courses/compare", response_model=APIResponse[CourseComparisonResponse])
def compare_selected_courses(req: CourseComparisonRequest):
    """Compares up to 3 courses on duration, eligibility, exams, salary & career opportunities."""
    if len(req.course_ids) < 2:
        raise HTTPException(status_code=400, detail="Please select at least 2 courses to compare.")
    courses = placement_compass_service.compare_courses(req.course_ids)
    return APIResponse(
        success=True,
        message="Courses side-by-side comparison generated",
        data=CourseComparisonResponse(courses=[CourseComparisonItem(**cr) for cr in courses])
    )
