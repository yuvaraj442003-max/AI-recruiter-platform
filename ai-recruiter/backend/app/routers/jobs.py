"""
Job endpoints: CRUD (recruiter-owned), browsing/search, applying
(candidate), and viewing ranked applicants (recruiter, owner-only).
"""
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.core.deps import get_current_user, require_role
from app.core.exceptions import NotFoundError, PermissionDeniedError
from app.ai.job_analyzer import analyze_job_description
from app.ai.question_generator import generate_interview_questions
from app.models.application import Application
from app.models.candidate import CandidateProfile, CandidateSkill
from app.models.job import Job, JobSkill, JobStatus
from app.models.user import User, UserRole
from app.schemas.application import ApplicationResponse
from app.schemas.common import APIResponse
from app.schemas.job import (
    JobAnalysisRequest,
    JobAnalysisResponse,
    JobCreate,
    JobResponse,
    JobUpdate,
    QuestionGenerationResponse,
)
from app.services.job_service import apply_to_job, create_job, rank_applicants, update_job

router = APIRouter(prefix="/jobs", tags=["Jobs"])


def _load_job_or_404(db: Session, job_id: str) -> Job:
    try:
        parsed_id = uuid.UUID(job_id)
    except ValueError:
        raise NotFoundError("Job not found")

    job = (
        db.query(Job)
        .options(joinedload(Job.job_skills).joinedload(JobSkill.skill))
        .filter(Job.id == parsed_id)
        .first()
    )
    if not job:
        raise NotFoundError("Job not found")
    return job


@router.post("/analyze", response_model=APIResponse[JobAnalysisResponse])
def analyze_job_description_endpoint(
    payload: JobAnalysisRequest,
    current_user: User = Depends(require_role(UserRole.recruiter)),
):
    """
    Analyzes a free-form job description via the configured LLM (or the
    Phase 2/3 NLP skill extractor as a fallback) so the "Post a Job" form
    can be pre-filled. Does not create a job.
    """
    result = analyze_job_description(payload.description)
    return APIResponse(success=True, message=f"Job description analyzed ({result['source']})", data=JobAnalysisResponse(**result))


@router.post("", response_model=APIResponse[JobResponse], status_code=201)
def create_job_endpoint(
    payload: JobCreate,
    current_user: User = Depends(require_role(UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    job = create_job(db, current_user.id, payload)
    return APIResponse(success=True, message="Job created successfully", data=JobResponse.from_job(job))


from app.core.deps import get_current_user, get_optional_user, require_role

from app.models.company import Company


@router.get("", response_model=APIResponse[list[JobResponse]])
def list_jobs(
    title: Optional[str] = Query(default=None),
    location: Optional[str] = Query(default=None),
    employment_type: Optional[str] = Query(default=None),
    skills: Optional[str] = Query(default=None),
    work_mode: Optional[str] = Query(default=None),
    verified_only: Optional[bool] = Query(default=False),
    current_user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db),
):
    query = db.query(Job).options(joinedload(Job.job_skills).joinedload(JobSkill.skill))

    if current_user and current_user.role in [UserRole.recruiter, UserRole.admin, UserRole.superadmin]:
        query = query.filter(or_(Job.recruiter_id == current_user.id, Job.status == JobStatus.published))
    else:
        query = query.filter(Job.status == JobStatus.published)

    if title:
        raw_tokens = [t.strip() for t in title.replace("/", " ").replace("(", " ").replace(")", " ").replace("-", " ").split() if len(t.strip()) > 1]
        tokens = [t for t in raw_tokens if t.lower() not in {"and", "or", "for", "the"}]
        if tokens:
            conditions = []
            for t in tokens:
                p = f"%{t}%"
                conditions.append(Job.title.ilike(p))
                conditions.append(Job.description.ilike(p))
                conditions.append(Job.company_name.ilike(p))
            query = query.filter(or_(*conditions))
        else:
            pattern = f"%{title}%"
            query = query.filter(or_(Job.title.ilike(pattern), Job.description.ilike(pattern), Job.company_name.ilike(pattern)))

    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    if employment_type:
        query = query.filter(Job.employment_type == employment_type)
    if work_mode:
        query = query.filter(Job.description.ilike(f"%{work_mode}%"))

    if skills:
        skill_list = [s.strip().lower() for s in skills.split(",") if s.strip()]
        if skill_list:
            query = query.join(Job.job_skills).join(JobSkill.skill).filter(
                or_(*[JobSkill.skill.has(skill_name=s) for s in skill_list])
            )

    if verified_only:
        verified_companies = db.query(Company.name).filter(Company.verification_status.in_(["domain_verified", "government_verified"])).all()
        v_names = [c[0] for c in verified_companies if c[0]]
        if v_names:
            query = query.filter(Job.company_name.in_(v_names))

    jobs = query.order_by(Job.created_at.desc()).all()
    return APIResponse(success=True, message="Jobs", data=[JobResponse.from_job(j) for j in jobs])



@router.get("/{job_id}", response_model=APIResponse[JobResponse])
def get_job(job_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    job = _load_job_or_404(db, job_id)
    if job.status != JobStatus.published and job.recruiter_id != current_user.id:
        raise NotFoundError("Job not found")
    return APIResponse(success=True, message="Job", data=JobResponse.from_job(job))


@router.put("/{job_id}", response_model=APIResponse[JobResponse])
def update_job_endpoint(
    job_id: str,
    payload: JobUpdate,
    current_user: User = Depends(require_role(UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    job = _load_job_or_404(db, job_id)
    if job.recruiter_id != current_user.id:
        raise PermissionDeniedError("You can only edit your own job postings.")
    job = update_job(db, job, payload)
    return APIResponse(success=True, message="Job updated", data=JobResponse.from_job(job))


@router.delete("/{job_id}", response_model=APIResponse[dict])
def delete_job_endpoint(
    job_id: str,
    current_user: User = Depends(require_role(UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    job = _load_job_or_404(db, job_id)
    if job.recruiter_id != current_user.id:
        raise PermissionDeniedError("You can only delete your own job postings.")
    db.delete(job)
    db.commit()
    return APIResponse(success=True, message="Job deleted", data={"id": job_id})


def _to_application_response(app: Application, job_title: str | None = None) -> ApplicationResponse:
    import json
    matched_sk = json.loads(app.matched_skills) if app.matched_skills else []
    missing_sk = json.loads(app.missing_skills) if app.missing_skills else []
    matched_kw = json.loads(app.matched_keywords) if app.matched_keywords else []
    missing_kw = json.loads(app.missing_keywords) if app.missing_keywords else []

    cand_user = app.candidate.user if (app.candidate and hasattr(app.candidate, "user")) else None

    return ApplicationResponse(
        id=app.id,
        candidate_id=app.candidate_id,
        job_id=app.job_id,
        status=app.status,
        match_score=app.match_score,
        applied_at=app.applied_at,
        updated_at=app.updated_at,
        ats_score=app.ats_score or app.match_score,
        job_match_score=app.job_match_score,
        skills_match_score=app.skills_match_score,
        experience_match_score=app.experience_match_score,
        education_match_score=app.education_match_score,
        location_match_score=app.location_match_score,
        keyword_match_score=app.keyword_match_score,
        responsibility_match_score=app.responsibility_match_score,
        matched_skills=matched_sk,
        missing_skills=missing_sk,
        matched_keywords=matched_kw,
        missing_keywords=missing_kw,
        recommendation=app.recommendation,
        screening_status=app.screening_status,
        is_eligible=app.is_eligible if app.is_eligible is not None else False,
        is_shortlisted=app.is_shortlisted if app.is_shortlisted is not None else False,
        screened_at=app.screened_at,
        screening_version=app.screening_version or "v1.0",
        recruiter_override=app.recruiter_override if app.recruiter_override is not None else False,
        override_reason=app.override_reason,
        candidate_name=cand_user.name if cand_user else None,
        candidate_email=cand_user.email if cand_user else None,
        job_title=job_title,
    )


@router.post("/{job_id}/apply", response_model=APIResponse[ApplicationResponse], status_code=201)
def apply_to_job_endpoint(
    job_id: str,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    try:
        parsed_id = uuid.UUID(job_id)
    except ValueError:
        raise NotFoundError("Job not found")

    application = apply_to_job(db, current_user.id, parsed_id)
    job = application.job or db.query(Job).filter(Job.id == application.job_id).first()
    return APIResponse(
        success=True,
        message="Application submitted and resume skills verified successfully",
        data=_to_application_response(application, job_title=job.title if job else None),
    )



@router.get("/{job_id}/ranking", response_model=APIResponse[list[dict]])
def get_job_ranking(
    job_id: str,
    current_user: User = Depends(require_role(UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    job = _load_job_or_404(db, job_id)
    if job.recruiter_id != current_user.id:
        raise PermissionDeniedError("You can only view rankings for your own job postings.")

    ranking = rank_applicants(db, job)
    return APIResponse(success=True, message="Candidate ranking", data=ranking)


@router.post("/{job_id}/generate-questions", response_model=APIResponse[QuestionGenerationResponse])
def generate_questions_endpoint(
    job_id: str,
    num_questions: int = Query(default=6, ge=1, le=15),
    current_user: User = Depends(require_role(UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    """
    Generates interview questions for this job via the configured LLM
    (or a hand-written question bank as a fallback). Preview only —
    persisting questions into an actual interview happens in Phase 5.
    """
    job = _load_job_or_404(db, job_id)
    if job.recruiter_id != current_user.id:
        raise PermissionDeniedError("You can only generate questions for your own job postings.")

    required_skills = [js.skill.skill_name for js in job.job_skills if js.required]
    result = generate_interview_questions(
        job_title=job.title,
        required_skills=required_skills,
        experience_years=job.experience_required,
        num_questions=num_questions,
    )
    return APIResponse(
        success=True,
        message=f"Questions generated ({result['source']})",
        data=QuestionGenerationResponse(**result),
    )


@router.post("/{job_id}/candidates/{candidate_id}/generate-questions", response_model=APIResponse[QuestionGenerationResponse])
def generate_candidate_interview_questions_endpoint(
    job_id: str,
    candidate_id: str,
    num_questions: int = Query(default=6, ge=1, le=15),
    current_user: User = Depends(require_role(UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    """
    Generates candidate-specific AI interview questions based on the job requirements
    AND the candidate's resume, skills, and experience.
    """
    job = _load_job_or_404(db, job_id)
    if job.recruiter_id != current_user.id:
        raise PermissionDeniedError("You can only generate questions for your own job postings.")

    candidate = db.query(CandidateProfile).options(
        joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill),
        joinedload(CandidateProfile.user)
    ).filter(CandidateProfile.id == candidate_id).first()

    if not candidate:
        raise NotFoundError("Candidate profile not found.")

    job_skills = [js.skill.skill_name for js in job.job_skills if js.required]
    cand_skills = [cs.skill.skill_name for cs in candidate.candidate_skills]
    combined_skills = sorted(list(set(job_skills + cand_skills)))

    result = generate_interview_questions(
        job_title=f"{job.title} (Candidate: {candidate.user.name if candidate.user else 'Candidate'})",
        required_skills=combined_skills,
        experience_years=candidate.experience_years or job.experience_required,
        num_questions=num_questions,
    )
    return APIResponse(
        success=True,
        message=f"Candidate-specific questions generated ({result['source']})",
        data=QuestionGenerationResponse(**result),
    )


from app.routers.applications import _to_response
from app.services.job_service import re_screen_application
from pydantic import BaseModel, Field


class ScreeningSettingsUpdate(BaseModel):
    min_ats_score: Optional[float] = Field(default=None, ge=0, le=100)
    min_job_match_score: Optional[float] = Field(default=None, ge=0, le=100)
    min_experience: Optional[float] = Field(default=None, ge=0)
    auto_screening: Optional[bool] = None
    auto_shortlist: Optional[bool] = None


@router.patch("/{job_id}/screening-settings", response_model=APIResponse[JobResponse])
def update_job_screening_settings(
    job_id: str,
    payload: ScreeningSettingsUpdate,
    current_user: User = Depends(require_role(UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    job = _load_job_or_404(db, job_id)
    if job.recruiter_id != current_user.id:
        raise PermissionDeniedError("You can only edit settings for your own job postings.")

    if payload.min_ats_score is not None:
        job.min_ats_score = payload.min_ats_score
    if payload.min_job_match_score is not None:
        job.min_job_match_score = payload.min_job_match_score
    if payload.min_experience is not None:
        job.min_experience = payload.min_experience
    if payload.auto_screening is not None:
        job.auto_screening = payload.auto_screening
    if payload.auto_shortlist is not None:
        job.auto_shortlist = payload.auto_shortlist

    db.commit()
    db.refresh(job)

    # Re-evaluate eligibility for all applications of this job under new threshold
    apps = db.query(Application).filter(Application.job_id == job.id).all()
    for app in apps:
        re_screen_application(db, app)

    return APIResponse(success=True, message="Screening settings updated", data=JobResponse.from_job(job))


@router.get("/{job_id}/screening-statistics", response_model=APIResponse[dict])
def get_job_screening_statistics(
    job_id: str,
    current_user: User = Depends(require_role(UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    job = _load_job_or_404(db, job_id)
    if job.recruiter_id != current_user.id:
        raise PermissionDeniedError("You can only view statistics for your own job postings.")

    applications = db.query(Application).filter(Application.job_id == job.id).all()

    # Re-screen any unscreened applications
    for app in applications:
        if not app.ats_score:
            re_screen_application(db, app)

    min_ats = getattr(job, "min_ats_score", 60.0) or 60.0

    total_applicants = len(applications)
    eligible_count = sum(1 for a in applications if (a.ats_score or a.match_score or 0.0) >= min_ats)
    shortlisted_count = sum(1 for a in applications if (a.status.value if hasattr(a.status, 'value') else str(a.status)) == "shortlisted")
    under_review_count = sum(1 for a in applications if (a.status.value if hasattr(a.status, 'value') else str(a.status)) in ["applied", "under_review"] and (a.ats_score or 0.0) < min_ats)
    not_recommended_count = sum(1 for a in applications if (a.ats_score or a.match_score or 0.0) < 40.0)

    # Top Candidates (ranked by ATS Score + Job Match Score)
    sorted_apps = sorted(applications, key=lambda a: (a.ats_score or 0.0) * 0.6 + (a.job_match_score or a.match_score or 0.0) * 0.4, reverse=True)

    top_candidates = []
    for app in sorted_apps[:5]:
        cand_user = app.candidate.user if (app.candidate and hasattr(app.candidate, "user")) else None
        top_candidates.append({
            "application_id": str(app.id),
            "candidate_name": cand_user.name if cand_user else "Candidate",
            "candidate_email": cand_user.email if cand_user else None,
            "ats_score": app.ats_score or app.match_score,
            "job_match_score": app.job_match_score or app.match_score,
            "status": app.status,
            "recommendation": app.recommendation,
        })

    stats = {
        "job_id": str(job.id),
        "job_title": job.title,
        "min_ats_threshold": min_ats,
        "total_applicants": total_applicants,
        "eligible_candidates": eligible_count,
        "shortlisted": shortlisted_count,
        "under_review": under_review_count,
        "not_recommended": not_recommended_count,
        "top_candidates": top_candidates,
    }
    return APIResponse(success=True, message="Screening statistics", data=stats)


@router.get("/{job_id}/applications/eligible", response_model=APIResponse[list[ApplicationResponse]])
def get_eligible_job_applications(
    job_id: str,
    current_user: User = Depends(require_role(UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    job = _load_job_or_404(db, job_id)
    if job.recruiter_id != current_user.id:
        raise PermissionDeniedError("You can only view applications for your own job postings.")

    min_ats = getattr(job, "min_ats_score", 60.0) or 60.0
    applications = (
        db.query(Application)
        .options(joinedload(Application.candidate).joinedload(CandidateProfile.user))
        .filter(Application.job_id == job.id)
        .all()
    )

    results = []
    for app in applications:
        if not app.ats_score:
            app = re_screen_application(db, app)
        if (app.ats_score or app.match_score or 0.0) >= min_ats:
            results.append(_to_response(app, job_title=job.title))

    results.sort(key=lambda a: a.ats_score or 0.0, reverse=True)
    return APIResponse(success=True, message="Eligible applications", data=results)


@router.get("/{job_id}/applications", response_model=APIResponse[list[ApplicationResponse]])
def get_job_applications(
    job_id: str,
    min_ats: Optional[float] = Query(default=None),
    status_filter: Optional[str] = Query(default=None),
    eligible_only: Optional[bool] = Query(default=False),
    current_user: User = Depends(require_role(UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    job = _load_job_or_404(db, job_id)
    if job.recruiter_id != current_user.id:
        raise PermissionDeniedError("You can only view applications for your own job postings.")

    applications = (
        db.query(Application)
        .options(joinedload(Application.candidate).joinedload(CandidateProfile.user))
        .filter(Application.job_id == job.id)
        .all()
    )

    results = []
    min_threshold = min_ats if min_ats is not None else 0.0
    threshold = getattr(job, "min_ats_score", 60.0) or 60.0

    for app in applications:
        if not app.ats_score:
            app = re_screen_application(db, app)

        score = app.ats_score or app.match_score or 0.0

        if min_ats is not None and score < min_ats:
            continue

        if eligible_only and score < threshold:
            continue

        if status_filter and status_filter.lower() != "all":
            app_st = (app.status.value if hasattr(app.status, "value") else str(app.status)).lower()
            if app_st != status_filter.lower():
                continue

        results.append(_to_response(app, job_title=job.title))

    results.sort(key=lambda a: a.ats_score or 0.0, reverse=True)
    return APIResponse(success=True, message="Applications", data=results)
