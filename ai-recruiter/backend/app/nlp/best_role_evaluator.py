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
        }


def find_best_suited_position(db: Session, candidate_user_id: uuid.UUID) -> BestRoleResult:
    """Scans all published job postings and industry domains to determine the #1 best suited role."""
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
        )

    candidate_skills = [cs.skill.skill_name for cs in profile.candidate_skills]
    resume_text = profile.resume_text or profile.summary or ""

    # 1. Evaluate against all industry tech domains
    domain_results = []
    for domain_key, domain_meta in DOMAINS_KB.items():
        res = evaluate_domain_ats_score(candidate_skills, resume_text, domain_key)
        domain_results.append((res.domain_score, domain_meta["title"], res))

    domain_results.sort(key=lambda x: x[0], reverse=True)
    top_domain_score, top_domain_title, top_domain_eval = domain_results[0] if domain_results else (0, "Full Stack Developer", None)

    # 2. Evaluate against all published active job postings in the system
    published_jobs = (
        db.query(Job)
        .options(joinedload(Job.job_skills).joinedload(JobSkill.skill))
        .filter(Job.status == JobStatus.published)
        .all()
    )

    job_results = []
    for job in published_jobs:
        match_res = compute_match(profile, job)
        job_results.append((int(round(match_res.final_score)), job, match_res))

    job_results.sort(key=lambda x: x[0], reverse=True)

    # 3. Determine overall best fit (comparing active jobs vs tech domains)
    best_job_score, best_job, best_job_match = job_results[0] if job_results else (0, None, None)

    if best_job and best_job_score >= top_domain_score and best_job_score >= 50:
        # Top match is an actual active open job posting
        matched_skills = best_job_match.matched_required_skills + best_job_match.matched_preferred_skills
        return BestRoleResult(
            best_role_title=best_job.title,
            best_match_score=best_job_score,
            matched_skills=matched_skills[:8],
            job_id=str(best_job.id),
            job_title=best_job.title,
            job_location=best_job.location,
            is_active_job=True,
            explanation=f"Your resume matches the open position '{best_job.title}' with a strong {best_job_score}% alignment.",
        )
    else:
        # Top match is an industry domain role
        matched_skills = top_domain_eval.matched_required_skills if top_domain_eval else candidate_skills[:5]
        return BestRoleResult(
            best_role_title=top_domain_title,
            best_match_score=top_domain_score,
            matched_skills=matched_skills[:8],
            job_id=str(best_job.id) if best_job else None,
            job_title=best_job.title if best_job else None,
            job_location=best_job.location if best_job else None,
            is_active_job=False,
            explanation=f"Based on your extracted skills and technical experience, your resume is best suited for a {top_domain_title} position ({top_domain_score}% Match).",
        )
