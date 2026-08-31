"""
ats_screener.py — Transparent ATS Candidate Screening & Match Engine.
Calculates a 100% weighted ATS score based on:
  1. Skills Match: 30%
  2. Experience Match: 20%
  3. Required Keywords Match: 15%
  4. Job Responsibilities Match: 15%
  5. Education Match: 10%
  6. Location Match: 5%
  7. Resume Readability / Structure: 5%
Total: 100%
"""
import re
import datetime
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

from app.ml.semantic_matcher import semantic_similarity
from app.ml.tfidf_matcher import tfidf_similarity
from app.nlp.skill_extractor import extract_skills
from app.models.candidate import CandidateProfile
from app.models.job import Job


@dataclass
class ATSResult:
    ats_score: float
    job_match_score: float
    skills_match_score: float
    experience_match_score: float
    education_match_score: float
    location_match_score: float
    keyword_match_score: float
    responsibility_match_score: float
    readability_score: float

    matched_skills: List[str] = field(default_factory=list)
    missing_skills: List[str] = field(default_factory=list)
    matched_preferred_skills: List[str] = field(default_factory=list)
    missing_preferred_skills: List[str] = field(default_factory=list)
    matched_keywords: List[str] = field(default_factory=list)
    missing_keywords: List[str] = field(default_factory=list)

    candidate_experience: Optional[float] = None
    required_experience: Optional[float] = None

    education_matched: bool = True
    location_matched: bool = True

    screening_status: str = "Review Required"
    recommendation: str = "Manual Review"
    is_eligible: bool = False
    explanation: str = ""
    version: str = "v1.0"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ats_score": self.ats_score,
            "job_match_score": self.job_match_score,
            "breakdown": {
                "skills_match": self.skills_match_score,
                "experience_match": self.experience_match_score,
                "keyword_match": self.keyword_match_score,
                "responsibility_match": self.responsibility_match_score,
                "education_match": self.education_match_score,
                "location_match": self.location_match_score,
                "readability": self.readability_score,
            },
            "matched_skills": self.matched_skills,
            "missing_skills": self.missing_skills,
            "matched_preferred_skills": self.matched_preferred_skills,
            "missing_preferred_skills": self.missing_preferred_skills,
            "matched_keywords": self.matched_keywords,
            "missing_keywords": self.missing_keywords,
            "candidate_experience": self.candidate_experience,
            "required_experience": self.required_experience,
            "education_matched": self.education_matched,
            "location_matched": self.location_matched,
            "screening_status": self.screening_status,
            "recommendation": self.recommendation,
            "is_eligible": self.is_eligible,
            "explanation": self.explanation,
            "version": self.version,
        }


def _extract_keywords(text: str, max_keywords: int = 15) -> List[str]:
    """Extract key technical and domain keywords from job description text."""
    if not text:
        return []
    # Stopwords list
    stopwords = {
        "and", "or", "the", "a", "an", "in", "on", "at", "for", "with", "about",
        "against", "between", "into", "through", "during", "before", "after",
        "above", "below", "to", "from", "up", "down", "out", "off", "over",
        "under", "again", "further", "then", "once", "here", "there", "when",
        "where", "why", "how", "all", "any", "both", "each", "few", "more",
        "most", "other", "some", "such", "no", "nor", "not", "only", "own",
        "same", "so", "than", "too", "very", "can", "will", "just", "should",
        "now", "we", "our", "you", "your", "are", "is", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "job", "role", "work",
        "candidate", "team", "company", "looking", "must", "required", "preferred"
    }
    words = re.findall(r'[A-Za-z0-9+#.#-]{2,}', text)
    cleaned = []
    seen = set()
    for w in words:
        wl = w.strip().lower()
        if len(wl) > 2 and wl not in stopwords and not wl.isdigit():
            if wl not in seen:
                seen.add(wl)
                cleaned.append(w.strip())
    return cleaned[:max_keywords]


def _evaluate_education(candidate_edu: Optional[str], job_desc: Optional[str]) -> tuple[float, bool]:
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

    req_level = 0
    for deg, lvl in degree_levels.items():
        if deg in job_text:
            req_level = max(req_level, lvl)

    if req_level == 0:
        return 100.0, True  # No explicit degree required

    cand_level = 0
    for deg, lvl in degree_levels.items():
        if deg in cand_text:
            cand_level = max(cand_level, lvl)

    if cand_level >= req_level:
        return 100.0, True
    elif cand_level == req_level - 1:
        return 75.0, False
    elif cand_level > 0:
        return 50.0, False
    return 30.0, False


def _evaluate_location(candidate_loc: Optional[str], job_loc: Optional[str], job_desc: Optional[str]) -> tuple[float, bool]:
    """Evaluates location match score (0-100)."""
    if not job_loc or "remote" in (job_loc or "").lower() or "remote" in (job_desc or "").lower():
        return 100.0, True
    if not candidate_loc:
        return 70.0, True

    c_loc = candidate_loc.strip().lower()
    j_loc = job_loc.strip().lower()

    if j_loc in c_loc or c_loc in j_loc:
        return 100.0, True

    # Check city/state token overlap
    j_tokens = set(re.findall(r'\w+', j_loc))
    c_tokens = set(re.findall(r'\w+', c_loc))
    if j_tokens.intersection(c_tokens):
        return 100.0, True

    return 50.0, False


def _evaluate_readability(resume_text: Optional[str]) -> float:
    """Evaluates ATS readability and document structure (0-100)."""
    if not resume_text or len(resume_text.strip()) < 50:
        return 20.0

    score = 50.0
    text_lower = resume_text.lower()

    # Section checks
    if any(k in text_lower for k in ["experience", "work history", "employment"]):
        score += 15.0
    if any(k in text_lower for k in ["education", "university", "college", "degree"]):
        score += 15.0
    if any(k in text_lower for k in ["skill", "technologies", "expertise"]):
        score += 10.0
    if "@" in resume_text or re.search(r'\d{10}', resume_text):
        score += 10.0

    return min(100.0, score)


def screen_candidate_ats(
    candidate: CandidateProfile,
    job: Job,
    min_ats_threshold: Optional[float] = None,
) -> ATSResult:
    """
    Screens candidate resume against job description and calculates 100% ATS score.
    """
    threshold = min_ats_threshold if min_ats_threshold is not None else (getattr(job, "min_ats_score", 60.0) or 60.0)

    # 1. Skill Extraction & Matching
    cand_skill_map = {
        cs.skill.skill_name.strip().lower(): cs.skill.skill_name.strip()
        for cs in candidate.candidate_skills
        if cs and cs.skill
    }

    required_skills = [js.skill.skill_name for js in job.job_skills if js.required]
    preferred_skills = [js.skill.skill_name for js in job.job_skills if not js.required]

    if not required_skills:
        extracted = extract_skills(job.description or "")
        if extracted:
            required_skills = extracted

    matched_required = []
    missing_required = []
    for s in required_skills:
        if s.strip().lower() in cand_skill_map:
            matched_required.append(s)
        else:
            missing_required.append(s)

    matched_preferred = []
    missing_preferred = []
    for s in preferred_skills:
        if s.strip().lower() in cand_skill_map:
            matched_preferred.append(s)
        else:
            missing_preferred.append(s)

    req_skill_score = (len(matched_required) / len(required_skills) * 100.0) if required_skills else 100.0
    pref_skill_score = (len(matched_preferred) / len(preferred_skills) * 100.0) if preferred_skills else 100.0

    skills_match_score = round(req_skill_score * 0.85 + pref_skill_score * 0.15, 2) if preferred_skills else round(req_skill_score, 2)

    # 2. Experience Matching
    cand_exp = candidate.experience_years or 0.0
    req_exp = getattr(job, "min_experience", None) or job.experience_required or 0.0

    if req_exp <= 0:
        experience_match_score = 100.0
    elif cand_exp >= req_exp:
        experience_match_score = 100.0
    else:
        experience_match_score = round((cand_exp / req_exp) * 100.0, 2)

    # 3. Keywords Matching
    job_keywords = _extract_keywords(f"{job.title} {job.description}", max_keywords=15)
    resume_text = candidate.resume_text or candidate.summary or ""
    resume_text_lower = resume_text.lower()

    matched_keywords = []
    missing_keywords = []
    for kw in job_keywords:
        if kw.lower() in resume_text_lower:
            matched_keywords.append(kw)
        else:
            missing_keywords.append(kw)

    keyword_match_score = round((len(matched_keywords) / len(job_keywords) * 100.0), 2) if job_keywords else 100.0

    # 4. Job Responsibilities & Semantic Similarity Match
    job_text = job.description or ""
    cand_history_text = f"{candidate.summary or ''} {candidate.work_experience or ''} {candidate.resume_text or ''}"
    tfidf_sim = tfidf_similarity(cand_history_text, job_text)
    semantic_sim = semantic_similarity(cand_history_text, job_text)
    responsibility_match_score = round((tfidf_sim * 0.4 + semantic_sim * 0.6), 2)

    # 5. Education Match
    education_match_score, edu_matched = _evaluate_education(candidate.education, job.description)

    # 6. Location Match
    location_match_score, loc_matched = _evaluate_location(candidate.location, job.location, job.description)

    # 7. Readability / ATS Formatting
    readability_score = _evaluate_readability(candidate.resume_text)

    # Calculate 100% Weighted ATS Score
    # Skills: 30%, Experience: 20%, Keywords: 15%, Responsibilities: 15%, Education: 10%, Location: 5%, Readability: 5%
    raw_ats_score = round(
        skills_match_score * 0.30
        + experience_match_score * 0.20
        + keyword_match_score * 0.15
        + responsibility_match_score * 0.15
        + education_match_score * 0.10
        + location_match_score * 0.05
        + readability_score * 0.05,
        2
    )

    # Missing critical required skills penalty
    ats_score = raw_ats_score
    if required_skills and len(matched_required) == 0:
        ats_score = round(raw_ats_score * 0.50, 2)
    elif required_skills and (len(matched_required) / len(required_skills)) < 0.5:
        ats_score = round(raw_ats_score * 0.75, 2)

    # Job Match Score (overall job relevance)
    job_match_score = round(
        responsibility_match_score * 0.40
        + keyword_match_score * 0.30
        + skills_match_score * 0.30,
        2
    )

    # Screening Status & Recommendation Logic per Specification
    if ats_score >= 80.0:
        screening_status = "Strong Match"
        recommendation = "Priority Candidate"
    elif ats_score >= 60.0:
        screening_status = "Eligible"
        recommendation = "Shortlist for Review"
    elif ats_score >= 40.0:
        screening_status = "Review Required"
        recommendation = "Manual Review"
    else:
        screening_status = "Low Match"
        recommendation = "Not Recommended"

    is_eligible = ats_score >= threshold

    # Generate Human-Explainable Match Summary
    explanation_parts = []
    explanation_parts.append(f"ATS Score: {ats_score}% ({screening_status}).")
    if required_skills:
        explanation_parts.append(f"Matched {len(matched_required)}/{len(required_skills)} required skills.")
    if missing_required:
        explanation_parts.append(f"Missing required skills: {', '.join(missing_required[:5])}.")
    if cand_exp < req_exp:
        explanation_parts.append(f"Experience ({cand_exp} yrs) is below required {req_exp} yrs.")
    else:
        explanation_parts.append(f"Experience ({cand_exp} yrs) meets or exceeds requirement ({req_exp} yrs).")

    explanation = " ".join(explanation_parts)

    return ATSResult(
        ats_score=ats_score,
        job_match_score=job_match_score,
        skills_match_score=skills_match_score,
        experience_match_score=experience_match_score,
        education_match_score=education_match_score,
        location_match_score=location_match_score,
        keyword_match_score=keyword_match_score,
        responsibility_match_score=responsibility_match_score,
        readability_score=readability_score,
        matched_skills=matched_required,
        missing_skills=missing_required,
        matched_preferred_skills=matched_preferred,
        missing_preferred_skills=missing_preferred,
        matched_keywords=matched_keywords,
        missing_keywords=missing_keywords,
        candidate_experience=cand_exp,
        required_experience=req_exp,
        education_matched=edu_matched,
        location_matched=loc_matched,
        screening_status=screening_status,
        recommendation=recommendation,
        is_eligible=is_eligible,
        explanation=explanation,
        version="v1.0"
    )
