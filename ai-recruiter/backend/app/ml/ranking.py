"""
ranking.py — combines skill match, experience match, TF-IDF similarity,
semantic similarity, and preferred-skill match into one explainable
final score, per the weighting the spec lays out:

    Skill Match           40%
    Experience Match      20%
    TF-IDF Similarity     15%
    Semantic Similarity   20%
    Preferred Skills       5%

The score is always returned with an explanation (which required
skills matched/were missing, the experience gap, etc.) — never as a
bare number — so a recruiter can see *why*, and so the score reads as
decision support rather than an objective verdict. No protected or
biometric/emotional attributes are used anywhere in this module.
"""
from dataclasses import dataclass, field

from app.ml.semantic_matcher import semantic_similarity
from app.ml.tfidf_matcher import tfidf_similarity
from app.models.candidate import CandidateProfile
from app.models.job import Job

WEIGHTS = {
    "skill_match": 0.40,
    "experience_match": 0.20,
    "tfidf_match": 0.15,
    "semantic_match": 0.20,
    "preferred_skill_match": 0.05,
}


@dataclass
class MatchResult:
    final_score: float
    skill_match: float
    experience_match: float
    tfidf_match: float
    semantic_match: float
    preferred_skill_match: float
    matched_required_skills: list[str] = field(default_factory=list)
    missing_required_skills: list[str] = field(default_factory=list)
    matched_preferred_skills: list[str] = field(default_factory=list)
    missing_preferred_skills: list[str] = field(default_factory=list)
    candidate_experience_years: float | None = None
    required_experience_years: float | None = None

    def to_dict(self) -> dict:
        return {
            "final_score": self.final_score,
            "breakdown": {
                "skill_match": self.skill_match,
                "experience_match": self.experience_match,
                "tfidf_match": self.tfidf_match,
                "semantic_match": self.semantic_match,
                "preferred_skill_match": self.preferred_skill_match,
            },
            "explanation": {
                "matched_required_skills": self.matched_required_skills,
                "missing_required_skills": self.missing_required_skills,
                "matched_preferred_skills": self.matched_preferred_skills,
                "missing_preferred_skills": self.missing_preferred_skills,
                "candidate_experience_years": self.candidate_experience_years,
                "required_experience_years": self.required_experience_years,
            },
        }


def _experience_match_score(
    candidate_years: float | None,
    required_years: float | None,
    skill_match: float = 100.0,
    has_required_skills: bool = False,
) -> float:
    """Calculates experience match score (0-100).
    If the job has required skills and candidate matched NONE of them (0% skill match),
    relevant tech stack experience is 0.0%."""
    if has_required_skills and skill_match == 0.0:
        return 0.0

    if not required_years or required_years <= 0:
        if candidate_years and candidate_years > 0:
            return round(min(skill_match, 100.0), 2) if has_required_skills else 100.0
        return 0.0

    if not candidate_years or candidate_years <= 0:
        return 0.0

    ratio = candidate_years / required_years
    score = round(min(ratio, 1.0) * 100, 2)
    if has_required_skills and skill_match < 100.0:
        factor = (skill_match / 100.0) ** 0.5
        score = round(score * factor, 2)
    return score


from app.nlp.skill_extractor import extract_skills


def compute_match(candidate: CandidateProfile, job: Job, include_semantic: bool = False) -> MatchResult:
    candidate_skill_names = {cs.skill.skill_name for cs in candidate.candidate_skills}

    required_skills = {js.skill.skill_name for js in job.job_skills if js.required}
    preferred_skills = {js.skill.skill_name for js in job.job_skills if not js.required}

    # If job has no explicit required skills attached, extract technical skills dynamically from job description
    effective_required_skills = required_skills
    if not effective_required_skills:
        dynamic_job_skills = set(extract_skills(job.description or ""))
        if dynamic_job_skills:
            effective_required_skills = dynamic_job_skills

    cand_skill_map = {cs.skill.skill_name.strip().lower(): cs.skill.skill_name.strip() for cs in candidate.candidate_skills if cs and cs.skill}

    matched_required_set = set()
    missing_required_set = set()
    for skill in effective_required_skills:
        if skill.strip().lower() in cand_skill_map:
            matched_required_set.add(skill)
        else:
            missing_required_set.add(skill)

    matched_required = sorted(list(matched_required_set))
    missing_required = sorted(list(missing_required_set))

    matched_preferred_set = set()
    missing_preferred_set = set()
    for skill in preferred_skills:
        if skill.strip().lower() in cand_skill_map:
            matched_preferred_set.add(skill)
        else:
            missing_preferred_set.add(skill)

    matched_preferred = sorted(list(matched_preferred_set))
    missing_preferred = sorted(list(missing_preferred_set))

    skill_match = round(len(matched_required) / len(effective_required_skills) * 100, 2) if effective_required_skills else 100.0
    preferred_skill_match = (
        round(len(matched_preferred) / len(preferred_skills) * 100, 2) if preferred_skills else 100.0
    )

    experience_match = _experience_match_score(
        candidate.experience_years,
        job.experience_required,
        skill_match=skill_match,
        has_required_skills=bool(effective_required_skills),
    )

    resume_text = candidate.resume_text or candidate.summary or ""
    job_text = job.description or ""
    tfidf_match = tfidf_similarity(resume_text, job_text)
    if include_semantic:
        try:
            semantic_match = semantic_similarity(resume_text, job_text)
        except Exception:
            semantic_match = tfidf_match
    else:
        semantic_match = tfidf_match

    raw_final_score = round(
        skill_match * WEIGHTS["skill_match"]
        + experience_match * WEIGHTS["experience_match"]
        + tfidf_match * WEIGHTS["tfidf_match"]
        + semantic_match * WEIGHTS["semantic_match"]
        + preferred_skill_match * WEIGHTS["preferred_skill_match"],
        2,
    )

    # Apply strict skill gap penalty: if required technical skills are missing, scale down final score realistically
    final_score = raw_final_score
    if effective_required_skills and skill_match < 60.0:
        penalty_factor = 0.40 + (skill_match / 60.0) * 0.60
        final_score = round(raw_final_score * penalty_factor, 2)

    return MatchResult(
        final_score=final_score,
        skill_match=skill_match,
        experience_match=experience_match,
        tfidf_match=tfidf_match,
        semantic_match=semantic_match,
        preferred_skill_match=preferred_skill_match,
        matched_required_skills=matched_required,
        missing_required_skills=missing_required,
        matched_preferred_skills=matched_preferred,
        missing_preferred_skills=missing_preferred,
        candidate_experience_years=candidate.experience_years,
        required_experience_years=job.experience_required,
    )
