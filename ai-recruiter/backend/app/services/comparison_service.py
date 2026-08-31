"""
comparison_service.py — Candidate side-by-side comparison & AI recommendation logic.
Queries candidates, ATS scores, skill matrices, interview performance, and calls LLM
for comprehensive candidate comparison & hiring recommendations.
"""
import json
import uuid
from typing import Any, Dict, List, Optional
from collections import defaultdict

from sqlalchemy.orm import Session, joinedload

from app.ai.llm_service import generate
from app.core.exceptions import NotFoundError, PermissionDeniedError, AppError
from app.models.application import Application
from app.models.candidate import CandidateProfile, CandidateSkill
from app.models.interview import Interview, InterviewEvaluation, InterviewStatus
from app.models.job import Job, JobSkill


def compare_candidates(db: Session, recruiter_id: uuid.UUID, job_id_str: str, candidate_ids_str: List[str]) -> Dict[str, Any]:
    # 1. Parse & Validate Job
    try:
        job_uuid = uuid.UUID(job_id_str)
    except ValueError:
        raise NotFoundError("Invalid Job ID")

    job = (
        db.query(Job)
        .options(joinedload(Job.job_skills).joinedload(JobSkill.skill))
        .filter(Job.id == job_uuid)
        .first()
    )
    if not job:
        raise NotFoundError("Job not found")

    if job.recruiter_id != recruiter_id:
        raise PermissionDeniedError("You can only compare candidates for your own job postings.")

    if not candidate_ids_str or len(candidate_ids_str) < 2 or len(candidate_ids_str) > 3:
        raise AppError("Comparison requires between 2 and 3 candidates.", "INVALID_COMPARISON_COUNT", 400)

    # 2. Parse candidate / application UUIDs
    parsed_ids = []
    for c_id in candidate_ids_str:
        try:
            parsed_ids.append(uuid.UUID(c_id.strip()))
        except ValueError:
            pass

    if not parsed_ids:
        raise NotFoundError("No valid candidate or application IDs provided.")

    # 3. Query Applications for this job
    applications = (
        db.query(Application)
        .options(
            joinedload(Application.candidate).joinedload(CandidateProfile.user),
            joinedload(Application.candidate).joinedload(CandidateProfile.candidate_skills).joinedload(CandidateSkill.skill),
        )
        .filter(
            Application.job_id == job.id,
            (Application.candidate_id.in_(parsed_ids) | Application.id.in_(parsed_ids))
        )
        .all()
    )

    if len(applications) < 2:
        raise NotFoundError("Found fewer than 2 matching applications for the selected candidates on this job.")

    # Query completed Interviews for these candidates on this job
    cand_ids = [a.candidate_id for a in applications]
    interviews = (
        db.query(Interview)
        .options(joinedload(Interview.evaluation))
        .filter(
            Interview.job_id == job.id,
            Interview.candidate_id.in_(cand_ids)
        )
        .all()
    )
    interviews_by_cand = {i.candidate_id: i for i in interviews}

    # Job required skills
    required_job_skills = sorted({js.skill.skill_name for js in job.job_skills if js.required and js.skill})
    all_job_skills = sorted({js.skill.skill_name for js in job.job_skills if js.skill})

    candidates_data = []
    candidate_strengths: Dict[str, List[str]] = {}
    candidate_weaknesses: Dict[str, List[str]] = {}
    missing_skills_map: Dict[str, List[str]] = {}

    for app in applications:
        cand = app.candidate
        user = cand.user if cand else None
        c_name = user.name if user else "Candidate"

        matched_skills = json.loads(app.matched_skills) if app.matched_skills else []
        missing_skills = json.loads(app.missing_skills) if app.missing_skills else []
        matched_keywords = json.loads(app.matched_keywords) if app.matched_keywords else []
        missing_keywords = json.loads(app.missing_keywords) if app.missing_keywords else []

        cand_skills = sorted({cs.skill.skill_name for cs in cand.candidate_skills if cs and cs.skill}) if cand else []

        # Interview scores if present
        interview_obj = interviews_by_cand.get(app.candidate_id)
        eval_obj = interview_obj.evaluation if interview_obj else None

        interview_data = None
        if interview_obj or eval_obj:
            interview_data = {
                "interview_id": str(interview_obj.id) if interview_obj else None,
                "status": interview_obj.status.value if (interview_obj and hasattr(interview_obj.status, "value")) else str(getattr(interview_obj, "status", "scheduled")),
                "overall_score": (eval_obj.overall_score if eval_obj else interview_obj.overall_score) if (eval_obj or interview_obj) else None,
                "technical_score": eval_obj.technical_score if eval_obj else None,
                "communication_score": eval_obj.communication_score if eval_obj else None,
                "problem_solving_score": eval_obj.problem_solving_score if eval_obj else None,
                "relevance_score": eval_obj.relevance_score if eval_obj else None,
                "recommendation": eval_obj.recommendation if eval_obj else None,
            }

        cand_entry = {
            "candidate_id": str(cand.id) if cand else str(app.candidate_id),
            "application_id": str(app.id),
            "name": c_name,
            "email": user.email if user else None,
            "headline": getattr(cand, "headline", None) or getattr(cand, "current_role", None) or "Candidate",
            "location": (cand.location if cand else None) or "Not specified",
            "experience_years": cand.experience_years if cand else 0.0,
            "education": cand.education if cand else "Not specified",
            "work_experience": cand.work_experience if cand else "Not specified",
            "summary": cand.summary or cand.ai_summary or "No summary provided",
            "certifications": getattr(cand, "certifications", None) or "None listed",

            # ATS Scores
            "ats_score": Math_round(app.ats_score or app.match_score or 0.0),
            "job_match_score": Math_round(app.job_match_score or app.match_score or 0.0),
            "skills_match_score": Math_round(app.skills_match_score or 0.0),
            "experience_match_score": Math_round(app.experience_match_score or 0.0),
            "keyword_match_score": Math_round(app.keyword_match_score or 0.0),
            "responsibility_match_score": Math_round(app.responsibility_match_score or 0.0),
            "education_match_score": Math_round(app.education_match_score or 100.0),
            "location_match_score": Math_round(app.location_match_score or 100.0),

            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "matched_keywords": matched_keywords,
            "missing_keywords": missing_keywords,
            "skills": cand_skills,
            "interview_performance": interview_data,
        }

        candidates_data.append(cand_entry)

        # Identify strengths & weaknesses
        strengths = []
        weaknesses = []

        if cand_entry["ats_score"] >= 80:
            strengths.append(f"High ATS match score ({cand_entry['ats_score']}%)")
        if cand_entry["experience_years"] >= job.experience_required:
            strengths.append(f"Meets required experience ({cand_entry['experience_years']} yrs vs {job.experience_required} yrs required)")
        else:
            weaknesses.append(f"Below required experience ({cand_entry['experience_years']} yrs vs {job.experience_required} yrs required)")

        if len(matched_skills) > 0:
            strengths.append(f"Matches {len(matched_skills)} key required skills")
        if len(missing_skills) > 0:
            weaknesses.append(f"Missing {len(missing_skills)} required skills ({', '.join(missing_skills[:3])})")

        if interview_data and interview_data.get("overall_score"):
            score = interview_data["overall_score"]
            if score >= 75:
                strengths.append(f"Strong interview performance ({score}/100)")
            elif score < 60:
                weaknesses.append(f"Below average interview score ({score}/100)")

        candidate_strengths[c_name] = strengths
        candidate_weaknesses[c_name] = weaknesses
        missing_skills_map[c_name] = missing_skills

    # 4. Construct Skill Matrix
    # Collect all unique skills among job requirements and candidates
    all_matrix_skills = set(required_job_skills)
    for c in candidates_data:
        all_matrix_skills.update(c["skills"])

    skill_matrix = []
    for sk in sorted(all_matrix_skills):
        is_req = sk in required_job_skills
        row = {
            "skill": sk,
            "is_required": is_req,
            "candidates": {}
        }
        for c in candidates_data:
            has_sk = sk in c["skills"] or sk in c["matched_skills"]
            row["candidates"][c["name"]] = "matching" if has_sk else ("missing" if is_req else "not_specified")

        skill_matrix.append(row)

    # 5. AI Candidate Recommendation Generation
    ai_recommendation = _generate_ai_recommendation(job, candidates_data)

    return {
        "job_id": str(job.id),
        "job_title": job.title,
        "candidates": candidates_data,
        "skill_matrix": skill_matrix,
        "recommended_candidate": ai_recommendation["recommended_candidate"],
        "recommendation_reason": ai_recommendation["recommendation_reason"],
        "candidate_strengths": candidate_strengths,
        "candidate_weaknesses": candidate_weaknesses,
        "missing_skills": missing_skills_map,
        "hiring_summary": ai_recommendation["hiring_summary"],
    }


def Math_round(val: Optional[float]) -> float:
    return round(val, 1) if val is not None else 0.0


def _generate_ai_recommendation(job: Job, candidates: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Uses llm_service to generate intelligent recommendation, falling back to deterministic scoring if unavailable."""
    # Build prompt context
    c_summaries = []
    for c in candidates:
        int_text = f", Interview Score: {c['interview_performance']['overall_score']}" if c.get("interview_performance") and c["interview_performance"].get("overall_score") else ""
        c_summaries.append(
            f"- Candidate Name: {c['name']}\n"
            f"  Experience: {c['experience_years']} years (Job requires: {job.experience_required} yrs)\n"
            f"  ATS Match Score: {c['ats_score']}%\n"
            f"  Matched Skills: {', '.join(c['matched_skills']) if c['matched_skills'] else 'None'}\n"
            f"  Missing Skills: {', '.join(c['missing_skills']) if c['missing_skills'] else 'None'}{int_text}\n"
            f"  Education: {c['education']}"
        )

    cand_text = "\n\n".join(c_summaries)

    system_prompt = (
        "You are an expert executive recruitment advisor. Compare the provided candidates for the job requisition "
        "and select the best suited candidate based on skills match, relevant experience, ATS score, and interview performance. "
        "Provide a concise, objective hiring recommendation."
    )

    user_prompt = (
        f"Job Title: {job.title}\n"
        f"Experience Required: {job.experience_required} years\n"
        f"Job Description: {job.description[:400]}...\n\n"
        f"Selected Candidates for Comparison:\n{cand_text}\n\n"
        f"Analyze these candidates and provide your recommendation in JSON format with keys:\n"
        f'- "recommended_candidate": "<Name of best candidate>"\n'
        f'- "recommendation_reason": "<Bullet points explaining why this candidate is top choice>"\n'
        f'- "hiring_summary": "<Brief summary comparison of all candidates>"'
    )

    raw_llm = generate(system_prompt, user_prompt, max_tokens=600)
    if raw_llm:
        try:
            # Strip markdown fence if present
            clean_llm = raw_llm.strip()
            if clean_llm.startswith("```"):
                clean_llm = clean_llm.split("```")[1]
                if clean_llm.startswith("json"):
                    clean_llm = clean_llm[4:]
            parsed = json.loads(clean_llm.strip())
            if isinstance(parsed, dict) and "recommended_candidate" in parsed:
                return {
                    "recommended_candidate": parsed.get("recommended_candidate", candidates[0]["name"]),
                    "recommendation_reason": parsed.get("recommendation_reason", "Strong overall qualification match."),
                    "hiring_summary": parsed.get("hiring_summary", "Comprehensive candidate comparison completed."),
                }
        except Exception:
            pass

    # Deterministic Rule-Based Fallback
    best_cand = max(
        candidates,
        key=lambda c: (
            c["ats_score"] * 0.4 +
            (c["interview_performance"]["overall_score"] if c.get("interview_performance") and c["interview_performance"].get("overall_score") else c["ats_score"]) * 0.3 +
            (100 if c["experience_years"] >= job.experience_required else 50) * 0.2 +
            (len(c["matched_skills"]) / (len(c["matched_skills"]) + len(c["missing_skills"]) or 1)) * 10
        )
    )

    other_cands = [c for c in candidates if c["name"] != best_cand["name"]]
    reason_bullets = [
        f"Highest overall qualification score and ATS match ({best_cand['ats_score']}%)",
        f"Meets experience requirement ({best_cand['experience_years']} yrs vs {job.experience_required} yrs required)",
        f"Matched {len(best_cand['matched_skills'])} key required skills"
    ]

    summary = f"{best_cand['name']} is the top recommendation for '{job.title}' based on technical skill alignment and experience requirements."

    return {
        "recommended_candidate": best_cand["name"],
        "recommendation_reason": "\n".join([f"• {b}" for b in reason_bullets]),
        "hiring_summary": summary,
    }
