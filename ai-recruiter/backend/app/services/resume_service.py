"""
resume_service.py — orchestrates the resume upload pipeline:
validate -> save file -> extract text -> run NLP -> upsert CandidateProfile
and the candidate's extracted skills.
"""
import os

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.candidate import CandidateProfile, CandidateSkill, Skill
from app.nlp.resume_parser import extract_resume_text
from app.nlp.skill_extractor import parse_resume_fields
from app.nlp.skills_data import SKILLS_KB
from app.utils.file_validation import secure_filename, validate_extension, validate_size


def seed_skills(db: Session) -> None:
    """Ensure every skill in the knowledge base exists as a row in `skills`.
    Idempotent — safe to call on every startup."""
    existing = {s.skill_name for s in db.query(Skill.skill_name).all()}
    new_skills = [
        Skill(skill_name=name, category=meta.get("category"))
        for name, meta in SKILLS_KB.items()
        if name not in existing
    ]
    if new_skills:
        db.add_all(new_skills)
        db.commit()


def _compute_profile_score(fields: dict) -> int:
    """Computes a realistic ATS Resume Readiness & Quality Score (0-100) based on
    contact info, skill volume, experience duration, education, section structure, and impact metrics."""
    score = 0

    # 1. Contact Information & Metadata (Max 15 pts)
    if fields.get("name"): score += 3
    if fields.get("email"): score += 3
    if fields.get("phone"): score += 3
    if fields.get("location") or fields.get("address"): score += 3
    if fields.get("address"): score += 3

    # 2. Technical Skill Volume & Diversity (Max 25 pts)
    skills = fields.get("skills", [])
    if len(skills) >= 15: score += 25
    elif len(skills) >= 10: score += 18
    elif len(skills) >= 5: score += 12
    elif len(skills) >= 1: score += 5

    # 3. Work Experience & Impact Metrics (Max 25 pts)
    exp_years = fields.get("experience_years") or 0.0
    work_exp = fields.get("work_experience") or ""
    orgs = fields.get("organizations") or []
    metrics = fields.get("metrics_and_impact") or []

    if work_exp or orgs: score += 8
    if exp_years >= 5.0: score += 10
    elif exp_years >= 3.0: score += 7
    elif exp_years >= 1.0: score += 4
    elif exp_years > 0.0: score += 2

    # Bonus for quantifiable metrics & impact numbers (percentages, load reductions, user counts)
    if len(metrics) >= 3: score += 7
    elif len(metrics) >= 1: score += 4

    # 4. ATS Standard Section Structure (Max 15 pts)
    ats_sections = fields.get("ats_sections") or {}
    if ats_sections.get("has_skills"): score += 3
    if ats_sections.get("has_experience"): score += 3
    if ats_sections.get("has_education"): score += 3
    if ats_sections.get("has_summary"): score += 3
    if ats_sections.get("has_certifications"): score += 3

    # 5. Education, Certifications & Summary Depth (Max 20 pts)
    if fields.get("education"): score += 7
    certs = fields.get("certifications") or []
    if certs: score += 5

    summary = fields.get("summary") or ""
    summary_words = len(summary.split())
    if summary_words >= 25: score += 8
    elif summary_words >= 10: score += 4

    # Apply penalty multiplier if critical ATS sections (Experience or Skills) are missing completely
    final_score = float(score)
    if not ats_sections.get("has_skills") and len(skills) < 3:
        final_score *= 0.8
    if not ats_sections.get("has_experience") and not work_exp:
        final_score *= 0.8

    return max(0, min(int(round(final_score)), 100))


def save_uploaded_file(file_bytes: bytes, original_filename: str) -> tuple[str, str]:
    """Validates and writes the file to disk. Returns (absolute_path, safe_filename)."""
    validate_extension(original_filename)
    validate_size(len(file_bytes), settings.MAX_UPLOAD_SIZE_MB)

    safe_name = secure_filename(original_filename)
    upload_dir = settings.UPLOAD_DIR
    os.makedirs(upload_dir, exist_ok=True)

    file_path = os.path.join(upload_dir, safe_name)
    with open(file_path, "wb") as f:
        f.write(file_bytes)

    return file_path, safe_name


def process_resume(db: Session, user_id, file_bytes: bytes, original_filename: str) -> CandidateProfile:
    """
    Full pipeline for one uploaded resume: save -> extract text -> parse
    fields -> upsert the candidate's profile and skill links.
    """
    file_path, safe_name = save_uploaded_file(file_bytes, original_filename)

    raw_text = extract_resume_text(file_bytes, original_filename)
    fields = parse_resume_fields(raw_text)

    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == user_id).first()
    is_new = False
    if not profile:
        profile = CandidateProfile(user_id=user_id)
        db.add(profile)
        is_new = True

    new_phone = fields.get("phone")
    new_location = fields.get("location")
    new_address = fields.get("address")
    new_summary = fields.get("summary")
    new_exp_years = fields.get("experience_years")
    new_education = fields.get("education")
    new_work_exp = fields.get("work_experience")

    profile.resume_path = file_path
    profile.resume_text = raw_text
    profile.resume_original_filename = original_filename

    profile.phone = new_phone or profile.phone

    # Location: Update location. If candidate has a previous location that is different, combine them (e.g. Bangalore / Salem)
    if new_location:
        if profile.location and not is_new and profile.location.lower() != new_location.lower() and new_location.lower() not in profile.location.lower():
            profile.location = f"{new_location} / {profile.location}"
        else:
            profile.location = new_location
    elif not profile.location:
        profile.location = None

    if new_address:
        profile.address = new_address

    profile.summary = new_summary or profile.summary

    # Accumulate experience years (take max of new vs existing)
    old_years = profile.experience_years or 0.0
    parsed_years = new_exp_years or 0.0
    profile.experience_years = max(parsed_years, old_years) if (parsed_years or old_years) else None

    profile.education = new_education or profile.education

    # Work Experience & Companies: MERGE new and existing work experience so company names from BOTH resumes are displayed
    if new_work_exp:
        if profile.work_experience and not is_new and new_work_exp.strip().lower() not in profile.work_experience.lower():
            profile.work_experience = f"{new_work_exp.strip()}\n\n{profile.work_experience.strip()}"
        else:
            profile.work_experience = new_work_exp.strip()

    profile.ai_summary = None
    profile.profile_score = _compute_profile_score(fields)

    db.flush()  # ensure profile.id is populated before linking skills

    seed_skills(db)
    # Merge existing skills with new skills so skills from all uploaded resumes accumulate
    existing_skills = [cs.skill.skill_name for cs in profile.candidate_skills] if (profile.candidate_skills and not is_new) else []
    merged_skills = sorted(list(set(existing_skills + (fields.get("skills") or []))))
    _sync_candidate_skills(db, profile, merged_skills)

    db.commit()
    db.refresh(profile)
    return profile


def _sync_candidate_skills(db: Session, profile: CandidateProfile, skill_names: list[str]) -> None:
    """Replace the candidate's skill links with the freshly extracted set, auto-creating new Skill records if needed."""
    db.query(CandidateSkill).filter(CandidateSkill.candidate_id == profile.id).delete()

    if not skill_names:
        return

    clean_skill_names = [s.strip() for s in skill_names if s and isinstance(s, str) and s.strip()]
    if not clean_skill_names:
        return

    existing_skills = db.query(Skill).all()
    skill_map = {s.skill_name.lower(): s for s in existing_skills}

    target_skill_ids = set()
    for name in clean_skill_names:
        name_lower = name.lower()
        if name_lower in skill_map:
            target_skill_ids.add(skill_map[name_lower].id)
        else:
            new_skill = Skill(skill_name=name, category="General")
            db.add(new_skill)
            db.flush()
            skill_map[name_lower] = new_skill
            target_skill_ids.add(new_skill.id)

    for skill_id in target_skill_ids:
        db.add(CandidateSkill(candidate_id=profile.id, skill_id=skill_id))
    db.flush()


def update_candidate_profile(
    db: Session,
    profile: CandidateProfile,
    update_data: dict,
    user_name: str = "",
    user_email: str = "",
) -> CandidateProfile:
    """Updates candidate profile fields, re-syncs skills if provided, and recalculates ATS score."""
    if "phone" in update_data and update_data["phone"] is not None:
        profile.phone = update_data["phone"]
    if "location" in update_data and update_data["location"] is not None:
        profile.location = update_data["location"]
    if "address" in update_data and update_data["address"] is not None:
        profile.address = update_data["address"]
    if "summary" in update_data and update_data["summary"] is not None:
        profile.summary = update_data["summary"]
    if "experience_years" in update_data and update_data["experience_years"] is not None:
        profile.experience_years = update_data["experience_years"]
    if "education" in update_data and update_data["education"] is not None:
        profile.education = update_data["education"]
    if "work_experience" in update_data and update_data["work_experience"] is not None:
        profile.work_experience = update_data["work_experience"]

    # LinkedIn-Style Professional Profile Fields
    for field in ["profile_photo", "headline", "current_role", "certifications", "portfolio_url", "linkedin_url", "github_url", "other_links"]:
        if field in update_data and update_data[field] is not None:
            setattr(profile, field, update_data[field])

    if "skills" in update_data and update_data["skills"] is not None:
        seed_skills(db)
        _sync_candidate_skills(db, profile, update_data["skills"])

    db.flush()

    active_skills = [cs.skill.skill_name for cs in profile.candidate_skills]
    fields = {
        "name": user_name or "Candidate",
        "email": user_email,
        "phone": profile.phone,
        "location": profile.location,
        "address": profile.address,
        "skills": active_skills,
        "experience_years": profile.experience_years,
        "education": profile.education,
        "summary": profile.summary,
        "work_experience": profile.work_experience,
    }
    profile.profile_score = _compute_profile_score(fields)

    db.commit()
    db.refresh(profile)
    return profile


def delete_candidate_profile(db: Session, profile: CandidateProfile) -> None:
    """Deletes candidate profile and removes the stored resume file if present."""
    if profile.resume_path and os.path.exists(profile.resume_path):
        try:
            os.remove(profile.resume_path)
        except OSError:
            pass

    db.delete(profile)
    db.commit()
