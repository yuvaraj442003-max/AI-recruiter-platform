"""
resume_verification_service.py — strict comparison between Candidate Create Form inputs
and extracted Resume fields before allowing registration.
"""
import re
from typing import Tuple, List, Dict, Any
from app.nlp.skills_data import get_all_skill_variants


def clean_digits(phone_str: str | None) -> str:
    if not phone_str:
        return ""
    return re.sub(r"\D", "", phone_str)


def verify_resume_against_form(fields: Dict[str, Any], form_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Compares candidate form entries against extracted resume fields.

    Returns:
        (is_valid: bool, mismatch_reasons: list[str])
    """
    mismatches: List[str] = []

    # 1. Phone Number Verification
    form_phone = form_data.get("phone")
    resume_phone = fields.get("phone")
    if form_phone and resume_phone:
        form_digits = clean_digits(form_phone)
        resume_digits = clean_digits(resume_phone)
        if len(form_digits) >= 7 and len(resume_digits) >= 7:
            # Check last 7 digits matching or overlap
            if form_digits[-7:] != resume_digits[-7:] and form_digits not in resume_digits and resume_digits not in form_digits:
                mismatches.append(f"Phone Number Mismatch: Form phone ('{form_phone}') does not match phone found in uploaded resume ('{resume_phone}').")

    # 2. Experience Years Verification
    form_exp = form_data.get("experience_years")
    resume_exp = fields.get("experience_years")
    if form_exp is not None and resume_exp is not None:
        try:
            f_exp = float(form_exp)
            r_exp = float(resume_exp)
            if abs(f_exp - r_exp) > 2.5 and f_exp > r_exp + 2.0:
                mismatches.append(f"Experience Years Mismatch: Form experience ({f_exp} yrs) contradicts work history extracted from resume ({r_exp} yrs).")
        except (ValueError, TypeError):
            pass

    # 3. Technical Skills Verification
    form_skills = form_data.get("skills") or []
    if isinstance(form_skills, str):
        form_skills = [s.strip() for s in form_skills.split(",") if s.strip()]

    resume_skills = fields.get("skills") or []
    resume_text = (fields.get("resume_text") or "").lower()

    if form_skills and (resume_skills or resume_text):
        matched_count = 0
        for sk in form_skills:
            sk_clean = sk.strip().lower()
            if not sk_clean:
                continue
            variants = get_all_skill_variants(sk_clean)
            if any(r_sk.lower() in variants for r_sk in resume_skills):
                matched_count += 1
            elif any(v in resume_text for v in variants if len(v) >= 2):
                matched_count += 1

        if matched_count == 0:
            skills_str = ", ".join(form_skills[:5])
            resume_skills_str = ", ".join(resume_skills[:5]) if resume_skills else "None"
            mismatches.append(f"Key Skills Mismatch: None of the entered form skills ('{skills_str}') were found in your uploaded resume (Resume skills: '{resume_skills_str}').")

    # 4. Candidate Name Verification
    form_name = form_data.get("name")
    resume_name = fields.get("name")
    if form_name and resume_name:
        f_words = {w.lower() for w in form_name.split() if len(w) >= 2}
        r_words = {w.lower() for w in resume_name.split() if len(w) >= 2}
        if f_words and r_words and not f_words.intersection(r_words):
            mismatches.append(f"Candidate Name Mismatch: Entered name ('{form_name}') contradicts name extracted from resume header ('{resume_name}').")

    is_valid = len(mismatches) == 0
    return is_valid, mismatches
