"""
Admin panel endpoints: manage users and skills, view all jobs, and
system-wide statistics. Every endpoint requires the admin role, which
(per app/schemas/user.py) can never be self-registered - only created
via scripts/create_admin.py.
"""
import uuid
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_role
from app.core.exceptions import NotFoundError
from app.models.application import Application
from app.models.audit_log import AuditLog
from app.models.candidate import Skill
from app.models.job import Job
from app.models.user import User, UserRole
from app.schemas.admin import (
    AdminJobOut,
    AdminSkillCreate,
    AdminSkillOut,
    AdminUserOut,
    AuditLogOut,
    SystemStats,
)
from app.schemas.common import APIResponse
from app.services.admin_service import create_skill, delete_skill, delete_user, get_system_stats
from app.utils.audit import log_action

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/users", response_model=APIResponse[list[AdminUserOut]])
def list_users(
    role: Optional[UserRole] = Query(default=None),
    current_user: User = Depends(require_role(UserRole.admin)),
    db: Session = Depends(get_db),
):
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    users = query.order_by(User.created_at.desc()).all()
    return APIResponse(success=True, message="Users", data=[AdminUserOut.model_validate(u) for u in users])


@router.get("/users/{user_id}", response_model=APIResponse[AdminUserOut])
def get_user(
    user_id: str,
    current_user: User = Depends(require_role(UserRole.admin)),
    db: Session = Depends(get_db),
):
    try:
        parsed_id = uuid.UUID(user_id)
    except ValueError:
        raise NotFoundError("User not found")

    user = db.get(User, parsed_id)
    if not user:
        raise NotFoundError("User not found")
    return APIResponse(success=True, message="User", data=AdminUserOut.model_validate(user))


@router.delete("/users/{user_id}", response_model=APIResponse[dict])
def delete_user_endpoint(
    user_id: str,
    current_user: User = Depends(require_role(UserRole.admin)),
    db: Session = Depends(get_db),
):
    try:
        parsed_id = uuid.UUID(user_id)
    except ValueError:
        raise NotFoundError("User not found")

    delete_user(db, parsed_id, current_user.id)
    log_action(db, "admin.user_deleted", user_id=current_user.id, details={"deleted_user_id": user_id})
    return APIResponse(success=True, message="User deleted", data={"id": user_id})


@router.get("/skills", response_model=APIResponse[list[AdminSkillOut]])
def list_skills(
    current_user: User = Depends(require_role(UserRole.admin)),
    db: Session = Depends(get_db),
):
    skills = db.query(Skill).order_by(Skill.skill_name).all()
    return APIResponse(success=True, message="Skills", data=[AdminSkillOut.model_validate(s) for s in skills])


@router.post("/skills", response_model=APIResponse[AdminSkillOut], status_code=201)
def create_skill_endpoint(
    payload: AdminSkillCreate,
    current_user: User = Depends(require_role(UserRole.admin)),
    db: Session = Depends(get_db),
):
    skill = create_skill(db, payload.skill_name, payload.category)
    log_action(db, "admin.skill_created", user_id=current_user.id, details={"skill_name": payload.skill_name})
    return APIResponse(success=True, message="Skill created", data=AdminSkillOut.model_validate(skill))


@router.delete("/skills/{skill_id}", response_model=APIResponse[dict])
def delete_skill_endpoint(
    skill_id: str,
    current_user: User = Depends(require_role(UserRole.admin)),
    db: Session = Depends(get_db),
):
    try:
        parsed_id = uuid.UUID(skill_id)
    except ValueError:
        raise NotFoundError("Skill not found")

    delete_skill(db, parsed_id)
    log_action(db, "admin.skill_deleted", user_id=current_user.id, details={"skill_id": skill_id})
    return APIResponse(success=True, message="Skill deleted", data={"id": skill_id})


@router.get("/jobs", response_model=APIResponse[list[AdminJobOut]])
def list_all_jobs(
    current_user: User = Depends(require_role(UserRole.admin)),
    db: Session = Depends(get_db),
):
    jobs = db.query(Job).order_by(Job.created_at.desc()).all()
    result = []
    for job in jobs:
        recruiter = db.get(User, job.recruiter_id)
        applications_count = db.query(Application).filter(Application.job_id == job.id).count()
        result.append(
            AdminJobOut(
                id=job.id,
                title=job.title,
                status=job.status.value,
                recruiter_name=recruiter.name if recruiter else None,
                applications_count=applications_count,
                created_at=job.created_at,
            )
        )
    return APIResponse(success=True, message="Jobs", data=result)


@router.get("/stats", response_model=APIResponse[SystemStats])
def system_stats(
    current_user: User = Depends(require_role(UserRole.admin)),
    db: Session = Depends(get_db),
):
    stats = get_system_stats(db)
    return APIResponse(success=True, message="System statistics", data=SystemStats(**stats))


from app.models.company import Company
from app.services.admin_service import (
    create_skill,
    delete_skill,
    delete_user,
    get_system_stats,
    moderate_job_status,
    toggle_user_active_status,
    update_company_verification_status,
)


@router.patch("/users/{user_id}/toggle-active", response_model=APIResponse[dict])
def toggle_user_active_endpoint(
    user_id: str,
    current_user: User = Depends(require_role(UserRole.admin)),
    db: Session = Depends(get_db),
):
    try:
        parsed_id = uuid.UUID(user_id)
    except ValueError:
        raise NotFoundError("User not found")

    user = toggle_user_active_status(db, parsed_id, current_user.id)
    status_str = "active" if user.is_active else "suspended"
    log_action(db, "admin.user_status_toggled", user_id=current_user.id, details={"target_user": user_id, "status": status_str})
    return APIResponse(success=True, message=f"User account is now {status_str}", data={"id": user_id, "is_active": user.is_active})


@router.get("/companies", response_model=APIResponse[list[dict]])
def list_companies(
    current_user: User = Depends(require_role(UserRole.admin)),
    db: Session = Depends(get_db),
):
    companies = db.query(Company).order_by(Company.created_at.desc()).all()
    data = [
        {
            "id": str(c.id),
            "name": c.name,
            "registration_number": c.registration_number,
            "cin_gstin": c.cin_gstin,
            "country": c.country,
            "address": c.address,
            "website": c.website,
            "official_email": c.official_email,
            "verification_status": c.verification_status,
            "ssl_verified": c.ssl_verified,
            "ssl_details": c.ssl_details,
            "verification_notes": c.verification_notes,
            "created_at": c.created_at.isoformat() if c.created_at else None,
        }
        for c in companies
    ]
    return APIResponse(success=True, message="Companies list", data=data)


@router.patch("/companies/{company_id}/verification", response_model=APIResponse[dict])
def review_company_verification(
    company_id: str,
    status: str,
    notes: Optional[str] = None,
    current_user: User = Depends(require_role(UserRole.admin)),
    db: Session = Depends(get_db),
):
    try:
        parsed_id = uuid.UUID(company_id)
    except ValueError:
        raise NotFoundError("Company not found")

    company = update_company_verification_status(db, parsed_id, status=status, notes=notes)
    log_action(db, "admin.company_verified", user_id=current_user.id, details={"company": company.name, "status": status})
    return APIResponse(success=True, message=f"Company verification status updated to {status}", data={"id": company_id, "status": company.verification_status})


@router.get("/suspicious-jobs", response_model=APIResponse[list[dict]])
def list_suspicious_jobs(
    current_user: User = Depends(require_role(UserRole.admin)),
    db: Session = Depends(get_db),
):
    jobs = (
        db.query(Job)
        .filter((Job.fraud_risk_score >= 30.0) | (Job.status.in_(["pending_review", "flagged"])))
        .order_by(Job.fraud_risk_score.desc())
        .all()
    )
    data = []
    for j in jobs:
        recruiter = db.get(User, j.recruiter_id)
        data.append(
            {
                "id": str(j.id),
                "title": j.title,
                "company_name": j.company_name or "Unknown Company",
                "recruiter_name": recruiter.name if recruiter else "Unknown Recruiter",
                "recruiter_email": recruiter.email if recruiter else None,
                "status": j.status.value if hasattr(j.status, "value") else str(j.status),
                "fraud_risk_score": j.fraud_risk_score,
                "fraud_risk_level": j.fraud_risk_level,
                "fraud_reasons": j.fraud_reasons,
                "salary_range": j.salary_range,
                "created_at": j.created_at.isoformat() if j.created_at else None,
            }
        )
    return APIResponse(success=True, message="Suspicious jobs list", data=data)


@router.patch("/jobs/{job_id}/moderate", response_model=APIResponse[dict])
def moderate_job(
    job_id: str,
    status: str,
    current_user: User = Depends(require_role(UserRole.admin)),
    db: Session = Depends(get_db),
):
    try:
        parsed_id = uuid.UUID(job_id)
    except ValueError:
        raise NotFoundError("Job not found")

    job = moderate_job_status(db, parsed_id, status=status)
    log_action(db, "admin.job_moderated", user_id=current_user.id, details={"job_id": job_id, "status": status})
    return APIResponse(success=True, message=f"Job status set to {status}", data={"id": job_id, "status": job.status.value if hasattr(job.status, "value") else str(job.status)})


from app.models.recruiter import RecruiterProfile
from app.services.admin_service import approve_recruiter_account, reject_recruiter_account


@router.get("/pending-recruiters", response_model=APIResponse[list[dict]])
def list_pending_recruiters(
    current_user: User = Depends(require_role(UserRole.admin)),
    db: Session = Depends(get_db),
):
    users = (
        db.query(User)
        .filter(User.role.in_([UserRole.recruiter, UserRole.company_admin]), User.verification_status == "pending_admin_review")
        .order_by(User.created_at.desc())
        .all()
    )
    data = []
    for u in users:
        prof = db.query(RecruiterProfile).filter(RecruiterProfile.user_id == u.id).first()
        data.append(
            {
                "id": str(u.id),
                "name": u.name,
                "email": u.email,
                "verification_status": u.verification_status,
                "verification_reasons": u.verification_reasons,
                "job_title": prof.job_title if prof else None,
                "phone": prof.phone if prof else None,
                "company_name": prof.company_name if prof else None,
                "website": prof.website if prof else None,
                "industry": prof.industry if prof else None,
                "company_size": prof.company_size if prof else None,
                "company_location": prof.location if prof else None,
                "created_at": u.created_at.isoformat() if u.created_at else None,
            }
        )
    return APIResponse(success=True, message="Pending recruiters list", data=data)


@router.patch("/recruiters/{user_id}/approve", response_model=APIResponse[dict])
def approve_recruiter_endpoint(
    user_id: str,
    current_user: User = Depends(require_role(UserRole.admin)),
    db: Session = Depends(get_db),
):
    try:
        parsed_id = uuid.UUID(user_id)
    except ValueError:
        raise NotFoundError("User not found")

    user = approve_recruiter_account(db, parsed_id)
    log_action(db, "admin.recruiter_approved", user_id=current_user.id, details={"recruiter_id": user_id})
    return APIResponse(success=True, message=f"Recruiter {user.name} approved successfully", data={"id": user_id, "verification_status": user.verification_status})


@router.patch("/recruiters/{user_id}/reject", response_model=APIResponse[dict])
def reject_recruiter_endpoint(
    user_id: str,
    current_user: User = Depends(require_role(UserRole.admin)),
    db: Session = Depends(get_db),
):
    try:
        parsed_id = uuid.UUID(user_id)
    except ValueError:
        raise NotFoundError("User not found")

    user = reject_recruiter_account(db, parsed_id)
    log_action(db, "admin.recruiter_rejected", user_id=current_user.id, details={"recruiter_id": user_id})
    return APIResponse(success=True, message=f"Recruiter {user.name} registration rejected", data={"id": user_id, "verification_status": user.verification_status})


@router.get("/audit-logs", response_model=APIResponse[list[AuditLogOut]])
def list_audit_logs(
    limit: int = Query(default=50, ge=1, le=200),
    action: Optional[str] = Query(default=None),
    current_user: User = Depends(require_role(UserRole.admin)),
    db: Session = Depends(get_db),
):
    query = db.query(AuditLog)
    if action:
        query = query.filter(AuditLog.action == action)
    logs = query.order_by(AuditLog.created_at.desc()).limit(limit).all()
    return APIResponse(success=True, message="Audit logs", data=[AuditLogOut.model_validate(l) for l in logs])




