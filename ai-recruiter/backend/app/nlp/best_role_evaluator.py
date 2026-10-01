"""
best_role_evaluator.py — Evaluates a candidate's parsed profile against all
available active job postings and industry tech domains to identify the single
best suited job position and role match.
"""
from dataclasses import dataclass, field
import uuid
from sqlalchemy.orm import Session, joinedload

from app.models.user import User
from app.models.candidate import CandidateProfile, CandidateSkill
from app.models.job import Job, JobSkill, JobStatus
from app.ml.ranking import compute_match
from app.nlp.domain_data import DOMAINS_KB
from app.nlp.domain_evaluator import evaluate_domain_ats_score


@dataclass
class BestRoleResult:
    best_role_title: str
    best_match_score: int
    matched_skills: list[str] = field(default_factory=list)
    job_id: str | None = None
    job_title: str | None = None
    job_location: str | None = None
    is_active_job: bool = False
    explanation: str = ""
    matched_roles: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "best_role_title": self.best_role_title,
            "best_match_score": self.best_match_score,
            "matched_skills": self.matched_skills,
            "job_id": self.job_id,
            "job_title": self.job_title,
            "job_location": self.job_location,
            "is_active_job": self.is_active_job,
            "explanation": self.explanation,
            "matched_roles": self.matched_roles,
        }


def find_best_suited_position(
    db: Session, 
    candidate_user_id: uuid.UUID = None, 
    profile: CandidateProfile = None,
    published_jobs: list = None,
) -> BestRoleResult:
    """Scans all published job postings and industry domains to determine the #1 best suited role and matching roles."""
    if not profile and candidate_user_id:
        profile = (
            db.query(CandidateProfile)
            .options(joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill))
            .filter(CandidateProfile.user_id == candidate_user_id)
            .first()
        )

    if not profile:
        return BestRoleResult(
            best_role_title="General Candidate",
            best_match_score=0,
            explanation="Upload your resume to identify your best suited job role.",
            matched_roles=[],
        )

    candidate_skills = [cs.skill.skill_name for cs in profile.candidate_skills if cs and cs.skill]
    resume_text = profile.resume_text or profile.summary or ""

    if not candidate_skills and resume_text:
        try:
            from app.nlp.skill_extractor import extract_skills
            candidate_skills = extract_skills(resume_text)
        except Exception:
            candidate_skills = []

    # 1. Evaluate against all published active real jobs in the system (excluding generic talent pools)
    if published_jobs is None:
        published_jobs = (
            db.query(Job)
            .options(joinedload(Job.job_skills).joinedload(JobSkill.skill))
            .filter(Job.status == JobStatus.published)
            .all()
        )

    active_real_jobs = [
        j for j in published_jobs
        if j.title and "talent pool" not in j.title.lower()
    ]

    job_results = []
    for job in active_real_jobs:
        try:
            match_res = compute_match(profile, job, include_semantic=False)
            score = int(round(match_res.final_score))
            matched_s = match_res.matched_required_skills + match_res.matched_preferred_skills
            job_results.append({
                "title": job.title,
                "score": score,
                "job_id": str(job.id),
                "job_title": job.title,
                "job_location": job.location,
                "is_active_job": True,
                "matched_skills": matched_s[:8],
                "explanation": f"Matches open job requisition '{job.title}' with {score}% alignment.",
                "type": "posted_job",
            })
        except Exception as e:
            continue

    job_results.sort(key=lambda x: x["score"], reverse=True)

    # 2. Evaluate against all industry tech domains
    domain_results = []
    for domain_key, domain_meta in DOMAINS_KB.items():
        try:
            res = evaluate_domain_ats_score(candidate_skills, resume_text, domain_key, calculate_extras=False)
            domain_results.append({
                "title": domain_meta["title"],
                "score": int(res.domain_score),
                "job_id": None,
                "job_title": domain_meta["title"],
                "job_location": None,
                "is_active_job": False,
                "matched_skills": res.matched_required_skills[:8],
                "explanation": f"Matches industry {domain_meta['title']} standard with {res.domain_score}% fit.",
                "type": "domain_role",
            })
        except Exception:
            continue

    domain_results.sort(key=lambda x: x["score"], reverse=True)

    # 3. Compile top ranked matched roles list
    all_matched_roles = []
    seen_titles = set()
    for item in (job_results + domain_results):
        norm_title = item["title"].strip().lower()
        if norm_title not in seen_titles and item["score"] >= 30:
            seen_titles.add(norm_title)
            all_matched_roles.append(item)
    all_matched_roles.sort(key=lambda x: x["score"], reverse=True)

    best_job = job_results[0] if job_results else None
    top_domain = domain_results[0] if domain_results else None

    # Prioritize active open positions when the match is strong
    if best_job and (best_job["score"] >= 50 or (top_domain and best_job["score"] >= top_domain["score"] - 10 and best_job["score"] >= 40)):
        primary_match = best_job
    elif top_domain:
        primary_match = top_domain
    elif all_matched_roles:
        primary_match = all_matched_roles[0]
    else:
        primary_match = {
            "title": profile.current_role or "Software Professional",
            "score": 50,
            "job_id": None,
            "job_title": profile.current_role or "Software Professional",
            "job_location": None,
            "is_active_job": False,
            "matched_skills": candidate_skills[:5],
            "explanation": "General technical candidate profile.",
            "type": "domain_role",
        }

    top_roles = all_matched_roles[:3]
    if not any(r["title"].lower() == primary_match["title"].lower() for r in top_roles):
        top_roles.insert(0, primary_match)

    return BestRoleResult(
        best_role_title=primary_match["title"],
        best_match_score=primary_match["score"],
        matched_skills=primary_match.get("matched_skills", []),
        job_id=primary_match.get("job_id"),
        job_title=primary_match.get("job_title"),
        job_location=primary_match.get("job_location"),
        is_active_job=primary_match.get("is_active_job", False),
        explanation=primary_match.get("explanation", ""),
        matched_roles=top_roles,
    )
