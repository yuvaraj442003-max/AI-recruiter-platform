"""
screening_worker.py — Async Screening Orchestrator & Task Handler.
Processes question generation, message dispatch, natural language response parsing,
state transitions, and final result calculation asynchronously.
"""
import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional

from sqlalchemy.orm import Session

from app.models.application import Application, ApplicationStatus
from app.models.candidate import CandidateProfile
from app.models.job import Job
from app.models.screening import (
    CandidateConsent,
    CommunicationLog,
    ScreeningAnswer,
    ScreeningChannel,
    ScreeningQuestion,
    ScreeningResult,
    ScreeningSession,
    ScreeningStatus,
)
from app.services.communication_provider import get_communication_provider
from app.services.screening_ai_service import extract_answer_structured, generate_job_questions
from app.services.screening_scoring_service import calculate_session_scores

logger = logging.getLogger("ai_recruiter.screening_worker")


def start_screening_session_task(db: Session, application_id: str) -> Optional[ScreeningSession]:
    """
    Initializes and triggers an automated AI screening session for an application.
    """
    try:
        app = db.query(Application).filter(Application.id == application_id).first()
        if not app:
            logger.error(f"Application {application_id} not found for screening initialization.")
            return None

        candidate = db.query(CandidateProfile).filter(CandidateProfile.id == app.candidate_id).first()
        job = db.query(Job).filter(Job.id == app.job_id).first()
        if not candidate or not job:
            logger.error(f"Candidate or Job missing for application {application_id}.")
            return None

        # Check candidate consent
        consent = db.query(CandidateConsent).filter(CandidateConsent.candidate_id == candidate.id).first()
        if consent and consent.opted_out_all:
            logger.info(f"Candidate {candidate.id} has opted out of automated messaging.")
            return None

        # Retrieve or create existing screening session
        session = db.query(ScreeningSession).filter(ScreeningSession.application_id == app.id).first()
        if not session:
            session = ScreeningSession(
                application_id=app.id,
                candidate_id=candidate.id,
                job_id=job.id,
                recruiter_id=job.recruiter_id,
                status=ScreeningStatus.pending,
                channel=ScreeningChannel.whatsapp,
            )
            db.add(session)
            db.commit()
            db.refresh(session)

        if session.status == ScreeningStatus.completed:
            logger.info(f"Screening session {session.id} is already completed.")
            return session

        # Prepare job details for question generator
        job_skills = [js.skill.skill_name for js in job.job_skills if js.skill] if job.job_skills else []
        job_dict = {
            "title": job.title,
            "description": job.description,
            "experience_required": job.experience_required,
            "location": job.location,
            "salary_range": job.salary_range,
            "skills": job_skills,
        }

        # Generate questions if not already present
        if not session.questions:
            raw_questions = generate_job_questions(job_dict)
            for idx, q_data in enumerate(raw_questions):
                q_obj = ScreeningQuestion(
                    screening_session_id=session.id,
                    question=q_data["question"],
                    question_type=q_data["question_type"],
                    expected_answer=q_data.get("expected_answer", ""),
                    weight=q_data.get("weight", 1.0),
                    sequence=idx + 1,
                )
                db.add(q_obj)
            session.total_questions = len(raw_questions)
            session.current_question_index = 0
            db.commit()
            db.refresh(session)

        # Destination candidate phone number
        candidate_phone = candidate.phone or (candidate.user.email if candidate.user else "")
        if not candidate_phone:
            candidate_phone = "+15550199283"  # Fallback for dev mode

        # Build welcome & Question 1 message
        q1 = session.questions[0] if session.questions else None
        if not q1:
            logger.error("No questions generated for screening session.")
            return session

        candidate_name = candidate.user.full_name if (candidate.user and candidate.user.full_name) else "Candidate"
        welcome_text = (
            f"Hi {candidate_name}! Thank you for applying for the {job.title} role.\n\n"
            f"I'm AI Recruiter Assistant. I have {len(session.questions)} quick screening questions to help process your application.\n\n"
            f"(Reply 'STOP' at any time to opt out).\n\n"
            f"Q1: {q1.question}"
        )

        # Dispatch message via communication provider
        try:
            provider = get_communication_provider()
            res = provider.send_message(candidate_phone, welcome_text, channel=session.channel.value)

            # Log communication
            comm_log = CommunicationLog(
                screening_session_id=session.id,
                candidate_id=candidate.id,
                channel=session.channel.value,
                direction="outbound",
                message=welcome_text,
                provider_message_id=res.get("provider_message_id") if isinstance(res, dict) else None,
                delivery_status=res.get("status", "sent") if isinstance(res, dict) else "sent",
            )
            db.add(comm_log)
        except Exception as msg_err:
            logger.warning(f"Failed to send welcome message: {msg_err}")

        session.status = ScreeningStatus.waiting_for_answer
        session.started_at = datetime.utcnow()
        app.screening_status = "in_progress"
        db.commit()

        return session
    except Exception as err:
        logger.exception(f"Error in start_screening_session_task: {err}")
        db.rollback()
        return None


def process_candidate_response_task(db: Session, session_id: str, candidate_answer: str) -> Dict[str, Any]:
    """
    Processes an incoming candidate response, extracts data, advances state, or completes session.
    """
    session = db.query(ScreeningSession).filter(ScreeningSession.id == session_id).first()
    if not session:
        return {"error": f"Screening session {session_id} not found."}

    candidate = db.query(CandidateProfile).filter(CandidateProfile.id == session.candidate_id).first()
    job = db.query(Job).filter(Job.id == session.job_id).first()
    candidate_phone = candidate.phone if candidate else "+15550199283"
    provider = get_communication_provider()

    # Log inbound message
    inbound_log = CommunicationLog(
        screening_session_id=session.id,
        candidate_id=session.candidate_id,
        channel=session.channel.value,
        direction="inbound",
        message=candidate_answer,
        delivery_status="received",
    )
    db.add(inbound_log)

    # 1. Check for Opt-Out intent
    extracted_res = extract_answer_structured(
        question_text="",
        question_type="",
        expected_criteria="",
        candidate_answer=candidate_answer,
    )

    if extracted_res.get("is_opt_out"):
        session.status = ScreeningStatus.opted_out
        # Record opt-out consent
        consent = db.query(CandidateConsent).filter(CandidateConsent.candidate_id == session.candidate_id).first()
        if not consent:
            consent = CandidateConsent(candidate_id=session.candidate_id)
            db.add(consent)
        consent.opted_out_all = True
        consent.opt_out_reason = candidate_answer
        db.commit()

        goodbye_msg = "You have successfully opted out of automated AI screening messages. Thank you!"
        provider.send_message(candidate_phone, goodbye_msg, channel=session.channel.value)
        return {"status": "opted_out", "message": "Candidate opted out."}

    # 2. Match answer to current question
    current_idx = session.current_question_index
    questions = session.questions
    if current_idx >= len(questions):
        return {"status": "already_completed"}

    current_q = questions[current_idx]

    # Evaluate answer using AI extraction
    job_skills = [js.skill.skill_name for js in job.job_skills if js.skill] if job and job.job_skills else []
    eval_res = extract_answer_structured(
        question_text=current_q.question,
        question_type=current_q.question_type,
        expected_criteria=current_q.expected_answer or "",
        candidate_answer=candidate_answer,
        job_data={"experience_required": job.experience_required if job else 0.0, "skills": job_skills},
    )

    # Save ScreeningAnswer row
    answer_obj = db.query(ScreeningAnswer).filter(ScreeningAnswer.screening_question_id == current_q.id).first()
    if not answer_obj:
        answer_obj = ScreeningAnswer(
            screening_question_id=current_q.id,
            screening_session_id=session.id,
            candidate_answer=candidate_answer,
            extracted_value=json.dumps(eval_res.get("extracted_value", {})),
            ai_score=eval_res.get("ai_score", 75.0),
            ai_reason=eval_res.get("ai_reason", ""),
        )
        db.add(answer_obj)
    else:
        answer_obj.candidate_answer = candidate_answer
        answer_obj.extracted_value = json.dumps(eval_res.get("extracted_value", {}))
        answer_obj.ai_score = eval_res.get("ai_score", 75.0)
        answer_obj.ai_reason = eval_res.get("ai_reason", "")

    db.commit()

    # 3. Advance question index
    next_idx = current_idx + 1
    session.current_question_index = next_idx

    if next_idx < len(questions):
        # Send next question
        next_q = questions[next_idx]
        next_msg = f"Q{next_idx + 1}: {next_q.question}"
        provider.send_message(candidate_phone, next_msg, channel=session.channel.value)

        outbound_log = CommunicationLog(
            screening_session_id=session.id,
            candidate_id=session.candidate_id,
            channel=session.channel.value,
            direction="outbound",
            message=next_msg,
            delivery_status="sent",
        )
        db.add(outbound_log)
        session.status = ScreeningStatus.waiting_for_answer
        db.commit()

        return {"status": "in_progress", "next_question_index": next_idx}
    else:
        # All questions answered — Calculate final score and complete session
        scores = calculate_session_scores(session)

        result_obj = db.query(ScreeningResult).filter(ScreeningResult.screening_session_id == session.id).first()
        if not result_obj:
            result_obj = ScreeningResult(
                screening_session_id=session.id,
                technical_score=scores["technical_score"],
                experience_score=scores["experience_score"],
                location_score=scores["location_score"],
                salary_score=scores["salary_score"],
                availability_score=scores["availability_score"],
                communication_score=scores["communication_score"],
                overall_score=scores["overall_score"],
                recommendation=scores["recommendation"],
                ai_summary=scores["ai_summary"],
            )
            db.add(result_obj)

        session.status = ScreeningStatus.completed
        session.screening_score = scores["overall_score"]
        session.recommendation = scores["recommendation"]
        session.completed_at = datetime.utcnow()

        # Update parent Application
        app = db.query(Application).filter(Application.id == session.application_id).first()
        if app:
            app.screening_status = "completed"
            app.overall_score = scores["overall_score"]
            app.recommendation = scores["recommendation"]

        db.commit()

        # Send completion message to candidate
        completion_msg = (
            f"Thank you! Your pre-screening interview for the {job.title if job else 'position'} is now complete.\n"
            f"Our recruiting team will review your responses shortly."
        )
        provider.send_message(candidate_phone, completion_msg, channel=session.channel.value)

        return {
            "status": "completed",
            "overall_score": scores["overall_score"],
            "recommendation": scores["recommendation"],
        }
