"""
candidate_feedback_service.py — Core Engine for Automated Candidate Feedback.
Handles evidence collection, AI prompt construction, Pydantic LLM output validation,
deterministic template fallback generation, recruiter approval workflows, and audit logging.
"""
import json
import logging
import re
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from sqlalchemy.orm import Session

from app.ai import llm_service
from app.models.application import Application, ApplicationStatus
from app.models.audit_log import AuditLog
from app.models.candidate import CandidateProfile
from app.models.candidate_feedback import CandidateFeedback, CandidateFeedbackReason, FeedbackStatus, FeedbackType
from app.models.job import Job
from app.models.notification import Notification
from app.schemas.feedback import FeedbackAIResponse
from app.services import email_service

logger = logging.getLogger("ai_recruiter.candidate_feedback")


def _safe_json_loads(data: Optional[str]) -> List[str]:
    if not data:
        return []
    try:
        val = json.loads(data)
        if isinstance(val, list):
            return [str(v).strip() for v in val if v]
        return []
    except Exception:
        # Fallback comma-split
        return [s.strip() for s in data.split(",") if s.strip()]


def collect_feedback_evidence(db: Session, app: Application) -> Dict[str, Any]:
    """
    Collects structured objective evidence from candidate profile, job requirements,
    ATS evaluation, pre-screening, assessment, and interview data.
    """
    cand = db.query(CandidateProfile).filter(CandidateProfile.id == app.candidate_id).first()
    job = db.query(Job).filter(Job.id == app.job_id).first()

    cand_name = cand.full_name if cand else "Candidate"
    job_title = job.title if job else "Position"
    company_name = job.company_name if (job and job.company_name) else "our hiring team"

    cand_skills = []
    if cand and cand.candidate_skills:
        cand_skills = [cs.skill.skill_name for cs in cand.candidate_skills if cs.skill]
    cand_exp = float(cand.experience_years) if (cand and cand.experience_years is not None) else 0.0

    job_skills = []
    if job and job.job_skills:
        job_skills = [js.skill.skill_name for js in job.job_skills if js.skill]

    job_min_exp = float(job.min_experience or job.experience_required or 0.0) if job else 0.0

    # ATS Matched & Missing Skills
    ats_matched = _safe_json_loads(app.matched_skills)
    ats_missing = _safe_json_loads(app.missing_skills)

    # Candidate strengths: Only skills present in candidate profile/ATS matched
    strengths = list(dict.fromkeys(ats_matched + [s for s in cand_skills if s in job_skills]))
    if not strengths and cand_skills:
        strengths = cand_skills[:3]

    # Top missing requirements: Top 2-5 mandatory missing skills/gaps
    missing_requirements = list(dict.fromkeys(ats_missing + [s for s in job_skills if s not in cand_skills]))
    if not missing_requirements and job_skills:
        missing_requirements = [s for s in job_skills if s not in strengths]
    missing_requirements = missing_requirements[:4]

    # Experience gap check
    exp_gap = None
    if cand_exp < job_min_exp:
        exp_gap = f"{job_min_exp}+ years of experience required (candidate has {cand_exp} years)"

    return {
        "candidate_name": cand_name,
        "job_title": job_title,
        "company_name": company_name,
        "candidate_skills": cand_skills,
        "candidate_experience_years": cand_exp,
        "job_skills": job_skills,
        "job_min_experience": job_min_exp,
        "strengths": strengths,
        "missing_requirements": missing_requirements,
        "experience_gap": exp_gap,
        "ats_score": app.ats_score or app.match_score or 0.0,
        "coding_score": app.coding_score,
        "interview_score": app.interview_score,
    }


def generate_deterministic_feedback(evidence: Dict[str, Any], level: str = "personalized") -> Dict[str, Any]:
    """
    Deterministic template fallback generator used when LLM is unavailable or fails validation.
    Generates polite, respectful, evidence-grounded non-selection feedback without hallucinations.
    """
    job_title = evidence.get("job_title", "Position")
    strengths = evidence.get("strengths", [])
    gaps = evidence.get("missing_requirements", [])
    exp_gap = evidence.get("experience_gap")

    str_text = ", ".join(strengths[:3]) if strengths else "software engineering fundamentals"
    gap_bullets = "\n".join([f"• {g}" for g in gaps[:3]]) if gaps else "• Specific technical domain experience"

    if level == "basic":
        summary = f"Thank you for applying for the {job_title} role."
        reason = f"While your background is valuable, this position was a closer match for candidates with specific role requirements."
        recommendation = "We encourage you to apply for future positions that better match your experience."
        content = (
            f"Thank you for applying for the {job_title} position.\n\n"
            f"Although your background is strong, your experience did not closely match all requirements of this specific position.\n\n"
            f"We appreciate your interest in our team and encourage you to explore future opportunities with us."
        )
    elif level == "detailed":
        summary = f"Your profile demonstrated solid experience in {str_text}."
        reason = f"The primary areas where your profile differed from role requirements were:\n{gap_bullets}"
        if exp_gap:
            reason += f"\n• {exp_gap}"
        recommendation = f"Your background in {str_text} is a great foundation. We encourage you to apply for future roles aligned with your technical strengths."
        content = (
            f"Thank you for applying for the {job_title} role.\n\n"
            f"What matched your profile well:\n" + "\n".join([f"✓ {s}" for s in strengths[:4]]) + "\n\n"
            f"Areas that were less aligned for this position:\n" + gap_bullets + "\n\n"
            f"While this role was a closer fit for other candidates, your experience is valuable. "
            f"We encourage you to apply for future opportunities that align closely with your background."
        )
    else:  # personalized (default)
        summary = f"Your profile demonstrated strong experience in {str_text}."
        reason = f"For this position, we were looking for stronger experience in: {', '.join(gaps[:3]) if gaps else 'specific cloud and domain tools'}."
        recommendation = f"We encourage you to apply for future backend/technical opportunities that align closely with your experience."
        content = (
            f"Thank you for applying for the {job_title} position.\n\n"
            f"Your profile demonstrated strong experience in {str_text}.\n\n"
            f"For this particular position, we were looking for stronger experience in:\n\n"
            f"{gap_bullets}\n\n"
            f"While your background is valuable, this role was a closer match for candidates with these specific requirements.\n\n"
            f"We encourage you to apply for future positions that better match your experience."
        )

    return {
        "summary": summary,
        "strengths": strengths[:4],
        "areas_for_improvement": gaps[:4],
        "reason": reason,
        "encouragement": recommendation,
        "tone": "respectful",
        "confidence": 1.0,
        "content": content,
    }


def generate_feedback_for_application(
    db: Session,
    application_id: uuid.UUID,
    custom_direction: Optional[str] = None,
    feedback_level: str = "personalized",
) -> CandidateFeedback:
    """
    Generates personalized, respectful candidate feedback for a non-selected application.
    Leverages LLM with Pydantic output validation and falls back gracefully to deterministic templates.
    """
    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise ValueError(f"Application {application_id} not found.")

    evidence = collect_feedback_evidence(db, app)
    job_title = evidence["job_title"]
    strengths = evidence["strengths"]
    missing_gaps = evidence["missing_requirements"]

    # Check or create CandidateFeedback DB record
    feedback = db.query(CandidateFeedback).filter(CandidateFeedback.application_id == application_id).first()
    if not feedback:
        feedback = CandidateFeedback(
            application_id=application_id,
            candidate_id=app.candidate_id,
            job_id=app.job_id,
            feedback_type=FeedbackType(feedback_level) if feedback_level in FeedbackType.__members__ else FeedbackType.personalized,
            feedback_status=FeedbackStatus.PENDING_REVIEW,
            ai_generated=True,
            recruiter_approved=False,
        )
        db.add(feedback)
        db.commit()
        db.refresh(feedback)

    # Attempt AI Generation
    system_prompt = (
        "You are an expert, compassionate AI Recruiting Coordinator. Generate respectful, non-judgmental, "
        "personalized candidate rejection feedback. Return ONLY valid JSON with keys:\n"
        "- 'summary': concise overview statement thanking candidate and acknowledging key strength\n"
        "- 'strengths': array of verified candidate strengths from input\n"
        "- 'areas_for_improvement': array of top 2 to 4 missing job requirements\n"
        "- 'reason': clear job-relevant reason for non-selection\n"
        "- 'encouragement': encouraging advice for future roles\n"
        "- 'tone': 'respectful'\n"
        "- 'confidence': float between 0.8 and 1.0\n"
        "STRICT CONSTRAINTS:\n"
        "1. Never mention protected characteristics (gender, race, age, religion, location, college).\n"
        "2. Never disclose internal ATS match scores (e.g. 72%), candidate ranks, or recruiter private notes.\n"
        "3. Never invent candidate skills or experience not present in the input.\n"
        "4. Keep tone professional, respectful, and constructive."
    )

    user_prompt = (
        f"Job Title: {job_title}\n"
        f"Verified Candidate Strengths: {', '.join(strengths) if strengths else 'Software engineering skills'}\n"
        f"Missing Job Requirements: {', '.join(missing_gaps) if missing_gaps else 'Domain specific tools'}\n"
        f"Experience Gap: {evidence.get('experience_gap') or 'None'}\n"
        f"Feedback Level: {feedback_level}\n"
        f"{f'Custom Recruiter Direction: {custom_direction}' if custom_direction else ''}"
    )

    llm_output = llm_service.generate(system_prompt, user_prompt, max_tokens=700)
    ai_result = None

    if llm_output:
        try:
            clean_json = re.sub(r"^```json\s*", "", llm_output, flags=re.MULTILINE)
            clean_json = re.sub(r"```$", "", clean_json, flags=re.MULTILINE).strip()
            parsed = json.loads(clean_json)
            validated = FeedbackAIResponse(**parsed)
            ai_result = validated.model_dump()
            ai_result["content"] = (
                f"Thank you for applying for the {job_title} position.\n\n"
                f"{validated.summary}\n\n"
                f"For this position, we were looking for stronger experience in:\n"
                + "\n".join([f"• {a}" for a in validated.areas_for_improvement]) + "\n\n"
                f"While your background is valuable, this role was a closer match for candidates with these requirements.\n\n"
                f"{validated.encouragement}"
            )
        except Exception as e:
            logger.warning(f"LLM feedback validation failed ({e}); falling back to deterministic template.")

    if not ai_result:
        ai_result = generate_deterministic_feedback(evidence, level=feedback_level)

    # Populate DB record
    feedback.summary = ai_result.get("summary")
    feedback.strengths = json.dumps(ai_result.get("strengths", []))
    feedback.areas_for_improvement = json.dumps(ai_result.get("areas_for_improvement", []))
    feedback.reason = ai_result.get("reason")
    feedback.recommendation = ai_result.get("encouragement")
    feedback.draft_content = ai_result.get("content")
    feedback.final_content = ai_result.get("content")
    feedback.feedback_status = FeedbackStatus.PENDING_REVIEW

    # Clear existing reasons and recreate structured evidence links
    db.query(CandidateFeedbackReason).filter(CandidateFeedbackReason.feedback_id == feedback.id).delete()
    for gap in ai_result.get("areas_for_improvement", []):
        r_item = CandidateFeedbackReason(
            feedback_id=feedback.id,
            reason_code="MISSING_REQUIRED_SKILL",
            reason_text=f"{gap} was a key requirement for this position.",
            evidence_type="JOB_REQUIREMENT",
            evidence_reference=gap,
        )
        db.add(r_item)

    db.commit()
    db.refresh(feedback)

    # Audit log entry
    audit = AuditLog(
        user_id=None,
        action="FEEDBACK_GENERATED",
        details=f"Generated candidate feedback for application {application_id} ({job_title})",
        meta_data={"application_id": str(application_id), "job_id": str(app.job_id)},
    )
    db.add(audit)
    db.commit()

    return feedback


def approve_and_send_feedback(
    db: Session,
    feedback_id: uuid.UUID,
    recruiter_user_id: uuid.UUID,
    final_content_override: Optional[str] = None,
) -> CandidateFeedback:
    """
    Approves candidate feedback draft, marks it SENT, delivers email & in-app notifications,
    and records mandatory audit log entries.
    """
    feedback = db.query(CandidateFeedback).filter(CandidateFeedback.id == feedback_id).first()
    if not feedback:
        raise ValueError(f"Feedback record {feedback_id} not found.")

    if final_content_override and final_content_override.strip():
        feedback.final_content = final_content_override.strip()
        # Audit record for editing
        edit_audit = AuditLog(
            user_id=recruiter_user_id,
            action="FEEDBACK_EDITED",
            details=f"Recruiter edited feedback draft for application {feedback.application_id}",
            meta_data={"feedback_id": str(feedback_id), "application_id": str(feedback.application_id)},
        )
        db.add(edit_audit)

    feedback.recruiter_approved = True
    feedback.feedback_status = FeedbackStatus.SENT
    feedback.approved_at = datetime.utcnow()
    feedback.sent_at = datetime.utcnow()

    db.commit()
    db.refresh(feedback)

    # In-App Notification
    app = db.query(Application).filter(Application.id == feedback.application_id).first()
    job = db.query(Job).filter(Job.id == feedback.job_id).first()
    job_title = job.title if job else "your job application"

    notif = Notification(
        user_id=app.candidate.user_id if (app and app.candidate) else None,
        title="Application Status Update & Feedback",
        message=f"Your application for {job_title} has been reviewed. Personalized feedback is now available.",
        link=f"candidate-dashboard.html?application_id={feedback.application_id}",
    )
    db.add(notif)

    # Email notification (if user email exists)
    try:
        if app and app.candidate and app.candidate.user and app.candidate.user.email:
            email_service.send_email(
                db=db,
                to_email=app.candidate.user.email,
                subject=f"Update on your application for {job_title}",
                body=f"Hello {app.candidate.full_name},\n\n{feedback.final_content}\n\nBest regards,\nAI Recruiter Platform",
            )
    except Exception as e:
        logger.error(f"Failed to send feedback email: {e}")

    # Audit Log
    approve_audit = AuditLog(
        user_id=recruiter_user_id,
        action="FEEDBACK_APPROVED",
        details=f"Recruiter approved candidate feedback for application {feedback.application_id}",
        meta_data={"feedback_id": str(feedback_id), "application_id": str(feedback.application_id)},
    )
    sent_audit = AuditLog(
        user_id=recruiter_user_id,
        action="FEEDBACK_SENT",
        details=f"Delivered candidate feedback notification for application {feedback.application_id}",
        meta_data={"feedback_id": str(feedback_id), "application_id": str(feedback.application_id)},
    )
    db.add_all([approve_audit, sent_audit])
    db.commit()

    return feedback
