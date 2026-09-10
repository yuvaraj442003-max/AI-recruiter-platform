"""
talent_rediscovery_service.py — Production-Grade Talent Pool Auto-Rediscovery & Silver Medalist Matching Engine.

Implements skill normalization, multi-dimensional weighted scoring (Skills 35%, Experience 20%, Semantic 20%,
Responsibilities 10%, Keywords 5%, Location 5%, Education 5%), Silver Medalist detection, Redis progress tracking,
and PostgreSQL result persistence.
"""
import json
import logging
import threading
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy.orm import Session, joinedload

from app.core.database import SessionLocal
from app.core.exceptions import AppError, NotFoundError
from app.models.application import Application
from app.models.candidate import CandidateProfile, CandidateSkill
from app.models.job import Job, JobSkill
from app.models.notification import Notification
from app.models.screening import CandidateConsent
from app.models.talent_rediscovery import (
    RediscoveryRunStatus,
    TalentRediscoveryResult,
    TalentRediscoveryRun,
)
from app.models.user import User
from app.services.redis_service import cache_set_json, cache_get_json

logger = logging.getLogger("ai_recruiter.services.talent_rediscovery")

# Normalized skill mappings dictionary
SKILL_NORMALIZATION_MAP = {
    "react": "React.js",
    "reactjs": "React.js",
    "react.js": "React.js",
    "react js": "React.js",
    "node": "Node.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "node js": "Node.js",
    "ts": "TypeScript",
    "typescript": "TypeScript",
    "js": "JavaScript",
    "javascript": "JavaScript",
    "py": "Python",
    "python": "Python",
    "fastapi": "FastAPI",
    "django": "Django",
    "flask": "Flask",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "sql": "SQL",
    "redis": "Redis",
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "k8s": "Kubernetes",
    "aws": "AWS",
    "amazon web services": "AWS",
    "azure": "Azure",
    "gcp": "GCP",
    "google cloud": "GCP",
    "html": "HTML",
    "css": "CSS",
    "tailwind": "TailwindCSS",
    "tailwindcss": "TailwindCSS",
    "nextjs": "Next.js",
    "next.js": "Next.js",
    "vue": "Vue.js",
    "vuejs": "Vue.js",
    "vue.js": "Vue.js",
}


def normalize_skill_name(skill_name: str) -> str:
    """Normalizes skill variants (e.g. 'react', 'React.js', 'react js' -> 'React.js')."""
    if not skill_name:
        return ""
    cleaned = skill_name.strip().lower()
    return SKILL_NORMALIZATION_MAP.get(cleaned, skill_name.strip())


def extract_and_normalize_job_requirements(job: Job) -> Dict[str, Any]:
    """Extracts and normalizes job requirements for deterministic talent matching."""
    job_skills_raw = []
    if job.job_skills:
        for js in job.job_skills:
            if js.skill and js.skill.skill_name:
                job_skills_raw.append(js.skill.skill_name)

    normalized_req_skills = list(set([normalize_skill_name(s) for s in job_skills_raw if s]))
    if not normalized_req_skills and job.description:
        # Extract basic keywords from description if skills list empty
        desc_lower = job.description.lower()
        for key in SKILL_NORMALIZATION_MAP.keys():
            if key in desc_lower:
                normalized_req_skills.append(SKILL_NORMALIZATION_MAP[key])
        normalized_req_skills = list(set(normalized_req_skills))

    responsibilities = []
    if job.description:
        lines = job.description.split("\n")
        for line in lines:
            line_str = line.strip()
            if line_str.startswith("-") or line_str.startswith("•") or line_str.startswith("*"):
                responsibilities.append(line_str.lstrip("-•* ").strip())

    return {
        "job_id": job.id,
        "title": job.title or "",
        "required_skills": normalized_req_skills,
        "minimum_experience": job.experience_required or 0.0,
        "location": job.location or "",
        "responsibilities": responsibilities,
        "description": job.description or "",
    }


def get_eligible_candidate_pool(db: Session, job: Job, rules: Optional[Dict[str, Any]] = None) -> List[CandidateProfile]:
    """Retrieves all active candidate profiles eligible for talent rediscovery."""
    query = (
        db.query(CandidateProfile)
        .join(User, CandidateProfile.user_id == User.id)
        .options(
            joinedload(CandidateProfile.user),
            joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill),
            joinedload(CandidateProfile.applications),
        )
        .filter(User.is_active == True)
    )

    # Exclude candidates who explicitly opted out of automated recruitment
    opted_out_ids = [
        c.candidate_id for c in db.query(CandidateConsent).filter(CandidateConsent.opted_out_all == True).all()
    ]
    if opted_out_ids:
        query = query.filter(~CandidateProfile.id.in_(opted_out_ids))

    candidates = query.all()
    return candidates


def calculate_candidate_rediscovery_score(candidate: CandidateProfile, job_reqs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes a multi-dimensional weighted deterministic match score (0.0 - 100.0).
    Weights: Skills 35%, Experience 20%, Semantic 20%, Responsibilities 10%, Keywords 5%, Location 5%, Education 5%.
    """
    cand_skills_raw = []
    if candidate.candidate_skills:
        for cs in candidate.candidate_skills:
            if cs.skill and cs.skill.skill_name:
                cand_skills_raw.append(cs.skill.skill_name)

    cand_skills = set([normalize_skill_name(s) for s in cand_skills_raw if s])
    req_skills = set(job_reqs.get("required_skills", []))

    matched_skills = list(cand_skills.intersection(req_skills))
    missing_skills = list(req_skills.difference(cand_skills))

    # 1. Skills Score (35%)
    if req_skills:
        skills_score = (len(matched_skills) / len(req_skills)) * 100.0
    else:
        skills_score = 80.0

    # 2. Experience Score (20%)
    req_exp = job_reqs.get("minimum_experience", 0.0)
    cand_exp = candidate.experience_years or 0.0

    if cand_exp >= req_exp:
        experience_score = 100.0
    elif req_exp > 0:
        experience_score = max(30.0, (cand_exp / req_exp) * 100.0)
    else:
        experience_score = 100.0

    # 3. Semantic & Responsibility Match (30%)
    cand_text = f"{candidate.headline or ''} {candidate.summary or ''} {candidate.work_experience or ''}".lower()
    job_text = f"{job_reqs.get('title', '')} {job_reqs.get('description', '')}".lower()

    # Simple keyword overlap heuristic for semantic score
    kw_hits = 0
    total_kws = max(1, len(req_skills))
    for sk in req_skills:
        if sk.lower() in cand_text:
            kw_hits += 1
    semantic_score = min(100.0, max(40.0, (kw_hits / total_kws) * 100.0))

    resp_hits = 0
    resps = job_reqs.get("responsibilities", [])
    if resps:
        for r in resps:
            r_words = [w for w in r.lower().split() if len(w) > 3]
            if any(w in cand_text for w in r_words):
                resp_hits += 1
        responsibility_score = min(100.0, max(50.0, (resp_hits / len(resps)) * 100.0))
    else:
        responsibility_score = semantic_score

    # 4. Keywords Score (5%)
    keyword_score = semantic_score

    # 5. Location Score (5%)
    req_loc = (job_reqs.get("location") or "").lower()
    cand_loc = (candidate.location or "").lower()

    if not req_loc or "remote" in req_loc or req_loc in cand_loc or cand_loc in req_loc:
        location_score = 100.0
    else:
        location_score = 60.0

    # 6. Education Score (5%)
    education_score = 90.0 if candidate.education else 70.0

    # Weighted Overall Score Calculation
    overall = (
        skills_score * 0.35
        + experience_score * 0.20
        + semantic_score * 0.20
        + responsibility_score * 0.10
        + keyword_score * 0.05
        + location_score * 0.05
        + education_score * 0.05
    )
    final_overall = round(overall, 1)

    return {
        "overall_score": final_overall,
        "skills_score": round(skills_score, 1),
        "experience_score": round(experience_score, 1),
        "semantic_score": round(semantic_score, 1),
        "responsibility_score": round(responsibility_score, 1),
        "keyword_score": round(keyword_score, 1),
        "location_score": round(location_score, 1),
        "education_score": round(education_score, 1),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "matched_keywords": matched_skills,
        "missing_keywords": missing_skills,
    }


def detect_silver_medalist(db: Session, candidate_id: uuid.UUID, current_job_id: uuid.UUID) -> Tuple[bool, Optional[uuid.UUID], Optional[str], Optional[str], Optional[float]]:
    """
    Identifies if a candidate is a Silver Medalist based on prior application history.
    Criteria: Previously shortlisted, interviewed, selected, or scored high ATS score (>= 75.0%).
    """
    past_apps = (
        db.query(Application)
        .options(joinedload(Application.job))
        .filter(Application.candidate_id == candidate_id, Application.job_id != current_job_id)
        .order_by(Application.created_at.desc())
        .all()
    )

    for app in past_apps:
        status_lower = (app.status.value if hasattr(app.status, "value") else str(app.status)).lower()
        ats_sc = app.ats_score or app.overall_score or 0.0

        if status_lower in ("shortlisted", "interview", "under_review", "selected") or ats_sc >= 75.0:
            job_title = app.job.title if app.job else "Previous Role"
            return True, app.job_id, job_title, status_lower.title(), round(ats_sc, 1)

    return False, None, None, None, None


def run_rediscovery_for_job(db: Session, job_id: uuid.UUID, top_n: int = 50) -> TalentRediscoveryRun:
    """
    Executes talent rediscovery pipeline for a job.
    Retrieves candidate pool, calculates weighted match scores, detects Silver Medalists,
    updates progress in Redis, and persists top ranked results in PostgreSQL without duplicates.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise NotFoundError("Job not found for talent rediscovery.")

    # 1. Retrieve or create run record
    run = (
        db.query(TalentRediscoveryRun)
        .filter(TalentRediscoveryRun.job_id == job_id)
        .order_by(TalentRediscoveryRun.created_at.desc())
        .first()
    )

    if not run or run.status in (RediscoveryRunStatus.completed, RediscoveryRunStatus.failed):
        run = TalentRediscoveryRun(
            job_id=job_id,
            status=RediscoveryRunStatus.processing,
            started_at=datetime.now(timezone.utc),
        )
        db.add(run)
        db.flush()

    run.status = RediscoveryRunStatus.processing
    db.commit()

    # Update Redis progress key
    redis_progress_key = f"rediscovery:job:{job_id}:progress"
    cache_set_json(redis_progress_key, {"processed": 0, "total": 0, "status": "PROCESSING", "matched": 0})

    try:
        job_reqs = extract_and_normalize_job_requirements(job)
        candidates = get_eligible_candidate_pool(db, job)

        total_count = len(candidates)
        run.total_candidates = total_count

        scored_results = []
        silver_count = 0

        for idx, candidate in enumerate(candidates, start=1):
            match_data = calculate_candidate_rediscovery_score(candidate, job_reqs)
            is_silver, prev_j_id, prev_j_title, prev_status, prev_ats = detect_silver_medalist(db, candidate.id, job_id)

            if is_silver:
                silver_count += 1
                explanation = f"Silver Medalist: Previously applied for '{prev_j_title}' ({prev_status}) and is now a {match_data['overall_score']}% match for {job.title}."
            else:
                explanation = f"Candidate profile demonstrates a {match_data['overall_score']}% match for {job.title} based on skill and experience alignment."

            scored_results.append(
                {
                    "candidate_id": candidate.id,
                    "cand_name": candidate.user.name if (candidate.user and candidate.user.name) else "Candidate",
                    "match_data": match_data,
                    "is_silver": is_silver,
                    "prev_j_id": prev_j_id,
                    "prev_j_title": prev_j_title,
                    "prev_status": prev_status,
                    "prev_ats": prev_ats,
                    "explanation": explanation,
                }
            )

            # Periodically update Redis progress
            if idx % 10 == 0 or idx == total_count:
                cache_set_json(
                    redis_progress_key,
                    {
                        "processed": idx,
                        "total": total_count,
                        "status": "PROCESSING",
                        "matched": len(scored_results),
                    },
                )

        # Sort candidates descending by overall score
        scored_results.sort(key=lambda x: x["match_data"]["overall_score"], reverse=True)

        # Keep top N results above threshold
        top_candidates = scored_results[:top_n]

        # 2. Persist to PostgreSQL (upsert logic to enforce UNIQUE(job_id, candidate_id))
        for rank, res_item in enumerate(top_candidates, start=1):
            cand_id = res_item["candidate_id"]
            md = res_item["match_data"]

            existing_result = (
                db.query(TalentRediscoveryResult)
                .filter(TalentRediscoveryResult.job_id == job_id, TalentRediscoveryResult.candidate_id == cand_id)
                .first()
            )

            if not existing_result:
                existing_result = TalentRediscoveryResult(
                    job_id=job_id,
                    candidate_id=cand_id,
                )
                db.add(existing_result)

            existing_result.overall_score = md["overall_score"]
            existing_result.skills_score = md["skills_score"]
            existing_result.experience_score = md["experience_score"]
            existing_result.semantic_score = md["semantic_score"]
            existing_result.responsibility_score = md["responsibility_score"]
            existing_result.keyword_score = md["keyword_score"]
            existing_result.location_score = md["location_score"]
            existing_result.education_score = md["education_score"]
            existing_result.rank = rank
            existing_result.is_silver_medalist = res_item["is_silver"]
            existing_result.previous_job_id = res_item["prev_j_id"]
            existing_result.previous_job_title = res_item["prev_j_title"]
            existing_result.previous_application_status = res_item["prev_status"]
            existing_result.previous_ats_score = res_item["prev_ats"]
            existing_result.matched_skills = json.dumps(md["matched_skills"])
            existing_result.missing_skills = json.dumps(md["missing_skills"])
            existing_result.matched_keywords = json.dumps(md["matched_keywords"])
            existing_result.missing_keywords = json.dumps(md["missing_keywords"])
            existing_result.match_explanation = res_item["explanation"]
            existing_result.status = "rediscovered"

        run.processed_candidates = total_count
        run.matched_candidates = len(top_candidates)
        run.status = RediscoveryRunStatus.completed
        run.completed_at = datetime.now(timezone.utc)

        # Notify recruiter
        if job.recruiter_id:
            rec_notif = Notification(
                user_id=job.recruiter_id,
                title="Talent Rediscovery Completed",
                message=f"AI rediscovered {len(top_candidates)} top candidate matches for '{job.title}', including {silver_count} Silver Medalists.",
                type="talent_rediscovery",
            )
            db.add(rec_notif)

        db.commit()

        # Update final Redis progress
        cache_set_json(
            redis_progress_key,
            {
                "processed": total_count,
                "total": total_count,
                "status": "COMPLETED",
                "matched": len(top_candidates),
                "silver_medalists": silver_count,
            },
        )

        logger.info(f"Talent Rediscovery completed for job {job_id}: {len(top_candidates)} candidates ranked.")
        return run

    except Exception as err:
        logger.exception(f"Talent Rediscovery failed for job {job_id}: {err}")
        run.status = RediscoveryRunStatus.failed
        run.error_message = str(err)
        db.commit()
        cache_set_json(redis_progress_key, {"status": "FAILED", "error": str(err)})
        raise err


def trigger_rediscovery_async(job_id: uuid.UUID) -> None:
    """Triggers background talent rediscovery in a non-blocking background thread."""

    def _worker():
        db = SessionLocal()
        try:
            run_rediscovery_for_job(db, job_id)
        except Exception as e:
            logger.error(f"Background talent rediscovery task error: {e}")
        finally:
            db.close()

    thread = threading.Thread(target=_worker, daemon=True)
    thread.start()
