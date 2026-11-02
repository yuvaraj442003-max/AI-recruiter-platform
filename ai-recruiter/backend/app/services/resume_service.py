"""
resume_service.py — orchestrates the resume upload pipeline:
validate -> save file -> extract text -> run NLP -> upsert CandidateProfile
and the candidate's extracted skills.
"""
import hashlib
import logging
import os
import uuid
from typing import Optional

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.candidate import CandidateProfile, CandidateSkill, Skill
from app.nlp.resume_parser import extract_resume_text
from app.nlp.skill_extractor import parse_resume_fields
from app.nlp.skills_data import SKILLS_KB
from app.utils.file_validation import secure_filename, validate_extension, validate_size

logger = logging.getLogger(__name__)


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


def process_resume(
    db: Session,
    user_id,
    file_bytes: bytes,
    original_filename: str,
    recruiter_id: Optional[uuid.UUID] = None,
    source: Optional[str] = None,
) -> CandidateProfile:
    """
    Full pipeline for one uploaded resume: save -> extract text -> parse
    fields -> upsert the candidate's profile and skill links -> auto-generate portfolio.
    """
    file_path, safe_name = save_uploaded_file(file_bytes, original_filename)
    resume_hash = hashlib.sha256(file_bytes).hexdigest()

    raw_text = extract_resume_text(file_bytes, original_filename)
    fields = parse_resume_fields(raw_text)
    extracted_skills = fields.get("skills") or []

    profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == user_id).first()
    if not profile:
        profile = CandidateProfile(user_id=user_id)
        db.add(profile)

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
    profile.resume_hash = resume_hash

    profile.phone = new_phone or profile.phone
    profile.location = new_location or profile.location
    profile.address = new_address or profile.address
    profile.summary = new_summary or profile.summary
    profile.experience_years = new_exp_years if new_exp_years is not None else profile.experience_years
    profile.education = new_education or profile.education
    profile.work_experience = new_work_exp or profile.work_experience

    # Extract rich structured fields from resume as single source of truth
    from app.services.resume_autofill_service import extract_candidate_autofill_fields
    autofill = {}
    try:
        autofill = extract_candidate_autofill_fields(file_bytes, original_filename)
    except Exception as e:
        logger.warning(f"autofill extraction in process_resume failed: {e}")

    extracted_name = autofill.get("name") or fields.get("name")
    if extracted_name and isinstance(extracted_name, str) and len(extracted_name.strip()) >= 2:
        clean_name = extracted_name.strip()
        profile.full_name = clean_name
        from app.models.user import User
        user_obj = profile.user or db.get(User, user_id)
        if user_obj:
            user_obj.name = clean_name
            db.add(user_obj)

    if autofill.get("certifications"):
        profile.certifications = autofill.get("certifications")
    elif extracted_certs:
        profile.certifications = ", ".join(extracted_certs) if isinstance(extracted_certs, list) else str(extracted_certs)

    if autofill.get("summary"):
        profile.summary = autofill.get("summary")

    if autofill.get("experience_years") is not None:
        try:
            profile.experience_years = float(autofill["experience_years"])
        except (ValueError, TypeError):
            pass

    profile.headline = autofill.get("headline") or fields.get("headline") or profile.headline
    profile.current_role = autofill.get("current_role") or fields.get("current_role") or fields.get("headline") or profile.current_role
    if not profile.headline and extracted_skills:
        profile.headline = f"{extracted_skills[0]} Specialist"
        profile.current_role = profile.headline

    if autofill.get("location") or fields.get("location"):
        profile.location = autofill.get("location") or fields.get("location")
    if autofill.get("phone") or fields.get("phone"):
        profile.phone = autofill.get("phone") or fields.get("phone")

    # Academic credentials extracted from resume
    if autofill.get("college"):
        profile.college_name = autofill.get("college")
    if autofill.get("degree"):
        profile.degree = autofill.get("degree")
    if autofill.get("branch"):
        profile.branch = autofill.get("branch")
    if autofill.get("graduation_year"):
        try:
            profile.graduation_year = int(str(autofill.get("graduation_year")).strip())
        except (ValueError, TypeError):
            pass
    if autofill.get("cgpa"):
        try:
            profile.cgpa = float(str(autofill.get("cgpa")).strip())
        except (ValueError, TypeError):
            pass

    # 12th Grade
    if autofill.get("twelfth_school"):
        profile.twelfth_school = autofill.get("twelfth_school")
    if autofill.get("twelfth_board"):
        profile.twelfth_board = autofill.get("twelfth_board")
    if autofill.get("twelfth_year"):
        try:
            profile.twelfth_year = int(str(autofill.get("twelfth_year")).strip())
        except (ValueError, TypeError):
            pass
    if autofill.get("twelfth_percentage"):
        try:
            profile.twelfth_percentage = float(str(autofill.get("twelfth_percentage")).strip())
        except (ValueError, TypeError):
            pass

    # 10th Grade
    if autofill.get("tenth_school"):
        profile.tenth_school = autofill.get("tenth_school")
    if autofill.get("tenth_board"):
        profile.tenth_board = autofill.get("tenth_board")
    if autofill.get("tenth_year"):
        try:
            profile.tenth_year = int(str(autofill.get("tenth_year")).strip())
        except (ValueError, TypeError):
            pass
    if autofill.get("tenth_percentage"):
        try:
            profile.tenth_percentage = float(str(autofill.get("tenth_percentage")).strip())
        except (ValueError, TypeError):
            pass

    profile.linkedin_url = autofill.get("linkedin_url") or fields.get("linkedin_url") or profile.linkedin_url
    profile.github_url = autofill.get("github_url") or fields.get("github_url") or profile.github_url
    profile.portfolio_url = autofill.get("portfolio_url") or fields.get("portfolio_url") or profile.portfolio_url

    if recruiter_id:
        profile.created_by_recruiter_id = recruiter_id
    if source:
        profile.source = source

    fields["resume_text"] = raw_text
    from app.ai.resume_summarizer import generate_resume_summary
    try:
        ai_res = generate_resume_summary(fields)
        profile.ai_summary = ai_res.get("summary")
    except Exception:
        profile.ai_summary = None

    profile.profile_score = _compute_profile_score(fields)

    db.flush()  # ensure profile.id is populated before linking skills

    seed_skills(db)
    # Sync candidate skills directly with the freshly extracted skills from the uploaded resume
    fresh_skills = sorted(list(set(extracted_skills)))
    _sync_candidate_skills(db, profile, fresh_skills)

    db.commit()
    db.refresh(profile)

    # Automatically extract candidate details and generate / update portfolio website
    try:
        from app.services.portfolio_service import build_portfolio_from_candidate_profile
        build_portfolio_from_candidate_profile(
            db=db,
            candidate=profile,
            file_bytes=file_bytes,
            filename=original_filename,
        )
    except Exception as e:
        logger.warning("Auto-generating portfolio after resume upload failed non-critically: %s", e)

    # Sync candidate resume vector to Qdrant vector database
    try:
        from app.services.qdrant_service import upsert_document, COLLECTION_RESUMES
        cand_text = f"Headline: {profile.headline or ''}\nSkills: {', '.join(fresh_skills)}\nSummary: {profile.summary or ''}\nExperience: {profile.work_experience or ''}\nResume: {raw_text}"
        upsert_document(
            collection_name=COLLECTION_RESUMES,
            doc_id=profile.id,
            text=cand_text,
            metadata={
                "candidate_id": str(profile.id),
                "user_id": str(profile.user_id),
                "headline": profile.headline,
                "current_role": profile.current_role,
                "experience_years": profile.experience_years,
                "skills": fresh_skills,
                "college_name": getattr(profile, "college_name", None),
                "target_role": getattr(profile, "target_role", None),
            },
        )
    except Exception as q_err:
        logger.debug("Qdrant candidate vector indexing non-critical notice: %s", q_err)

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

    # LinkedIn-Style Professional Profile Fields & College/Academic Credentials
    for field in [
        "full_name", "resume_email", "profile_photo", "headline", "current_role", "certifications",
        "portfolio_url", "linkedin_url", "github_url", "other_links",
        "college_name", "degree", "branch", "graduation_year", "cgpa",
        "twelfth_school", "twelfth_board", "twelfth_year", "twelfth_percentage",
        "tenth_school", "tenth_board", "tenth_year", "tenth_percentage",
    ]:
        if field in update_data and update_data[field] is not None:
            setattr(profile, field, update_data[field])

    new_cand_name = update_data.get("full_name") or update_data.get("name")
    if new_cand_name and isinstance(new_cand_name, str) and new_cand_name.strip():
        profile.full_name = new_cand_name.strip()
        from app.models.user import User
        user_obj = profile.user or db.get(User, profile.user_id)
        if user_obj:
            user_obj.name = new_cand_name.strip()
            db.add(user_obj)

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
