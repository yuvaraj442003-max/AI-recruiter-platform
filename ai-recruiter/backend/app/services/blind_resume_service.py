"""
blind_resume_service.py — Sanitization & Anonymization Engine for Blind Screening Mode.
Generates non-identifying candidate codes (e.g. CAND-10452), strips personal contact info/links/names,
masks institution names into degree/field representations, and creates identity-safe AI prompts.
"""
import re
import uuid
import hashlib
from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session

from app.models.blind_screening import BlindScreeningCandidate, BlindScreeningConfig
from app.models.candidate import CandidateProfile


def generate_candidate_code(candidate_id: uuid.UUID, job_id: uuid.UUID) -> str:
    """Generates a stable, non-identifying candidate code e.g. CAND-10452 based on UUID hashes."""
    combined = f"{candidate_id}:{job_id}"
    hash_int = int(hashlib.md5(combined.encode("utf-8")).hexdigest(), 16)
    code_num = 10000 + (hash_int % 89999)
    return f"CAND-{code_num}"


def get_or_create_blind_candidate(db: Session, job_id: uuid.UUID, candidate_id: uuid.UUID) -> BlindScreeningCandidate:
    """Retrieves or creates a BlindScreeningCandidate record with candidate code."""
    blind_cand = (
        db.query(BlindScreeningCandidate)
        .filter(BlindScreeningCandidate.job_id == job_id, BlindScreeningCandidate.candidate_id == candidate_id)
        .first()
    )

    if not blind_cand:
        code = generate_candidate_code(candidate_id, job_id)
        # Ensure code uniqueness for this job
        existing_code = (
            db.query(BlindScreeningCandidate)
            .filter(BlindScreeningCandidate.job_id == job_id, BlindScreeningCandidate.candidate_code == code)
            .first()
        )
        if existing_code:
            # Fallback incremental offset
            alt_num = 10000 + (uuid.uuid4().int % 89999)
            code = f"CAND-{alt_num}"

        blind_cand = BlindScreeningCandidate(
            job_id=job_id,
            candidate_id=candidate_id,
            candidate_code=code,
            screening_status="pending",
        )
        db.add(blind_cand)
        db.commit()
        db.refresh(blind_cand)

    return blind_cand


def get_or_create_blind_config(db: Session, job_id: uuid.UUID) -> BlindScreeningConfig:
    """Retrieves or creates default job blind screening settings."""
    config = db.query(BlindScreeningConfig).filter(BlindScreeningConfig.job_id == job_id).first()
    if not config:
        config = BlindScreeningConfig(
            job_id=job_id,
            enabled=True,
            hide_name=True,
            hide_photo=True,
            hide_age=True,
            hide_gender=True,
            hide_location=True,
            hide_college=True,
            hide_email=True,
            hide_phone=True,
            hide_address=True,
            hide_social_links=True,
            reveal_policy="reveal_after_shortlist",
        )
        db.add(config)
        db.commit()
        db.refresh(config)
    return config


def sanitize_education_text(raw_education: Optional[str]) -> List[Dict[str, str]]:
    """
    Sanitizes education history by converting college names into degree and field of study.
    E.g., "B.E. Computer Science from XYZ College, Chennai" -> [{"degree": "Bachelor's Degree", "field": "Computer Science"}].
    """
    if not raw_education:
        return [{"degree": "Higher Education", "field": "Relevant Domain"}]

    items = []
    lines = [l.strip() for l in raw_education.split("\n") if l.strip()]

    degree_map = {
        "b.e": ("Bachelor's Degree", "Computer Science / Engineering"),
        "b.tech": ("Bachelor's Degree", "Information Technology / CS"),
        "bs": ("Bachelor's Degree", "Computer Science"),
        "bachelor": ("Bachelor's Degree", "Relevant Field"),
        "m.tech": ("Master's Degree", "Engineering"),
        "ms": ("Master's Degree", "Computer Science"),
        "m.s": ("Master's Degree", "Computer Science"),
        "master": ("Master's Degree", "Relevant Field"),
        "phd": ("Doctorate (Ph.D.)", "Specialized Field"),
        "diploma": ("Diploma / Associate", "Technical Studies"),
    }

    raw_lower = raw_education.lower()
    found_degree = False

    for key, (deg, fld) in degree_map.items():
        if key in raw_lower:
            items.append({"degree": deg, "field": fld})
            found_degree = True
            break

    if not found_degree:
        items.append({"degree": "Bachelor's / Master's Degree", "field": "Relevant Technical Domain"})

    return items


def sanitize_resume_text(
    resume_text: str,
    candidate_name: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
) -> str:
    """
    Strips email addresses, phone numbers, social links, URLs, personal addresses,
    candidate names, and college names from parsed resume text for Blind Resume representation.
    """
    if not resume_text:
        return ""

    sanitized = resume_text

    # 1. Strip candidate name if provided
    if candidate_name and len(candidate_name.strip()) > 2:
        name_parts = candidate_name.strip().split()
        for part in name_parts:
            if len(part) > 2:
                sanitized = re.sub(re.escape(part), "[REDACTED]", sanitized, flags=re.IGNORECASE)

    # 2. Strip emails
    if email:
        sanitized = re.sub(re.escape(email), "[REDACTED_EMAIL]", sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r"[\w\.-]+@[\w\.-]+\.\w+", "[REDACTED_EMAIL]", sanitized)

    # 3. Strip phone numbers
    if phone:
        sanitized = re.sub(re.escape(phone), "[REDACTED_PHONE]", sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r"(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", "[REDACTED_PHONE]", sanitized)

    # 4. Strip URLs / Social Links
    sanitized = re.sub(r"https?://\S+", "[REDACTED_URL]", sanitized)
    sanitized = re.sub(r"www\.\S+", "[REDACTED_URL]", sanitized)
    sanitized = re.sub(r"linkedin\.com/\S+", "[REDACTED_LINKEDIN]", sanitized)
    sanitized = re.sub(r"github\.com/\S+", "[REDACTED_GITHUB]", sanitized)

    # 5. Mask college / university names pattern
    sanitized = re.sub(r"(college|university|institute|school) of \w+", "Accredited Higher Education Institution", sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(r"\b\w+ (college|university|institute)\b", "Accredited Higher Education Institution", sanitized, flags=re.IGNORECASE)

    return sanitized


def build_sanitized_ai_prompt(
    candidate_code: str,
    experience_years: float,
    skills: List[str],
    work_exp_summary: str,
    job_title: str,
) -> Dict[str, Any]:
    """
    Builds a sanitized JSON object for LLM evaluation prompts.
    Excludes all identity fields (no name, photo, age, gender, location, college).
    """
    return {
        "candidate_code": candidate_code,
        "experience_years": experience_years,
        "normalized_skills": skills,
        "work_experience_summary": work_exp_summary,
        "target_job": job_title,
    }
