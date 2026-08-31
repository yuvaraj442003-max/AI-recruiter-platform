"""
ats_scoring_service.py — Dynamic job-specific ATS score calculator & suggestion generator.

Calculates weighted 6-dimension ATS score:
  - Skills Match:           30%
  - Experience Match:       20%
  - Keywords Match:         15%
  - Responsibilities Match: 15%
  - Education Match:        10%
  - Location Match:         10%

Supports skill normalization, aliases, IT & non-IT jobs, missing/matched skill & keyword detection,
and generates job-specific AI resume improvement suggestions.
"""
import re
from typing import Any, Dict, List, Optional, Set, Tuple

from app.nlp.skills_data import ALIAS_INDEX, SKILLS_KB, get_all_skill_variants
from app.nlp.text_processor import clean_text
from app.ml.semantic_matcher import semantic_similarity
from app.ml.tfidf_matcher import tfidf_similarity
from app.models.candidate import CandidateProfile
from app.models.job import Job, JobSkill

# Configurable Scoring Weights (Must equal 1.0)
ATS_WEIGHTS: Dict[str, float] = {
    "skills": 0.30,
    "experience": 0.20,
    "keywords": 0.15,
    "responsibilities": 0.15,
    "education": 0.10,
    "location": 0.10,
}


# Stopwords for keyword extraction
STOPWORDS: Set[str] = {
    "a", "an", "the", "and", "or", "but", "if", "because", "as", "until", "while",
    "of", "at", "by", "for", "with", "about", "against", "between", "into", "through",
    "during", "before", "after", "above", "below", "to", "from", "up", "upon", "down",
    "in", "out", "on", "off", "over", "under", "again", "further", "then", "once",
    "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
    "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only",
    "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just",
    "don", "should", "now", "we", "our", "you", "your", "are", "is", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "job", "role", "work",
    "candidate", "team", "company", "looking", "must", "required", "preferred",
    "experience", "ability", "skills", "knowledge", "years", "year", "working",
    "description", "responsibilities", "requirements"
}


def normalize_skill(skill_name: str) -> str:
    """Normalizes skill using ALIAS_INDEX or case/whitespace clean-up."""
    if not skill_name:
        return ""
    cleaned = skill_name.strip()
    key = cleaned.lower()
    if key in ALIAS_INDEX:
        return ALIAS_INDEX[key]
    return cleaned


def extract_keywords_from_text(text: str, max_keywords: int = 20) -> List[str]:
    """Extracts non-stopword domain and technical keywords from job description."""
    if not text:
        return []
    words = re.findall(r"[A-Za-z0-9+#.#-]{2,}", text)
    cleaned = []
    seen = set()
    for w in words:
        wl = w.strip().lower()
        if len(wl) > 2 and wl not in STOPWORDS and not wl.isdigit():
            normalized = ALIAS_INDEX.get(wl, w.strip())
            if normalized.lower() not in seen:
                seen.add(normalized.lower())
                cleaned.append(normalized)
    return cleaned[:max_keywords]


def evaluate_education(candidate_edu: Optional[str], job_desc: Optional[str]) -> Tuple[float, bool]:
    """Evaluates education match score (0-100) and match flag."""
    if not job_desc or not candidate_edu:
        return 100.0, True

    job_text = job_desc.lower()
    cand_text = candidate_edu.lower()

    degree_levels = {
        "phd": 5, "doctorate": 5,
        "master": 4, "m.s": 4, "ms": 4, "m.tech": 4, "m.e": 4, "mba": 4,
        "bachelor": 3, "b.s": 3, "bs": 3, "b.tech": 3, "b.e": 3, "b.a": 3, "degree": 3,
        "associate": 2, "diploma": 2,
        "high school": 1
    }

    req_level = max([lvl for deg, lvl in degree_levels.items() if deg in job_text], default=0)
    if req_level == 0:
        return 100.0, True

    cand_level = max([lvl for deg, lvl in degree_levels.items() if deg in cand_text], default=0)
    if cand_level >= req_level:
        return 100.0, True
    elif cand_level == req_level - 1:
        return 75.0, False
    elif cand_level > 0:
        return 50.0, False
    return 40.0, False


def evaluate_location(candidate_loc: Optional[str], job_loc: Optional[str], job_desc: Optional[str]) -> Tuple[float, bool]:
    """Evaluates location match score (0-100) and match flag."""
    if not job_loc or "remote" in (job_loc or "").lower() or "remote" in (job_desc or "").lower():
        return 100.0, True
    if not candidate_loc:
        return 70.0, True

    c_loc = candidate_loc.strip().lower()
    j_loc = job_loc.strip().lower()

    if j_loc in c_loc or c_loc in j_loc:
        return 100.0, True

    j_tokens = set(re.findall(r"\w+", j_loc))
    c_tokens = set(re.findall(r"\w+", c_loc))
    if j_tokens.intersection(c_tokens):
        return 100.0, True

    return 50.0, False


def generate_ai_suggestions(
    job_title: str,
    missing_skills: List[str],
    missing_keywords: List[str],
    candidate_exp: float,
    required_exp: float,
    job_description: Optional[str] = None
) -> List[str]:
    """Generates role-specific AI resume improvement suggestions."""
    suggestions = []

    # Missing Skills Suggestions
    if missing_skills:
        top_missing = missing_skills[:3]
        for sk in top_missing:
            suggestions.append(f"Add hands-on project or experience with {sk} if applicable.")

    # Missing Keywords Suggestions
    if missing_keywords:
        top_kw = missing_keywords[:3]
        suggestions.append(f"Include relevant keywords like {', '.join(top_kw)} in your summary or work experience.")

    # Experience Suggestion
    if candidate_exp < required_exp:
        suggestions.append(f"Highlight relevant project depth and leadership to compensate for the experience gap ({candidate_exp} yrs vs {required_exp} yrs required).")

    # Domain / Job Title specific suggestions
    title_lower = (job_title or "").lower()
    desc_lower = (job_description or "").lower()

    if any(k in title_lower or k in desc_lower for k in ["data", "analyst", "analytics"]):
        if not any("sql" in sk.lower() for sk in missing_skills):
            suggestions.append("Add measurable data analytics achievements (e.g. optimized query latency by 40%, built automated dashboards).")
    elif any(k in title_lower or k in desc_lower for k in ["hr", "recruiter", "talent", "people"]):
        suggestions.append("Highlight key HR metrics such as time-to-hire reduction, employee retention rates, or ATS workflow optimization.")
    elif any(k in title_lower or k in desc_lower for k in ["sales", "account", "business development"]):
        suggestions.append("Quantify sales achievements with revenue impact, deal sizes, or quota attainment percentages.")
    elif any(k in title_lower or k in desc_lower for k in ["finance", "accountant", "audit"]):
        suggestions.append("Emphasize financial accuracy, compliance achievements, or experience with ERP/accounting tools.")
    else:
        suggestions.append("Include measurable metrics and key accomplishments for your past roles.")

    return suggestions[:5]


def calculate_job_specific_ats(candidate: CandidateProfile, job: Job) -> Dict[str, Any]:
    """
    Calculates detailed job-specific ATS scores and returns structured breakdown.
    Extracts and normalizes skills from candidate resume text and job requirements.
    """
    from app.nlp.skill_extractor import extract_skills

    # 1. Candidate Skills Normalization & Set Building
    cand_raw_skills = [
        cs.skill.skill_name for cs in (candidate.candidate_skills or []) if cs and cs.skill
    ]
    # Scan resume text, summary, work experience, and raw skills for additional skills
    resume_full_text = f"{candidate.resume_text or ''} {candidate.summary or ''} {candidate.work_experience or ''} {getattr(candidate, 'skills_raw', '') or ''}"

    extracted_cand_skills = extract_skills(resume_full_text) if resume_full_text.strip() else []

    all_cand_skills = set(cand_raw_skills).union(set(extracted_cand_skills))
    cand_skill_variants: set[str] = set()
    for s in all_cand_skills:
        cand_skill_variants.update(get_all_skill_variants(s))

    # Also build a lower-case raw text search string for multi-word or boundary skill matching
    resume_lower_search = f" {resume_full_text.lower()} "

    # 2. Job Required Skills Set Building
    required_job_skills = [
        normalize_skill(js.skill.skill_name)
        for js in (job.job_skills or []) if js.required and js.skill
    ]
    preferred_job_skills = [
        normalize_skill(js.skill.skill_name)
        for js in (job.job_skills or []) if not js.required and js.skill
    ]

    # Extract skills from job description & requirements text
    job_full_text = f"{job.title or ''} {getattr(job, 'requirements', '') or ''} {job.description or ''}"
    extracted_job_skills = extract_skills(job_full_text) if job_full_text.strip() else []

    for s in extracted_job_skills:
        norm_s = normalize_skill(s)
        if norm_s and norm_s.lower() not in [r.lower() for r in required_job_skills] and norm_s.lower() not in [p.lower() for p in preferred_job_skills]:
            required_job_skills.append(norm_s)

    # 3. Match Skills against Candidate Resume & Profile
    matched_skills = []
    missing_skills = []

    for r_skill in required_job_skills:
        r_norm = normalize_skill(r_skill)
        req_variants = get_all_skill_variants(r_skill).union(get_all_skill_variants(r_norm))

        is_matched = False
        # Check if candidate skill set contains any alias or variant of the required skill
        if req_variants.intersection(cand_skill_variants):
            is_matched = True
        else:
            # Check raw resume text for any variant
            for v in req_variants:
                if (
                    f" {v} " in resume_lower_search
                    or f" {v}," in resume_lower_search
                    or f" {v}." in resume_lower_search
                    or f"({v})" in resume_lower_search
                    or f"/{v}" in resume_lower_search
                    or f"{v}/" in resume_lower_search
                ):
                    is_matched = True
                    break

        if is_matched:
            if r_norm not in matched_skills:
                matched_skills.append(r_norm)
        else:
            if r_norm not in missing_skills:
                missing_skills.append(r_norm)

    for p_skill in preferred_job_skills:
        p_norm = normalize_skill(p_skill)
        pref_variants = get_all_skill_variants(p_skill).union(get_all_skill_variants(p_norm))
        is_p_matched = bool(pref_variants.intersection(cand_skill_variants))
        if not is_p_matched:
            for v in pref_variants:
                if f" {v} " in resume_lower_search or f" {v}," in resume_lower_search or f" {v}." in resume_lower_search:
                    is_p_matched = True
                    break
        if is_p_matched and p_norm not in matched_skills:
            matched_skills.append(p_norm)

    if required_job_skills:
        skills_match_score = round((len(matched_skills) / len(required_job_skills)) * 100.0, 1)
        skills_match_score = min(100.0, skills_match_score)
    else:
        skills_match_score = 100.0


    # 2. Experience Match
    cand_exp = candidate.experience_years or 0.0
    req_exp = getattr(job, "min_experience", None) or job.experience_required or 0.0

    if req_exp <= 0:
        experience_match_score = 100.0
    elif cand_exp >= req_exp:
        experience_match_score = 100.0
    else:
        experience_match_score = round((cand_exp / req_exp) * 100.0, 1)

    # 3. Keywords Match
    job_keywords = extract_keywords_from_text(f"{job.title} {job.description}", max_keywords=15)
    resume_text = candidate.resume_text or candidate.summary or candidate.work_experience or ""
    resume_lower = resume_text.lower()

    matched_keywords = []
    missing_keywords = []
    for kw in job_keywords:
        kw_variants = get_all_skill_variants(kw)
        if kw.lower() in resume_lower or bool(kw_variants.intersection(cand_skill_variants)):
            matched_keywords.append(kw)
        else:
            missing_keywords.append(kw)


    keyword_match_score = round((len(matched_keywords) / len(job_keywords) * 100.0), 1) if job_keywords else 100.0

    # 4. Responsibilities Match
    cand_history_text = f"{candidate.summary or ''} {candidate.work_experience or ''} {candidate.resume_text or ''}"
    job_text = job.description or ""
    tfidf_sim = tfidf_similarity(cand_history_text, job_text)
    semantic_sim = semantic_similarity(cand_history_text, job_text)
    responsibility_match_score = round((tfidf_sim * 0.4 + semantic_sim * 0.6), 1)

    # 5. Education Match
    education_match_score, edu_matched = evaluate_education(candidate.education, job.description)

    # 6. Location Match
    location_match_score, loc_matched = evaluate_location(candidate.location, job.location, job.description)

    # Weighted Overall ATS Score
    overall_ats_score = round(
        skills_match_score * ATS_WEIGHTS["skills"]
        + experience_match_score * ATS_WEIGHTS["experience"]
        + keyword_match_score * ATS_WEIGHTS["keywords"]
        + responsibility_match_score * ATS_WEIGHTS["responsibilities"]
        + education_match_score * ATS_WEIGHTS["education"]
        + location_match_score * ATS_WEIGHTS["location"],
        1
    )

    # Suggestions
    suggestions = generate_ai_suggestions(
        job_title=job.title,
        missing_skills=missing_skills,
        missing_keywords=missing_keywords,
        candidate_exp=cand_exp,
        required_exp=req_exp,
        job_description=job.description
    )

    return {
        "candidate_id": str(candidate.id),
        "job_id": str(job.id),
        "overall_ats_score": overall_ats_score,
        "score_breakdown": {
            "skills": skills_match_score,
            "experience": experience_match_score,
            "keywords": keyword_match_score,
            "responsibilities": responsibility_match_score,
            "education": education_match_score,
            "location": location_match_score,
        },
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "suggestions": suggestions,
        "candidate_experience": cand_exp,
        "required_experience": req_exp,
        "education_matched": edu_matched,
        "location_matched": loc_matched,
    }
