"""
candidate_search_service.py — Production-Grade Recruiter Candidate Search & Advanced Filtering Engine.

Executes multi-criteria candidate search, natural language query parsing, IT/non-IT skill normalization,
job-specific ATS match scoring, explainable AI ranking, configurable qualification thresholding,
saved search management, search history logging, direct invitations, and bulk shortlisting.
"""
import os
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_, desc

from app.models.application import Application
from app.models.candidate import CandidateProfile, CandidateSkill
from app.models.interview import Interview
from app.models.job import Job
from app.models.user import User, UserRole
from app.models.calendar import ScheduledInterview
from app.models.saved_search import (
    SavedCandidateSearch,
    CandidateSearchHistory,
    CandidateInvitation,
    CandidateShortlist,
)
from app.models.audit_log import AuditLog
from app.services.ats_scoring_service import calculate_job_specific_ats, normalize_skill
from app.services.search_query_parser import parse_search_query
from app.ml.semantic_matcher import semantic_similarity
from app.core.exceptions import NotFoundError, PermissionDeniedError, BadRequestError

# Configurable ranking weights (Must sum to 1.0)
CANDIDATE_SEARCH_WEIGHTS: Dict[str, float] = {
    "ats_score": 0.40,
    "skills_match": 0.25,
    "experience_match": 0.15,
    "interview_score": 0.10,
    "education_match": 0.10,
}


def search_and_rank_candidates(
    db: Session,
    query_text: Optional[str] = None,
    job_id: Optional[str] = None,
    filters: Optional[Dict[str, Any]] = None,
    qualification_threshold: float = 60.0,
    page: int = 1,
    page_size: int = 20,
    sort_by: str = "best_match",
    recruiter_id: Optional[uuid.UUID] = None,
) -> Dict[str, Any]:
    """
    Executes multi-criteria candidate search, parses query, applies filters,
    calculates dynamic job-specific ATS scores, ranks candidates, and paginates.
    """
    query_text = (query_text or "").strip()
    explicit_filters = filters or {}

    # 1. Parse natural language search query if provided
    parsed_query_filters = parse_search_query(query_text) if query_text else {}

    # Merge filters (explicit filters override parsed query)
    skills = explicit_filters.get("skills") or parsed_query_filters.get("skills") or []
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(",") if s.strip()]

    skill_match_mode = (explicit_filters.get("skill_match_mode") or "all").lower()

    min_exp = explicit_filters.get("minimum_experience")
    if min_exp is None:
        min_exp = parsed_query_filters.get("minimum_experience")

    max_exp = explicit_filters.get("maximum_experience")
    if max_exp is None:
        max_exp = parsed_query_filters.get("maximum_experience")

    location = explicit_filters.get("location") or parsed_query_filters.get("location")

    min_ats = explicit_filters.get("minimum_ats_score")
    if min_ats is None:
        min_ats = parsed_query_filters.get("minimum_ats_score")

    max_ats = explicit_filters.get("maximum_ats_score")

    min_interview = explicit_filters.get("minimum_interview_score")
    education_filter = explicit_filters.get("education")
    job_role_filter = explicit_filters.get("job_role") or parsed_query_filters.get("job_role")

    # Read threshold from request or fallback
    thresh = explicit_filters.get("qualification_threshold")
    if thresh is not None:
        try:
            qualification_threshold = float(thresh)
        except (ValueError, TypeError):
            pass

    # Normalize requested skills
    norm_requested_skills = [normalize_skill(s) for s in skills if s]

    # Retrieve selected job if job_id provided
    target_job = None
    explicit_job_id = None
    if job_id:
        try:
            j_uuid = uuid.UUID(job_id)
            target_job = db.query(Job).options(joinedload(Job.job_skills)).filter(Job.id == j_uuid).first()
            explicit_job_id = j_uuid
        except ValueError:
            target_job = None

    # Fallback to latest posted job if ATS filter is requested without explicit job_id
    if not target_job and min_ats is not None:
        target_job = db.query(Job).order_by(Job.created_at.desc()).first()

    # 2. Query Candidate Profiles
    query_db = db.query(CandidateProfile).options(
        joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill),
        joinedload(CandidateProfile.user),
    )

    if explicit_job_id:
        # Target job specified: return ONLY candidates who applied for this specific job
        applied_cand_ids = db.query(Application.candidate_id).filter(Application.job_id == explicit_job_id)
        query_db = query_db.filter(CandidateProfile.id.in_(applied_cand_ids))
    elif job_id:
        # Invalid format job_id provided -> empty query
        query_db = query_db.filter(CandidateProfile.id == uuid.uuid4())
    else:
        # All Jobs: return candidates who applied to at least one job or were uploaded by recruiters
        applied_cand_ids = db.query(Application.candidate_id)
        query_db = query_db.filter(
            or_(
                CandidateProfile.id.in_(applied_cand_ids),
                CandidateProfile.created_by_recruiter_id.isnot(None)
            )
        )

    all_candidates = query_db.all()

    # Log search history if recruiter_id provided and query/filters are active
    if recruiter_id and (query_text or explicit_filters):
        try:
            log_search_history(db, recruiter_id, query_text, explicit_filters)
        except Exception:
            pass

    matched_results = []

    for cand in all_candidates:
        cand_user = cand.user
        cand_name = cand_user.name if cand_user else "Candidate"
        cand_email = cand_user.email if cand_user else ""

        cand_headline = cand.headline or cand.current_role or "Software Professional"
        cand_location = cand.location or "Not Specified"
        exp_years = float(cand.experience_years or 0.0)
        cand_education = cand.education or ""
        cand_resume_text = f"{cand.resume_text or ''} {cand.summary or ''} {cand.work_experience or ''}"

        # Natural Language Query Matching (Name, Resume, Headline, Role, Education)
        if query_text:
            q_lower = query_text.lower()
            text_to_search = f"{cand_name.lower()} {cand_headline.lower()} {cand_location.lower()} {cand_education.lower()} {cand_resume_text.lower()}"
            
            # Simple keyword match or semantic match
            keyword_hit = any(part in text_to_search for part in q_lower.split() if len(part) > 2)
            if not keyword_hit:
                # Fallback to semantic similarity check for candidate profile
                sem_sim = semantic_similarity(query_text, cand_resume_text[:1500])
                if sem_sim < 30.0:
                    continue

        # Candidate Skills
        cand_skills_list = [cs.skill.skill_name for cs in cand.candidate_skills if cs.skill]
        cand_skills_norm = {normalize_skill(s).lower(): s for s in cand_skills_list}

        # Skill Matching
        matched_skills = []
        missing_skills = []

        if norm_requested_skills:
            for req_skill in norm_requested_skills:
                req_lower = req_skill.lower()
                if req_lower in cand_skills_norm:
                    matched_skills.append(cand_skills_norm[req_lower])
                elif req_lower in cand_resume_text.lower():
                    matched_skills.append(req_skill)
                else:
                    missing_skills.append(req_skill)

            if skill_match_mode == "all" and len(matched_skills) < len(norm_requested_skills):
                continue
            elif skill_match_mode == "any" and len(matched_skills) == 0:
                continue

        skills_match_pct = (len(matched_skills) / max(len(norm_requested_skills), 1)) * 100.0 if norm_requested_skills else 100.0

        # Experience Filter
        if min_exp is not None and exp_years < float(min_exp):
            continue
        if max_exp is not None and exp_years > float(max_exp):
            continue

        # Location Filter (Partial matching & Remote support)
        if location and location.strip():
            loc_query = location.strip().lower()
            if loc_query not in cand_location.lower() and loc_query != "remote":
                continue

        # Job Role Filter
        if job_role_filter and job_role_filter.strip():
            if job_role_filter.strip().lower() not in cand_headline.lower():
                continue

        # Education Filter
        if education_filter and education_filter.strip():
            if education_filter.strip().lower() not in cand_education.lower():
                continue

        # Job-Specific ATS & Job Match Calculation
        ats_score = 0.0
        job_match_score = 0.0
        matched_keywords = []

        if target_job:
            ats_res = calculate_job_specific_ats(cand, target_job)
            ats_score = float(ats_res["overall_ats_score"])
            job_match_score = float(ats_res["overall_ats_score"])
            matched_keywords = ats_res.get("matched_keywords", [])
        else:
            ats_score = float(cand.profile_score or 75.0)
            job_match_score = ats_score

        # ATS Score Filter
        if min_ats is not None and ats_score < float(min_ats):
            continue
        if max_ats is not None and ats_score > float(max_ats):
            continue

        # Latest Interview Score Retrieval
        latest_interview = (
            db.query(Interview)
            .filter(Interview.candidate_id == cand.id)
            .order_by(Interview.created_at.desc())
            .first()
        )
        interview_score = float(latest_interview.overall_score) if (latest_interview and latest_interview.overall_score is not None) else None

        if min_interview is not None:
            if interview_score is None or interview_score < float(min_interview):
                continue

        # Experience Match Sub-score
        req_exp = target_job.experience_required if target_job else 2.0
        exp_match_pct = min(100.0, (exp_years / max(req_exp, 1.0)) * 100.0)

        # Education Sub-score
        edu_score = 100.0 if cand.education else 80.0

        # Interview Sub-score
        effective_interview_score = interview_score if interview_score is not None else 75.0

        # Weighted Ranking Score Calculation
        ranking_score = round(
            ats_score * CANDIDATE_SEARCH_WEIGHTS["ats_score"]
            + skills_match_pct * CANDIDATE_SEARCH_WEIGHTS["skills_match"]
            + exp_match_pct * CANDIDATE_SEARCH_WEIGHTS["experience_match"]
            + effective_interview_score * CANDIDATE_SEARCH_WEIGHTS["interview_score"]
            + edu_score * CANDIDATE_SEARCH_WEIGHTS["education_match"],
            1,
        )

        # Qualification Threshold Calculation
        primary_eval_score = max(ats_score, job_match_score)
        is_qualified = primary_eval_score >= qualification_threshold
        qualification_badge = "✓ Qualified" if is_qualified else "Below Threshold"

        # Build Explainable AI Match Reasons ("Why this candidate?")
        match_reasons = []
        for sk in matched_skills[:4]:
            match_reasons.append(f"✓ {sk} matched")
        if exp_years > 0:
            match_reasons.append(f"✓ {exp_years:g} years experience")
        if location and location.strip() and (location.strip().lower() in cand_location.lower() or "remote" in cand_location.lower()):
            match_reasons.append(f"✓ Location matched ({cand_location})")
        if ats_score > 0:
            match_reasons.append(f"✓ {round(ats_score)}% ATS score")
        if target_job:
            match_reasons.append(f"✓ {round(job_match_score)}% job match")

        created_str = cand.created_at.strftime("%Y-%m-%d") if cand.created_at else ""
        updated_str = cand.updated_at.strftime("%Y-%m-%d") if cand.updated_at else ""

        matched_results.append({
            "candidate_id": str(cand.id),
            "user_id": str(cand.user_id) if cand.user_id else "",
            "candidate_name": cand_name,
            "candidate_email": cand_email,
            "headline": cand_headline,
            "job_role": cand.current_role or cand_headline,
            "location": cand_location,
            "experience_years": exp_years,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "matched_keywords": matched_keywords,
            "ats_score": round(ats_score, 1),
            "job_match_score": round(job_match_score, 1),
            "interview_score": round(interview_score, 1) if interview_score is not None else None,
            "ranking_score": ranking_score,
            "education": cand_education or "Not Specified",
            "is_qualified": is_qualified,
            "qualification_badge": qualification_badge,
            "match_reasons": match_reasons,
            "has_resume": bool(cand.resume_path or cand.resume_text),
            "resume_filename": cand.resume_original_filename or (os.path.basename(cand.resume_path) if cand.resume_path else None),
            "created_at": created_str,
            "updated_at": updated_str,
        })

    # 3. Sort Results
    if sort_by == "ats_score":
        matched_results.sort(key=lambda x: x["ats_score"], reverse=True)
    elif sort_by == "experience":
        matched_results.sort(key=lambda x: x["experience_years"], reverse=True)
    elif sort_by == "interview_score":
        matched_results.sort(key=lambda x: (x["interview_score"] or 0), reverse=True)
    elif sort_by == "newest":
        matched_results.sort(key=lambda x: x["created_at"], reverse=True)
    elif sort_by == "recently_updated":
        matched_results.sort(key=lambda x: x["updated_at"], reverse=True)
    else:
        # Default: best_match
        matched_results.sort(key=lambda x: x["ranking_score"], reverse=True)

    # 4. Compute Summary Stats
    total_results = len(matched_results)
    qualified_count = sum(1 for c in matched_results if c["is_qualified"])

    # Compute shortlists, invites, interviews count
    shortlisted_count = 0
    invited_count = 0
    interviews_scheduled = 0

    if recruiter_id:
        shortlisted_count = db.query(CandidateShortlist).filter(CandidateShortlist.recruiter_id == recruiter_id).count()
        invited_count = db.query(CandidateInvitation).filter(CandidateInvitation.recruiter_id == recruiter_id).count()
        interviews_scheduled = db.query(ScheduledInterview).filter(ScheduledInterview.recruiter_id == recruiter_id).count()

    # 5. Pagination
    page_size = max(1, page_size)
    total_pages = max(1, (total_results + page_size - 1) // page_size)
    page = max(1, min(page, total_pages))

    start_idx = (page - 1) * page_size
    paginated_results = matched_results[start_idx : start_idx + page_size]

    return {
        "total_results": total_results,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages,
        "qualification_threshold": qualification_threshold,
        "summary_stats": {
            "total_found": total_results,
            "qualified_count": qualified_count,
            "shortlisted_count": shortlisted_count,
            "invited_count": invited_count,
            "interviews_scheduled": interviews_scheduled,
        },
        "filters_applied": {
            "query": query_text,
            "skills": norm_requested_skills,
            "skill_match_mode": skill_match_mode,
            "minimum_experience": min_exp,
            "maximum_experience": max_exp,
            "location": location,
            "minimum_ats_score": min_ats,
            "maximum_ats_score": max_ats,
            "minimum_interview_score": min_interview,
            "education": education_filter,
            "job_role": job_role_filter,
            "job_id": job_id,
            "qualification_threshold": qualification_threshold,
        },
        "results": paginated_results,
    }


# Saved Search Services
def save_candidate_search(
    db: Session,
    recruiter_id: uuid.UUID,
    name: str,
    query: Optional[str] = "",
    job_id: Optional[str] = None,
    filters: Optional[Dict[str, Any]] = None
) -> SavedCandidateSearch:
    j_uuid = None
    if job_id:
        try:
            j_uuid = uuid.UUID(job_id)
        except ValueError:
            pass

    saved = SavedCandidateSearch(
        recruiter_id=recruiter_id,
        name=name,
        query=query or "",
        job_id=j_uuid,
        filters=filters or {},
    )
    db.add(saved)
    db.commit()
    db.refresh(saved)
    return saved


def get_saved_searches(db: Session, recruiter_id: uuid.UUID) -> List[SavedCandidateSearch]:
    return (
        db.query(SavedCandidateSearch)
        .filter(SavedCandidateSearch.recruiter_id == recruiter_id)
        .order_by(SavedCandidateSearch.created_at.desc())
        .all()
    )


def delete_saved_search(db: Session, recruiter_id: uuid.UUID, search_id: uuid.UUID) -> bool:
    saved = (
        db.query(SavedCandidateSearch)
        .filter(SavedCandidateSearch.id == search_id, SavedCandidateSearch.recruiter_id == recruiter_id)
        .first()
    )
    if not saved:
        raise NotFoundError("Saved search not found")
    db.delete(saved)
    db.commit()
    return True


# Search History Services
def log_search_history(
    db: Session,
    recruiter_id: uuid.UUID,
    query: str,
    filters: Dict[str, Any]
):
    entry = CandidateSearchHistory(
        recruiter_id=recruiter_id,
        query=query,
        filters=filters,
    )
    db.add(entry)
    db.commit()


def get_recent_searches(db: Session, recruiter_id: uuid.UUID, limit: int = 10) -> List[Dict[str, Any]]:
    records = (
        db.query(CandidateSearchHistory)
        .filter(CandidateSearchHistory.recruiter_id == recruiter_id)
        .order_by(CandidateSearchHistory.created_at.desc())
        .limit(limit)
        .all()
    )
    history = []
    seen = set()
    for r in records:
        q_str = r.query or ""
        if q_str and q_str not in seen:
            seen.add(q_str)
            history.append({
                "id": str(r.id),
                "query": q_str,
                "filters": r.filters,
                "created_at": r.created_at.isoformat() if r.created_at else ""
            })
    return history


def clear_search_history(db: Session, recruiter_id: uuid.UUID) -> bool:
    db.query(CandidateSearchHistory).filter(CandidateSearchHistory.recruiter_id == recruiter_id).delete()
    db.commit()
    return True


# Candidate Engagement & Invitation Services
def invite_candidate(
    db: Session,
    recruiter_id: uuid.UUID,
    candidate_id: uuid.UUID,
    job_id: uuid.UUID,
    message: Optional[str] = ""
) -> CandidateInvitation:
    # Check if invitation already exists to prevent duplicate invites
    existing = (
        db.query(CandidateInvitation)
        .filter(
            CandidateInvitation.recruiter_id == recruiter_id,
            CandidateInvitation.candidate_id == candidate_id,
            CandidateInvitation.job_id == job_id,
        )
        .first()
    )
    if existing:
        return existing

    invitation = CandidateInvitation(
        recruiter_id=recruiter_id,
        candidate_id=candidate_id,
        job_id=job_id,
        message=message or "We reviewed your profile and would like to invite you to apply for our job role.",
        status="invited"
    )
    db.add(invitation)

    # Log audit
    audit = AuditLog(
        user_id=recruiter_id,
        action="candidate_invited",
        details=f"Invited candidate {candidate_id} for job {job_id}",
    )
    db.add(audit)

    db.commit()
    db.refresh(invitation)

    # Optionally trigger invitation email
    try:
        cand_profile = db.query(CandidateProfile).filter(CandidateProfile.id == candidate_id).first()
        job_obj = db.query(Job).filter(Job.id == job_id).first()
        if cand_profile and cand_profile.user and job_obj:
            from app.services.email_service import send_shortlisted_email
            send_shortlisted_email(
                db=db,
                recruiter_id=recruiter_id,
                candidate_email=cand_profile.user.email,
                candidate_name=cand_profile.user.name,
                job_title=job_obj.title,
                company_name=job_obj.company_name or "AI Recruiter",
                candidate_id=str(candidate_id),
                job_id=str(job_id),
            )
    except Exception:
        pass

    return invitation


def bulk_invite_candidates(
    db: Session,
    recruiter_id: uuid.UUID,
    candidate_ids: List[str],
    job_id: uuid.UUID,
    message: Optional[str] = ""
) -> Dict[str, Any]:
    invited_count = 0
    skipped_count = 0

    for c_id_str in candidate_ids:
        try:
            c_uuid = uuid.UUID(c_id_str)
            invite_candidate(db, recruiter_id, c_uuid, job_id, message)
            invited_count += 1
        except Exception:
            skipped_count += 1

    return {
        "invited_count": invited_count,
        "skipped_count": skipped_count,
        "message": f"Successfully sent invitations to {invited_count} candidate(s)."
    }


def shortlist_candidate(
    db: Session,
    recruiter_id: uuid.UUID,
    candidate_id: uuid.UUID,
    job_id: Optional[uuid.UUID] = None,
    notes: Optional[str] = ""
) -> CandidateShortlist:
    existing = (
        db.query(CandidateShortlist)
        .filter(
            CandidateShortlist.recruiter_id == recruiter_id,
            CandidateShortlist.candidate_id == candidate_id,
            CandidateShortlist.job_id == job_id,
        )
        .first()
    )
    if existing:
        return existing

    shortlist = CandidateShortlist(
        recruiter_id=recruiter_id,
        candidate_id=candidate_id,
        job_id=job_id,
        notes=notes or "Shortlisted from Recruiter Candidate Search."
    )
    db.add(shortlist)

    # Log Audit
    db.add(AuditLog(
        user_id=recruiter_id,
        action="candidate_shortlisted",
        details=f"Shortlisted candidate {candidate_id}",
    ))

    db.commit()
    db.refresh(shortlist)
    return shortlist


def bulk_shortlist_candidates(
    db: Session,
    recruiter_id: uuid.UUID,
    candidate_ids: List[str],
    job_id: Optional[uuid.UUID] = None
) -> Dict[str, Any]:
    count = 0
    for c_id_str in candidate_ids:
        try:
            c_uuid = uuid.UUID(c_id_str)
            shortlist_candidate(db, recruiter_id, c_uuid, job_id)
            count += 1
        except Exception:
            pass

    return {
        "shortlisted_count": count,
        "message": f"Successfully shortlisted {count} candidate(s)."
    }


# Secure Resume Access Service
def get_candidate_resume_file(
    db: Session,
    candidate_id: uuid.UUID,
    requesting_user: User
) -> Tuple[str, str, str]:
    """
    Verifies permission and returns (file_path, filename, media_type) for candidate's resume.
    Recruiters, admins, or candidate owner are allowed. Public access is forbidden.
    """
    profile = db.query(CandidateProfile).filter(CandidateProfile.id == candidate_id).first()
    if not profile:
        raise NotFoundError("Candidate profile not found")

    # Authorization Check
    if requesting_user.role not in [UserRole.recruiter, UserRole.company_admin, UserRole.admin]:
        if profile.user_id != requesting_user.id:
            raise PermissionDeniedError("Unauthorized access to candidate resume")

    if not profile.resume_path or not os.path.exists(profile.resume_path):
        raise NotFoundError("Resume file does not exist on server")

    file_path = profile.resume_path
    filename = profile.resume_original_filename or os.path.basename(file_path)

    media_type = "application/pdf"
    if filename.lower().endswith(".docx"):
        media_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    elif filename.lower().endswith(".doc"):
        media_type = "application/msword"

    # Audit log resume access
    db.add(AuditLog(
        user_id=requesting_user.id,
        action="resume_viewed",
        details=f"User viewed resume for candidate {candidate_id}",
    ))
    db.commit()

    return file_path, filename, media_type
