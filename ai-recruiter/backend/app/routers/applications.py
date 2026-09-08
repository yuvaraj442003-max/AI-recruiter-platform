"""
Application endpoints not scoped under a specific job: a candidate's
own application list, a single application's detail, and status
updates by the owning recruiter (shortlist, reject, etc.).
"""
import json
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from app.core.database import get_db
from app.core.deps import require_role
from app.core.exceptions import NotFoundError, PermissionDeniedError
from app.models.application import Application
from app.models.candidate import CandidateProfile
from app.models.job import Job
from app.models.user import User, UserRole
from app.schemas.application import (
    ApplicationDetailResponse,
    ApplicationResponse,
    ApplicationStatusUpdate,
)
from app.schemas.common import APIResponse

router = APIRouter(prefix="/applications", tags=["Applications"])


from app.services.job_service import re_screen_application

def _to_response(app: Application, job_title: str | None = None) -> ApplicationResponse:
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
        is_shortlisted=app.is_shortlisted if app.is_shortlisted is not None else (app.status == ApplicationStatus.shortlisted),
        screened_at=app.screened_at,
        screening_version=app.screening_version or "v1.0",
        recruiter_override=app.recruiter_override if app.recruiter_override is not None else False,
        override_reason=app.override_reason,
        source=getattr(app, "source", "direct_candidate") or "direct_candidate",
        uploaded_by_recruiter_id=str(app.uploaded_by_recruiter_id) if getattr(app, "uploaded_by_recruiter_id", None) else None,
        candidate_name=cand_user.name if cand_user else None,
        candidate_email=cand_user.email if cand_user else None,
        job_title=job_title,
    )


@router.get("", response_model=APIResponse[list[ApplicationResponse]])
def list_my_applications(
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
    if not profile:
        return APIResponse(success=True, message="Applications", data=[])

    applications = (
        db.query(Application)
        .options(joinedload(Application.job))
        .filter(Application.candidate_id == profile.id)
        .order_by(Application.applied_at.desc())
        .all()
    )
    return APIResponse(
        success=True,
        message="Applications",
        data=[_to_response(a, job_title=a.job.title if a.job else None) for a in applications],
    )


@router.post("/{application_id}/screen", response_model=APIResponse[ApplicationResponse])
def screen_application_endpoint(
    application_id: str,
    current_user: User = Depends(require_role(UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    try:
        parsed_id = uuid.UUID(application_id)
    except ValueError:
        raise NotFoundError("Application not found")

    application = (
        db.query(Application)
        .options(joinedload(Application.job), joinedload(Application.candidate))
        .filter(Application.id == parsed_id)
        .first()
    )
    if not application:
        raise NotFoundError("Application not found")
    if not application.job or application.job.recruiter_id != current_user.id:
        raise PermissionDeniedError("You can only screen applications for your own job postings.")

    application = re_screen_application(db, application)
    return APIResponse(
        success=True,
        message="Application screened successfully",
        data=_to_response(application, job_title=application.job.title),
    )


@router.get("/{application_id}/ats-report", response_model=APIResponse[dict])
def get_ats_report_endpoint(
    application_id: str,
    current_user: User = Depends(require_role(UserRole.candidate, UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    try:
        parsed_id = uuid.UUID(application_id)
    except ValueError:
        raise NotFoundError("Application not found")

    application = (
        db.query(Application)
        .options(joinedload(Application.job), joinedload(Application.candidate))
        .filter(Application.id == parsed_id)
        .first()
    )
    if not application:
        raise NotFoundError("Application not found")

    if not application.ats_score:
        application = re_screen_application(db, application)

    breakdown_dict = json.loads(application.match_breakdown) if application.match_breakdown else {}

    report = {
        "application_id": str(application.id),
        "ats_score": application.ats_score or application.match_score,
        "job_match_score": application.job_match_score or application.match_score,
        "screening_status": application.screening_status or "Eligible",
        "recommendation": application.recommendation or "Review Required",
        "is_eligible": application.is_eligible,
        "recruiter_override": application.recruiter_override,
        "override_reason": application.override_reason,
        "scores": {
            "skills_match": application.skills_match_score,
            "experience_match": application.experience_match_score,
            "education_match": application.education_match_score,
            "location_match": application.location_match_score,
            "keyword_match": application.keyword_match_score,
            "responsibility_match": application.responsibility_match_score,
        },
        "matched_skills": json.loads(application.matched_skills) if application.matched_skills else [],
        "missing_skills": json.loads(application.missing_skills) if application.missing_skills else [],
        "matched_keywords": json.loads(application.matched_keywords) if application.matched_keywords else [],
        "missing_keywords": json.loads(application.missing_keywords) if application.missing_keywords else [],
        "breakdown": breakdown_dict.get("breakdown") if breakdown_dict else None,
        "explanation": breakdown_dict.get("explanation") if breakdown_dict else None,
    }
    return APIResponse(success=True, message="ATS Report", data=report)


@router.get("/{application_id}", response_model=APIResponse[ApplicationDetailResponse])
def get_application(
    application_id: str,
    current_user: User = Depends(require_role(UserRole.candidate, UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    try:
        parsed_id = uuid.UUID(application_id)
    except ValueError:
        raise NotFoundError("Application not found")

    application = (
        db.query(Application)
        .options(
            joinedload(Application.job),
            joinedload(Application.candidate).joinedload(CandidateProfile.user),
            joinedload(Application.candidate).joinedload(CandidateProfile.candidate_skills)
        )
        .filter(Application.id == parsed_id)
        .first()
    )
    if not application:
        raise NotFoundError("Application not found")

    is_owning_candidate = (
        current_user.role == UserRole.candidate
        and application.candidate
        and application.candidate.user_id == current_user.id
    )
    is_owning_recruiter = (
        current_user.role == UserRole.recruiter
        and application.job
        and application.job.recruiter_id == current_user.id
    )
    if not (is_owning_candidate or is_owning_recruiter):
        raise PermissionDeniedError("You don't have access to this application.")

    breakdown_data = json.loads(application.match_breakdown) if application.match_breakdown else None
    
    cand = application.candidate
    cand_user = cand.user if cand else None
    cand_profile_dict = None
    if cand:
        cand_profile_dict = {
            "id": str(cand.id),
            "user_id": str(cand.user_id),
            "name": cand_user.name if cand_user else "Candidate",
            "email": cand_user.email if cand_user else None,
            "phone": cand.phone,
            "location": cand.location,
            "address": cand.address,
            "headline": getattr(cand, "headline", None),
            "current_role": getattr(cand, "current_role", None),
            "summary": cand.summary,
            "ai_summary": cand.ai_summary,
            "experience_years": cand.experience_years,
            "education": cand.education,
            "work_experience": cand.work_experience,
            "certifications": getattr(cand, "certifications", None),
            "portfolio_url": getattr(cand, "portfolio_url", None),
            "linkedin_url": getattr(cand, "linkedin_url", None),
            "github_url": getattr(cand, "github_url", None),
            "other_links": getattr(cand, "other_links", None),
            "profile_photo": getattr(cand, "profile_photo", None),
            "resume_original_filename": cand.resume_original_filename,
            "profile_score": cand.profile_score,
            "skills": sorted({cs.skill.skill_name for cs in cand.candidate_skills if cs.skill}),
        }

    job = application.job
    job_dict = None
    if job:
        job_dict = {
            "id": str(job.id),
            "title": job.title,
            "description": job.description,
            "location": job.location,
            "employment_type": job.employment_type,
            "experience_required": job.experience_required,
            "salary_range": job.salary_range,
            "company_name": getattr(job, "company_name", None),
            "company_logo": getattr(job, "company_logo", None),
            "min_ats_score": getattr(job, "min_ats_score", 60.0),
        }

    response = ApplicationDetailResponse(
        **_to_response(application, job_title=job.title if job else None).model_dump(),
        breakdown=breakdown_data.get("breakdown") if breakdown_data else None,
        explanation=breakdown_data.get("explanation") if breakdown_data else None,
        ats_report={
            "ats_score": application.ats_score or application.match_score,
            "job_match_score": application.job_match_score,
            "screening_status": application.screening_status,
            "recommendation": application.recommendation,
            "is_eligible": application.is_eligible,
            "matched_skills": json.loads(application.matched_skills) if application.matched_skills else [],
            "missing_skills": json.loads(application.missing_skills) if application.missing_skills else [],
            "matched_keywords": json.loads(application.matched_keywords) if application.matched_keywords else [],
            "missing_keywords": json.loads(application.missing_keywords) if application.missing_keywords else [],
        },
        candidate_profile=cand_profile_dict,
        job_details=job_dict,
    )
    return APIResponse(success=True, message="Application detail", data=response)


from app.models.application_history import ApplicationStatusHistory
from app.services.notification_service import create_notification


@router.patch("/{application_id}/status", response_model=APIResponse[ApplicationResponse])
def update_application_status(
    application_id: str,
    payload: ApplicationStatusUpdate,
    current_user: User = Depends(require_role(UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    try:
        parsed_id = uuid.UUID(application_id)
    except ValueError:
        raise NotFoundError("Application not found")

    application = (
        db.query(Application)
        .options(joinedload(Application.job), joinedload(Application.candidate))
        .filter(Application.id == parsed_id)
        .first()
    )
    if not application:
        raise NotFoundError("Application not found")
    if not application.job or application.job.recruiter_id != current_user.id:
        raise PermissionDeniedError("You can only update applications for your own job postings.")

    old_status = application.status.value if hasattr(application.status, "value") else str(application.status)
    application.status = payload.status
    new_status = payload.status.value if hasattr(payload.status, "value") else str(payload.status)

    min_ats = getattr(application.job, "min_ats_score", 60.0) or 60.0
    current_ats = application.ats_score or application.match_score or 0.0

    # Recruiter override check
    if payload.override_reason or (new_status == "shortlisted" and current_ats < min_ats):
        application.recruiter_override = True
        application.override_reason = payload.override_reason or f"Manually shortlisted by recruiter despite ATS score ({current_ats}%) being below threshold ({min_ats}%)."

    if new_status == "shortlisted":
        application.is_shortlisted = True

    note_text = f"Status changed by recruiter ({current_user.name})"
    if application.recruiter_override:
        note_text += f" [Recruiter Override: {application.override_reason}]"

    # 1. Log Application Status History
    history = ApplicationStatusHistory(
        application_id=application.id,
        previous_status=old_status,
        new_status=new_status,
        notes=note_text,
    )
    db.add(history)

    # 2. Notify Candidate
    if application.candidate and application.candidate.user_id:
        title_map = {
            "under_review": "Application Under Review",
            "shortlisted": "Application Shortlisted!",
            "interview": "Interview Invitation",
            "selected": "Congratulations! You have been Selected",
            "rejected": "Application Status Update",
        }
        type_map = {
            "shortlisted": "success",
            "selected": "success",
            "interview": "info",
            "rejected": "warning",
        }
        create_notification(
            db=db,
            user_id=application.candidate.user_id,
            title=title_map.get(new_status, "Application Status Updated"),
            message=f"Your application for '{application.job.title}' is now: {new_status.replace('_', ' ').title()}.",
            notification_type=type_map.get(new_status, "info"),
            link="/my-applications.html",
        )

        # Send status update email to candidate
        try:
            from app.services.email_service import send_application_status_email
            cand_user = application.candidate.user if application.candidate else None
            if cand_user and cand_user.email:
                comp_name = (
                    application.job.company.name if (application.job and getattr(application.job, "company", None))
                    else f"{current_user.name}'s Company"
                )
                job_title = application.job.title if application.job else "Position"
                send_application_status_email(
                    to_email=cand_user.email,
                    candidate_name=cand_user.name,
                    job_title=job_title,
                    company_name=comp_name,
                    new_status=new_status,
                    notes=payload.notes if hasattr(payload, 'notes') and payload.notes else None,
                    db=db,
                )
        except Exception as err:
            print(f"Warning: Failed to dispatch status update email: {err}")

    db.commit()
    db.refresh(application)

    return APIResponse(
        success=True,
        message="Application status updated",
        data=_to_response(application, job_title=application.job.title),
    )

