"""
admin_service.py — user/skill management and system-wide statistics
for the admin panel, plus the admin-account creation logic used by
both the CLI bootstrap script and (if ever needed) an authenticated
admin-promotes-admin endpoint.
"""
from collections import Counter

from sqlalchemy.orm import Session

from app.core.exceptions import AppError, ConflictError, NotFoundError
from app.core.security import hash_password
from app.models.application import Application, ApplicationStatus
from app.models.candidate import CandidateProfile, CandidateSkill, Skill
from app.models.interview import Interview, InterviewStatus
from app.models.job import Job, JobSkill
from app.models.user import User, UserRole


def create_admin_user(db: Session, name: str, email: str, password: str) -> User:
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise ConflictError(f"A user with email '{email}' already exists.")

    admin = User(name=name, email=email, password_hash=hash_password(password), role=UserRole.admin)
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin


def delete_user(db: Session, target_user_id, acting_admin_id) -> None:
    if target_user_id == acting_admin_id:
        raise AppError("You cannot delete your own admin account.", "CANNOT_DELETE_SELF", 400)

    user = db.get(User, target_user_id)
    if not user:
        raise NotFoundError("User not found")

    db.delete(user)
    db.commit()


def create_skill(db: Session, skill_name: str, category: str | None) -> Skill:
    existing = db.query(Skill).filter(Skill.skill_name == skill_name).first()
    if existing:
        raise ConflictError(f"Skill '{skill_name}' already exists.")

    skill = Skill(skill_name=skill_name, category=category)
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return skill


def delete_skill(db: Session, skill_id) -> None:
    skill = db.get(Skill, skill_id)
    if not skill:
        raise NotFoundError("Skill not found")
    db.delete(skill)
    db.commit()


from app.models.company import Company


def toggle_user_active_status(db: Session, target_user_id, acting_admin_id) -> User:
    if target_user_id == acting_admin_id:
        raise AppError("You cannot suspend your own admin account.", "CANNOT_SUSPEND_SELF", 400)

    user = db.get(User, target_user_id)
    if not user:
        raise NotFoundError("User not found")

    user.is_active = not getattr(user, "is_active", True)
    db.commit()
    db.refresh(user)
    return user


def update_company_verification_status(db: Session, company_id, status: str, notes: str = None) -> Company:
    company = db.get(Company, company_id)
    if not company:
        raise NotFoundError("Company not found")

    company.verification_status = status
    if notes:
        company.verification_notes = notes
    db.commit()
    db.refresh(company)
    return company


def moderate_job_status(db: Session, job_id, status: str) -> Job:
    job = db.get(Job, job_id)
    if not job:
        raise NotFoundError("Job not found")

    job.status = status
    db.commit()
    db.refresh(job)
    return job


def approve_recruiter_account(db: Session, user_id) -> User:
    user = db.get(User, user_id)
    if not user:
        raise NotFoundError("User not found")

    user.verification_status = "approved"
    user.is_active = True
    db.commit()
    db.refresh(user)
    return user


def reject_recruiter_account(db: Session, user_id) -> User:
    user = db.get(User, user_id)
    if not user:
        raise NotFoundError("User not found")

    user.verification_status = "rejected"
    user.is_active = False
    db.commit()
    db.refresh(user)
    return user



def get_system_stats(db: Session) -> dict:
    users = db.query(User).all()
    users_by_role = Counter(u.role.value for u in users)

    companies = db.query(Company).all()
    verified_companies = sum(1 for c in companies if c.verification_status in ["domain_verified", "government_verified"])

    jobs = db.query(Job).all()
    published_jobs = sum(1 for j in jobs if j.status.value == "published")
    suspicious_jobs = sum(1 for j in jobs if (j.fraud_risk_score or 0) >= 30.0 or j.status.value in ["pending_review", "flagged"])

    applications = db.query(Application).all()
    match_scores = [a.match_score for a in applications if a.match_score is not None]
    avg_match_score = round(sum(match_scores) / len(match_scores), 2) if match_scores else None

    applications_by_status = {status.value: 0 for status in ApplicationStatus}
    for a in applications:
        applications_by_status[a.status.value] += 1

    interviews = db.query(Interview).all()
    completed_interviews = [i for i in interviews if i.status == InterviewStatus.completed]
    interview_scores = [i.overall_score for i in completed_interviews if i.overall_score is not None]
    avg_interview_score = round(sum(interview_scores) / len(interview_scores), 2) if interview_scores else None
    interview_completion_rate = (
        round(len(completed_interviews) / len(interviews) * 100, 2) if interviews else None
    )

    # Most requested skills across all job postings (required + preferred).
    job_skill_counter: Counter = Counter()
    for js in db.query(JobSkill).all():
        job_skill_counter[js.skill_id] += 1
    skills_by_id = {s.id: s.skill_name for s in db.query(Skill).all()}
    most_requested_skills = [
        {"skill": skills_by_id[skill_id], "count": count}
        for skill_id, count in job_skill_counter.most_common(10)
        if skill_id in skills_by_id
    ]

    # Most common skills across all candidate profiles.
    candidate_skill_counter: Counter = Counter()
    for cs in db.query(CandidateSkill).all():
        candidate_skill_counter[cs.skill_id] += 1
    most_common_candidate_skills = [
        {"skill": skills_by_id[skill_id], "count": count}
        for skill_id, count in candidate_skill_counter.most_common(10)
        if skill_id in skills_by_id
    ]

    return {
        "total_users": len(users),
        "total_recruiters": users_by_role.get("recruiter", 0),
        "total_candidates": users_by_role.get("candidate", 0),
        "total_admins": users_by_role.get("admin", 0) + users_by_role.get("superadmin", 0),
        "total_companies": len(companies),
        "verified_companies": verified_companies,
        "total_jobs": len(jobs),
        "published_jobs": published_jobs,
        "suspicious_jobs": suspicious_jobs,
        "total_applications": len(applications),
        "applications_by_status": applications_by_status,
        "avg_match_score": avg_match_score,
        "total_interviews": len(interviews),
        "completed_interviews": len(completed_interviews),
        "interview_completion_rate": interview_completion_rate,
        "avg_interview_score": avg_interview_score,
        "most_requested_skills": most_requested_skills,
        "most_common_candidate_skills": most_common_candidate_skills,
    }

