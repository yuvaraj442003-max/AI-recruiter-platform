"""
job_service.py — job creation/update with skill normalization, applying
to a job (computing + persisting a match score), ranking a job's
applicants, and recommending jobs to a candidate.
"""
import json
import logging
import uuid

logger = logging.getLogger("ai_recruiter.services.job_service")

from sqlalchemy.orm import Session, joinedload

from app.core.exceptions import AppError, ConflictError, NotFoundError
from app.ml.ranking import compute_match
from app.models.application import Application, ApplicationStatus
from app.models.candidate import CandidateProfile, CandidateSkill, Skill
from app.models.job import Job, JobSkill, JobStatus
from app.nlp.skill_extractor import extract_skills
from app.nlp.skills_data import ALIAS_INDEX


from app.services.fraud_service import detect_job_fraud
from app.services.notification_service import create_notification
from app.models.user import User, UserRole


def _normalize_skill_name(raw_name: str) -> str:
    canonical = ALIAS_INDEX.get(raw_name.strip().lower())
    return canonical or raw_name.strip().title()


def _get_or_create_skill(db: Session, name: str) -> Skill:
    canonical = _normalize_skill_name(name)
    skill = db.query(Skill).filter(Skill.skill_name == canonical).first()
    if not skill:
        skill = Skill(skill_name=canonical, category=None)
        db.add(skill)
        db.flush()
    return skill


def _set_job_skills(db: Session, job: Job, required_skills: list[str], preferred_skills: list[str]) -> None:
    db.query(JobSkill).filter(JobSkill.job_id == job.id).delete()

    seen: set[str] = set()
    for name in required_skills:
        skill = _get_or_create_skill(db, name)
        if skill.skill_name in seen:
            continue
        seen.add(skill.skill_name)
        db.add(JobSkill(job_id=job.id, skill_id=skill.id, required=True, weight=1.0))

    for name in preferred_skills:
        skill = _get_or_create_skill(db, name)
        if skill.skill_name in seen:
            continue
        seen.add(skill.skill_name)
        db.add(JobSkill(job_id=job.id, skill_id=skill.id, required=False, weight=0.5))


import datetime
from app.ml.ats_screener import screen_candidate_ats

def create_job(db: Session, recruiter_id: uuid.UUID, payload) -> Job:
    # 1. Run AI Fraud Detection
    fraud_result = detect_job_fraud(
        title=payload.title,
        description=payload.description,
        salary_range=payload.salary_range,
        company_website=getattr(payload, "company_website", None),
    )

    initial_status = payload.status
    if fraud_result["risk_level"] == "HIGH":
        initial_status = JobStatus.pending_review

    non_tech_val = getattr(payload, "non_technical_skills", None)
    if isinstance(non_tech_val, list):
        non_tech_val = ", ".join(non_tech_val)

    job = Job(
        recruiter_id=recruiter_id,
        title=payload.title,
        description=payload.description,
        location=payload.location,
        employment_type=payload.employment_type,
        experience_required=payload.experience_required,
        salary_range=payload.salary_range,
        status=initial_status,
        relevant_work_experience=getattr(payload, "relevant_work_experience", None),
        non_technical_skills=non_tech_val,
        company_experience_requirements=getattr(payload, "company_experience_requirements", None),
        min_ats_score=getattr(payload, "min_ats_score", 60.0) or 60.0,
        min_job_match_score=getattr(payload, "min_job_match_score", 60.0) or 60.0,
        min_experience=getattr(payload, "min_experience", 0.0) or 0.0,
        auto_screening=getattr(payload, "auto_screening", True) if getattr(payload, "auto_screening", True) is not None else True,
        auto_shortlist=getattr(payload, "auto_shortlist", True) if getattr(payload, "auto_shortlist", True) is not None else True,
        fraud_risk_score=fraud_result["risk_score"],
        fraud_risk_level=fraud_result["risk_level"],
        fraud_reasons=json.dumps(fraud_result["reasons"]),
        company_name=getattr(payload, "company_name", None),
        company_logo=getattr(payload, "company_logo", None),
        company_description=getattr(payload, "company_description", None),
        company_website=getattr(payload, "company_website", None),
        company_location=getattr(payload, "company_location", None),
        industry=getattr(payload, "industry", None),
        company_size=getattr(payload, "company_size", None),
        linkedin_profile=getattr(payload, "linkedin_profile", None),
        github_profile=getattr(payload, "github_profile", None),
        other_links=getattr(payload, "other_links", None),
    )
    db.add(job)
    db.flush()

    required = payload.required_skills
    preferred = payload.preferred_skills or []
    if required is None:
        required = extract_skills(payload.description)

    _set_job_skills(db, job, required, preferred)

    # Notify admins if high risk fraud detected
    if fraud_result["risk_level"] == "HIGH":
        admins = db.query(User).filter(User.role.in_([UserRole.admin, UserRole.superadmin])).all()
        for admin in admins:
            create_notification(
                db=db,
                user_id=admin.id,
                title="High Fraud Risk Job Flagged",
                message=f"Job '{job.title}' by {job.company_name or 'Recruiter'} scored {fraud_result['risk_score']}/100 and requires review.",
                notification_type="warning",
                link="/admin.html",
            )

    db.commit()
    db.refresh(job)
    return _load_job(db, job.id)


def update_job(db: Session, job: Job, payload) -> Job:
    data = payload.model_dump(exclude_unset=True, exclude={"required_skills", "preferred_skills"})
    for field, value in data.items():
        setattr(job, field, value)

    # Re-evaluate fraud risk if description or title changed
    if payload.title is not None or payload.description is not None:
        fraud_result = detect_job_fraud(
            title=job.title,
            description=job.description,
            salary_range=job.salary_range,
            company_website=job.company_website,
        )
        job.fraud_risk_score = fraud_result["risk_score"]
        job.fraud_risk_level = fraud_result["risk_level"]
        job.fraud_reasons = json.dumps(fraud_result["reasons"])
        if fraud_result["risk_level"] == "HIGH" and job.status == JobStatus.published:
            job.status = JobStatus.pending_review

    if payload.required_skills is not None or payload.preferred_skills is not None:
        current_required = [js.skill.skill_name for js in job.job_skills if js.required]
        current_preferred = [js.skill.skill_name for js in job.job_skills if not js.required]
        _set_job_skills(
            db,
            job,
            payload.required_skills if payload.required_skills is not None else current_required,
            payload.preferred_skills if payload.preferred_skills is not None else current_preferred,
        )

    db.commit()
    db.refresh(job)
    return _load_job(db, job.id)



def _load_job(db: Session, job_id) -> Job:
    return (
        db.query(Job)
        .options(joinedload(Job.job_skills).joinedload(JobSkill.skill))
        .filter(Job.id == job_id)
        .first()
    )


def _load_candidate_profile(db: Session, user_id) -> CandidateProfile | None:
    return (
        db.query(CandidateProfile)
        .options(joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill))
        .filter(CandidateProfile.user_id == user_id)
        .first()
    )


def re_screen_application(db: Session, application: Application) -> Application:
    """Calculates or re-calculates ATS screening score for an application."""
    job = _load_job(db, application.job_id)
    cand = application.candidate
    if not cand:
        cand = (
            db.query(CandidateProfile)
            .options(joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill))
            .filter(CandidateProfile.id == application.candidate_id)
            .first()
        )

    if not job or not cand:
        return application

    ats_res = screen_candidate_ats(cand, job, min_ats_threshold=getattr(job, "min_ats_score", 60.0))

    application.ats_score = ats_res.ats_score
    application.job_match_score = ats_res.job_match_score
    application.skills_match_score = ats_res.skills_match_score
    application.experience_match_score = ats_res.experience_match_score
    application.education_match_score = ats_res.education_match_score
    application.location_match_score = ats_res.location_match_score
    application.keyword_match_score = ats_res.keyword_match_score
    application.responsibility_match_score = ats_res.responsibility_match_score

    application.matched_skills = json.dumps(ats_res.matched_skills)
    application.missing_skills = json.dumps(ats_res.missing_skills)
    application.matched_keywords = json.dumps(ats_res.matched_keywords)
    application.missing_keywords = json.dumps(ats_res.missing_keywords)

    application.recommendation = ats_res.recommendation
    application.screening_status = ats_res.screening_status
    application.is_eligible = ats_res.is_eligible
    application.screened_at = datetime.datetime.now(datetime.timezone.utc)
    application.screening_version = ats_res.version

    application.match_score = ats_res.ats_score
    application.match_breakdown = json.dumps(ats_res.to_dict())

    # Auto Shortlist check if candidate applied and is eligible
    if getattr(job, "auto_shortlist", True) and ats_res.is_eligible and application.status == ApplicationStatus.applied:
        application.status = ApplicationStatus.shortlisted
        application.is_shortlisted = True

    db.commit()
    db.refresh(application)
    return application


def apply_to_job(db: Session, candidate_user_id, job_id) -> Application:
    profile = _load_candidate_profile(db, candidate_user_id)
    if not profile or (not profile.resume_path and not profile.resume_text and not profile.candidate_skills and not profile.summary and not profile.work_experience):
        raise AppError(
            "Please upload your resume before applying to jobs so the system can verify and extract your skills.", "NO_RESUME", 400
        )

    # Auto-extract and sync skills into profile if missing
    if not profile.candidate_skills and (profile.resume_text or profile.summary or profile.work_experience):
        resume_full_text = f"{profile.resume_text or ''} {profile.summary or ''} {profile.work_experience or ''}"
        from app.nlp.skill_extractor import extract_skills
        extracted = extract_skills(resume_full_text)
        if extracted:
            from app.services.resume_service import _sync_candidate_skills, seed_skills
            seed_skills(db)
            _sync_candidate_skills(db, profile, extracted)
            db.commit()
            profile = _load_candidate_profile(db, candidate_user_id)

    job = _load_job(db, job_id)
    if not job:
        raise NotFoundError("Job not found")
    if job.status != JobStatus.published:
        if job.status == JobStatus.paused:
            raise AppError("This job posting is currently paused and not accepting new applications.", "JOB_PAUSED", 400)
        raise AppError("This job is not currently accepting applications.", "JOB_NOT_PUBLISHED", 400)

    existing = (
        db.query(Application)
        .filter(Application.candidate_id == profile.id, Application.job_id == job.id)
        .first()
    )
    if existing:
        raise ConflictError("You have already applied to this job.")

    # Execute ATS Screening logic
    ats_res = screen_candidate_ats(profile, job, min_ats_threshold=getattr(job, "min_ats_score", 60.0))


    auto_short = getattr(job, "auto_shortlist", False)
    if auto_short and ats_res.is_eligible:
        initial_status = ApplicationStatus.shortlisted
        is_shortlisted = True
    else:
        initial_status = ApplicationStatus.applied
        is_shortlisted = False

    application = Application(
        candidate_id=profile.id,
        job_id=job.id,
        status=initial_status,
        match_score=ats_res.ats_score,
        match_breakdown=json.dumps(ats_res.to_dict()),
        ats_score=ats_res.ats_score,
        job_match_score=ats_res.job_match_score,
        skills_match_score=ats_res.skills_match_score,
        experience_match_score=ats_res.experience_match_score,
        education_match_score=ats_res.education_match_score,
        location_match_score=ats_res.location_match_score,
        keyword_match_score=ats_res.keyword_match_score,
        responsibility_match_score=ats_res.responsibility_match_score,
        matched_skills=json.dumps(ats_res.matched_skills),
        missing_skills=json.dumps(ats_res.missing_skills),
        matched_keywords=json.dumps(ats_res.matched_keywords),
        missing_keywords=json.dumps(ats_res.missing_keywords),
        recommendation=ats_res.recommendation,
        screening_status=ats_res.screening_status,
        is_eligible=ats_res.is_eligible,
        is_shortlisted=is_shortlisted,
        screened_at=datetime.datetime.now(datetime.timezone.utc),
        screening_version=ats_res.version,
    )
    db.add(application)
    db.commit()
    db.refresh(application)

    # Dispatch Application Received & Shortlisted emails in background
    try:
        cand_user = profile.user if profile else None
        if cand_user and cand_user.email:
            comp_name = job.company_name or "AI Recruiter"
            from app.services.email_service import send_application_received_email, send_shortlisted_email
            send_application_received_email(
                to_email=cand_user.email,
                candidate_name=cand_user.name,
                job_title=job.title,
                company_name=comp_name,
                candidate_id=profile.id,
                job_id=job.id,
                db=db,
            )

            if is_shortlisted:
                send_shortlisted_email(
                    to_email=cand_user.email,
                    candidate_name=cand_user.name,
                    job_title=job.title,
                    company_name=comp_name,
                    candidate_id=profile.id,
                    job_id=job.id,
                    recruiter_id=job.recruiter_id,
                    db=db,
                )
    except Exception as exc:
        logger.warning(f"Failed to dispatch application confirmation email: {exc}")

    return application


def rank_applicants(db: Session, job: Job) -> list[dict]:
    applications = (
        db.query(Application)
        .options(
            joinedload(Application.candidate).joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill),
            joinedload(Application.candidate),
        )
        .filter(Application.job_id == job.id)
        .all()
    )

    ranked_items = []
    for app in applications:
        if app.candidate:
            match_res = compute_match(app.candidate, job)
            match_dict = match_res.to_dict()
            app.match_score = match_res.final_score
            app.match_breakdown = json.dumps(match_dict)
            ranked_items.append((app, match_dict))
        else:
            breakdown = json.loads(app.match_breakdown) if app.match_breakdown else {}
            ranked_items.append((app, breakdown))

    db.commit()
    ranked_items.sort(key=lambda x: x[0].match_score or 0.0, reverse=True)

    ranked = []
    for rank, (app, match_dict) in enumerate(ranked_items, start=1):
        ranked.append(
            {
                "rank": rank,
                "application_id": app.id,
                "candidate_id": app.candidate_id,
                "status": app.status,
                "match_score": app.match_score,
                "breakdown": match_dict.get("breakdown") if match_dict else None,
                "explanation": match_dict.get("explanation") if match_dict else None,
            }
        )
    return ranked


def recommend_jobs_for_candidate(db: Session, candidate_user_id, limit: int = 10) -> list[dict]:
    profile = _load_candidate_profile(db, candidate_user_id)
    if not profile:
        return []

    jobs = (
        db.query(Job)
        .options(joinedload(Job.job_skills).joinedload(JobSkill.skill))
        .filter(Job.status == JobStatus.published)
        .all()
    )

    scored = []
    for job in jobs:
        result = compute_match(profile, job)
        scored.append({"job": job, "match_score": result.final_score, "breakdown": result.to_dict()["breakdown"]})

    scored.sort(key=lambda item: item["match_score"], reverse=True)
    return scored[:limit]
