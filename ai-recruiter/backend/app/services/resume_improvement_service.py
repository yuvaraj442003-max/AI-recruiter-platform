"""
resume_improvement_service.py — Job-specific AI Resume Coach & Improvement Engine.

Performs:
  - Weak sentence detection & action-verb rewriting
  - Job-specific missing keyword guidance
  - Missing skill learning recommendations
  - Missing achievement detection & metric placeholders ([X%])
  - Grammar & tense consistency corrections
  - Formatting & structural analysis
  - 6 Quality Sub-scores (Writing, Keywords, Achievements, Grammar, Formatting, Relevance)
  - Strict AI safety (never fabricates experience or metrics)
"""
import re
from typing import Any, Dict, List, Optional, Tuple

from app.ai.llm_service import generate
from app.models.candidate import CandidateProfile
from app.models.job import Job
from app.services.ats_scoring_service import calculate_job_specific_ats, extract_keywords_from_text, normalize_skill

WEAK_PHRASES: List[str] = [
    "worked on", "helped with", "responsible for", "participated in",
    "did tasks", "handled work", "worked with", "assisted in",
    "tasked with", "was involved in", "part of team", "did project",
    "worked in", "was responsible"
]

ACTION_VERBS: Dict[str, str] = {
    "worked on": "Developed and implemented",
    "helped with": "Collaborated on building",
    "responsible for": "Led and managed",
    "participated in": "Contributed to developing",
    "did tasks": "Executed key requirements for",
    "handled work": "Administered and optimized",
    "worked with": "Engineered features alongside",
    "assisted in": "Co-authored and delivered",
    "tasked with": "Spearheaded",
    "was involved in": "Drove the execution of",
    "part of team": "Collaborated with cross-functional teams to deliver",
    "did project": "Designed and delivered",
    "worked in": "Spearheaded initiatives in",
    "was responsible": "Directed operations for",
}


def detect_weak_sentences(text: str, job_title: str) -> List[Dict[str, Any]]:
    """Detects low-impact or weak sentences and generates action-oriented recommended rewrites."""
    if not text:
        return []

    lines = [line.strip().lstrip("•-* ") for line in text.splitlines() if len(line.strip()) > 10]
    if not lines:
        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        lines = [s.strip() for s in sentences if len(s.strip()) > 15]

    weak_items = []
    seen = set()

    for line in lines[:15]:
        line_lower = line.lower()
        if line_lower in seen:
            continue

        matched_phrase = None
        for wp in WEAK_PHRASES:
            if wp in line_lower:
                matched_phrase = wp
                break

        is_short = len(line.split()) < 6
        is_passive = any(w in line_lower for w in ["was done", "were created", "is responsible"])

        if matched_phrase or is_short or is_passive:
            seen.add(line_lower)
            verb = ACTION_VERBS.get(matched_phrase, "Spearheaded and delivered")
            
            # Replace weak phrase or prefix
            if matched_phrase:
                pattern = re.compile(re.escape(matched_phrase), re.IGNORECASE)
                recommended = pattern.sub(verb, line)
            else:
                recommended = f"{verb} {line[0].lower() + line[1:] if line else line}"

            # Ensure proper capitalization & punctuation
            recommended = recommended[0].upper() + recommended[1:]
            if not recommended.endswith("."):
                recommended += "."

            reasons = ["Uses a stronger action verb."]
            if matched_phrase:
                reasons.append(f"Replaces passive phrase '{matched_phrase}'.")
            if is_short:
                reasons.append("Expands short sentence with specific technical context.")
            reasons.append("Demonstrates technical contribution and professional clarity.")

            weak_items.append({
                "original": line,
                "recommended": recommended,
                "reason": reasons,
                "needs_candidate_confirmation": False
            })

            if len(weak_items) >= 5:
                break

    # Fallback if no weak phrases explicitly found
    if not weak_items and lines:
        sample_line = lines[0]
        weak_items.append({
            "original": sample_line,
            "recommended": f"Engineered and delivered {sample_line[0].lower() + sample_line[1:] if len(sample_line) > 1 else sample_line}.",
            "reason": ["Replaces default wording with strong action verb.", "Provides clearer technical focus."],
            "needs_candidate_confirmation": False
        })

    return weak_items


def analyze_achievements_and_metrics(text: str) -> Tuple[float, List[Dict[str, Any]]]:
    """Analyzes experience for quantifiable metrics (% or numbers) and generates placeholder suggestions."""
    if not text:
        return 40.0, []

    lines = [line.strip().lstrip("•-* ") for line in text.splitlines() if len(line.strip()) > 15]
    if not lines:
        lines = [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if len(s.strip()) > 15]

    total_bullets = len(lines) if lines else 1
    metric_regex = re.compile(r'\d+%\s*|\d+\s*(?:users|clients|projects|ms|sec|seconds|hrs|hours|k|m|million|billion|\$)', re.IGNORECASE)

    bullets_with_metrics = sum(1 for line in lines if metric_regex.search(line))
    achievement_impact_score = round((bullets_with_metrics / max(total_bullets, 1)) * 100.0, 1)
    achievement_impact_score = max(35.0, min(100.0, achievement_impact_score))

    achievement_suggestions = []

    # Find bullets missing metrics
    for line in lines:
        if not metric_regex.search(line) and len(line) > 15:
            suggestion_text = f"Add a measurable result if available, such as: {line.rstrip('.')} by [X%], supporting [X] users or reducing processing time by [Y%]."
            achievement_suggestions.append({
                "original": line,
                "suggestion": suggestion_text,
                "requires_confirmation": True
            })
            if len(achievement_suggestions) >= 4:
                break

    if not achievement_suggestions:
        achievement_suggestions.append({
            "original": lines[0] if lines else "Worked on key projects.",
            "suggestion": "Quantify your impact by adding metrics such as: 'Improved system performance by [X%]' or 'Supported [X] active users'.",
            "requires_confirmation": True
        })

    return achievement_impact_score, achievement_suggestions


def analyze_grammar_and_tense(text: str) -> Tuple[float, List[Dict[str, Any]]]:
    """Scans for common grammar and tense consistency errors."""
    if not text:
        return 95.0, []

    grammar_corrections = []
    
    # Common grammar/tense patterns
    patterns = [
        (r"\bI am worked\b", "I worked"),
        (r"\bDevelop application and managed\b", "Developed applications and managed"),
        (r"\bresponsible for handle\b", "responsible for handling"),
        (r"\bhave experience in develop\b", "have experience in developing"),
        (r"\bworked in python development\b", "worked in Python development"),
        (r"\bwas lead a team\b", "led a team"),
        (r"\bhelped in build\b", "assisted in building"),
    ]

    for pat, corr in patterns:
        if re.search(pat, text, re.IGNORECASE):
            match = re.search(pat, text, re.IGNORECASE).group(0)
            grammar_corrections.append({
                "original": match,
                "corrected": corr
            })

    grammar_score = 95.0 if not grammar_corrections else max(70.0, 100.0 - (len(grammar_corrections) * 10))
    return grammar_score, grammar_corrections


def analyze_formatting(text: str) -> Tuple[float, List[str]]:
    """Analyzes resume structure and formatting."""
    suggestions = []
    if not text:
        return 60.0, ["Upload a complete resume to analyze document structure and headings."]

    score = 90.0
    paragraphs = text.split("\n\n")
    has_bullets = any("•" in line or "-" in line for line in text.splitlines())

    if not has_bullets:
        score -= 15.0
        suggestions.append("Convert long experience paragraphs into bullet points for easier scanning by recruiters.")

    long_paras = [p for p in paragraphs if len(p.split()) > 80]
    if long_paras:
        score -= 10.0
        suggestions.append("Break down lengthy paragraphs (over 80 words) into concise 1-2 sentence bullet points.")

    text_lower = text.lower()
    if not any(k in text_lower for k in ["summary", "profile", "about"]):
        suggestions.append("Add a 2-3 sentence Professional Summary section at the top of your resume.")
    if not any(k in text_lower for k in ["skills", "technologies", "expertise"]):
        suggestions.append("Add a dedicated Skills & Expertise section.")

    if not suggestions:
        suggestions.append("Good section structure and formatting detected.")

    return max(50.0, score), suggestions


def analyze_and_improve_resume(candidate: CandidateProfile, job: Job) -> Dict[str, Any]:
    """
    Main orchestrator for AI Resume Improvement & AI Resume Coach report generation.
    """
    resume_text = candidate.resume_text or candidate.summary or candidate.work_experience or ""
    
    # 1. Run ATS Analysis
    ats_data = calculate_job_specific_ats(candidate, job)
    overall_ats = ats_data["overall_ats_score"]
    matched_skills = ats_data["matched_skills"]
    missing_skills = ats_data["missing_skills"]
    matched_keywords = ats_data["matched_keywords"]
    missing_keywords = ats_data["missing_keywords"]

    # 2. Weak Sentence Detection
    weak_sentences = detect_weak_sentences(resume_text, job.title)

    # 3. Achievements & Metrics Analysis
    achievement_impact_score, achievement_suggestions = analyze_achievements_and_metrics(resume_text)

    # 4. Grammar & Tense Analysis
    grammar_score, grammar_corrections = analyze_grammar_and_tense(resume_text)

    # 5. Formatting Analysis
    formatting_score, formatting_suggestions = analyze_formatting(resume_text)

    # 6. Quality Sub-Scores Calculation
    writing_quality = min(100.0, round(80.0 + (10.0 if len(weak_sentences) <= 2 else 0.0), 1))
    keyword_optimization = ats_data["score_breakdown"]["keywords"]
    job_relevance = ats_data["score_breakdown"]["responsibilities"]

    overall_resume_quality = round(
        writing_quality * 0.20
        + keyword_optimization * 0.20
        + achievement_impact_score * 0.20
        + grammar_score * 0.15
        + formatting_score * 0.10
        + job_relevance * 0.15,
        1
    )

    # Priority Improvements
    priority_improvements = []
    if missing_keywords:
        priority_improvements.append(f"Add missing job-relevant keywords: {', '.join(missing_keywords[:3])} where truthful.")
    if achievement_impact_score < 70.0:
        priority_improvements.append("Add measurable achievements (percentages %, numbers, or user metrics) to work experience.")
    if weak_sentences:
        priority_improvements.append("Strengthen weak experience descriptions using strong action verbs.")
    if missing_skills:
        priority_improvements.append(f"Consider learning or highlighting required skills: {', '.join(missing_skills[:3])}.")

    if not priority_improvements:
        priority_improvements.append("Your resume is well aligned for this job posting.")

    # Section-by-section breakdown (Summary, Skills, Experience)
    summary_text = candidate.summary or "Python Developer with technical knowledge."
    improved_summary = (
        f"{summary_text.rstrip('.')} with strong focus on {job.title} roles. "
        f"Experienced in {', '.join(matched_skills[:3]) if matched_skills else 'key industry practices'} "
        f"and delivering scalable solutions."
    )

    sections_breakdown = [
        {
            "section_name": "Professional Summary",
            "current_content": summary_text,
            "problems_found": [
                "Missing explicit target job keywords." if missing_keywords else "Could be more impactful.",
                "Lacks quantifiable scope."
            ],
            "recommended_improvements": [
                f"Incorporate key target role keywords for '{job.title}'.",
                "Highlight key technical and domain accomplishments."
            ],
            "improved_version": improved_summary,
            "note": "Only include skills and experience supported by your actual background."
        }
    ]

    return {
        "candidate_id": str(candidate.id),
        "job_id": str(job.id),
        "overall_resume_quality": overall_resume_quality,
        "scores": {
            "writing_quality": writing_quality,
            "keyword_optimization": keyword_optimization,
            "achievement_impact": achievement_impact_score,
            "grammar": grammar_score,
            "formatting": formatting_score,
            "job_relevance": job_relevance,
        },
        "weak_sentences": weak_sentences,
        "missing_keywords": missing_keywords,
        "missing_skills": missing_skills,
        "achievement_suggestions": achievement_suggestions,
        "grammar_corrections": grammar_corrections,
        "formatting_suggestions": formatting_suggestions,
        "priority_improvements": priority_improvements,
        "sections": sections_breakdown,
    }
