"""
interview_service.py — orchestrates the AI interview flow: creating an
interview for a candidate+job (validated against an existing
Application), generating and persisting questions, accepting answers
(auto-evaluating each one), and rolling everything up into a final
interview evaluation and report once all questions are answered.
"""
import json
from datetime import datetime, timezone

from sqlalchemy.orm import Session, joinedload

from app.ai.interview_evaluator import evaluate_answer, evaluate_interview
from app.ai.question_generator import generate_interview_questions
from app.core.exceptions import AppError, ConflictError, NotFoundError
from app.models.application import Application
from app.models.candidate import CandidateProfile
from app.models.interview import (
    Interview,
    InterviewAnswer,
    InterviewEvaluation,
    InterviewQuestion,
    InterviewStatus,
)
from app.models.job import Job, JobSkill


def load_interview(db: Session, interview_id) -> Interview | None:
    return (
        db.query(Interview)
        .options(
            joinedload(Interview.questions).joinedload(InterviewQuestion.answer),
            joinedload(Interview.evaluation),
            joinedload(Interview.candidate).joinedload(CandidateProfile.user),
            joinedload(Interview.job),
        )
        .filter(Interview.id == interview_id)
        .first()
    )


def create_interview(db: Session, recruiter_id, candidate_profile_id, job_id, interview_type, num_questions=6) -> Interview:
    job = db.query(Job).options(joinedload(Job.job_skills).joinedload(JobSkill.skill)).filter(Job.id == job_id).first()
    if not job:
        raise NotFoundError("Job not found")
    if job.recruiter_id != recruiter_id:
        raise AppError("You can only start interviews for your own job postings.", "PERMISSION_DENIED", 403)

    candidate = db.query(CandidateProfile).filter(CandidateProfile.id == candidate_profile_id).first()
    if not candidate:
        raise NotFoundError("Candidate profile not found")

    application = (
        db.query(Application)
        .filter(Application.candidate_id == candidate_profile_id, Application.job_id == job_id)
        .first()
    )
    if not application:
        raise AppError(
            "This candidate hasn't applied to this job — an application is required before starting an interview.",
            "NO_APPLICATION",
            400,
        )

    existing = (
        db.query(Interview)
        .filter(Interview.candidate_id == candidate_profile_id, Interview.job_id == job_id)
        .first()
    )
    if existing:
        raise ConflictError("An interview already exists for this candidate and job.")

    interview = Interview(
        candidate_id=candidate_profile_id,
        job_id=job_id,
        application_id=application.id,
        interview_type=interview_type,
        status=InterviewStatus.scheduled,
    )
    db.add(interview)
    db.flush()

    _generate_questions(db, interview, job, candidate, num_questions)

    interview.status = InterviewStatus.in_progress
    interview.started_at = datetime.now(timezone.utc)
    db.commit()

    return load_interview(db, interview.id)


def _generate_questions(db: Session, interview: Interview, job: Job, candidate: CandidateProfile, num_questions: int) -> None:
    db.query(InterviewQuestion).filter(InterviewQuestion.interview_id == interview.id).delete()

    required_skills = [js.skill.skill_name for js in job.job_skills if js.required]
    result = generate_interview_questions(
        job_title=job.title,
        required_skills=required_skills,
        experience_years=candidate.experience_years,
        num_questions=num_questions,
    )

    for order, q in enumerate(result["questions"], start=1):
        db.add(
            InterviewQuestion(
                interview_id=interview.id,
                question=q["question"],
                question_type=q["type"],
                difficulty=q["difficulty"],
                expected_topics=json.dumps(q.get("expected_topics", [])),
                order_number=order,
            )
        )
    db.flush()


def regenerate_questions(db: Session, interview: Interview, num_questions: int = 6) -> Interview:
    if interview.status == InterviewStatus.completed:
        raise AppError("Cannot regenerate questions for a completed interview.", "INTERVIEW_COMPLETED", 400)

    job = db.query(Job).options(joinedload(Job.job_skills).joinedload(JobSkill.skill)).filter(Job.id == interview.job_id).first()
    candidate = db.query(CandidateProfile).filter(CandidateProfile.id == interview.candidate_id).first()

    _generate_questions(db, interview, job, candidate, num_questions)
    db.commit()
    return load_interview(db, interview.id)


def submit_answer(db: Session, interview: Interview, question_id, answer_text: str, answer_source: str = "text") -> InterviewAnswer:
    if interview.status == InterviewStatus.completed:
        raise AppError("This interview has already been completed.", "INTERVIEW_COMPLETED", 400)

    question = (
        db.query(InterviewQuestion)
        .filter(InterviewQuestion.id == question_id, InterviewQuestion.interview_id == interview.id)
        .first()
    )
    if not question:
        raise NotFoundError("Question not found on this interview")

    existing = db.query(InterviewAnswer).filter(InterviewAnswer.question_id == question_id).first()
    if existing:
        raise ConflictError("This question has already been answered.")

    job = db.query(Job).filter(Job.id == interview.job_id).first()
    expected_topics = json.loads(question.expected_topics) if question.expected_topics else []

    evaluation = evaluate_answer(
        question=question.question,
        expected_topics=expected_topics,
        answer_text=answer_text,
        job_context=job.description if job else "",
    )

    answer = InterviewAnswer(
        question_id=question.id,
        candidate_id=interview.candidate_id,
        answer_text=answer_text,
        answer_source=answer_source,
        answer_score=evaluation["overall_score"],
        feedback=json.dumps({"strengths": evaluation.get("strengths", []), "improvements": evaluation.get("improvements", [])}),
    )
    db.add(answer)
    db.flush()

    _maybe_complete_interview(db, interview)

    db.commit()
    db.refresh(answer)
    return answer


def _maybe_complete_interview(db: Session, interview: Interview) -> None:
    total_questions = db.query(InterviewQuestion).filter(InterviewQuestion.interview_id == interview.id).count()
    answered = (
        db.query(InterviewAnswer)
        .join(InterviewQuestion, InterviewAnswer.question_id == InterviewQuestion.id)
        .filter(InterviewQuestion.interview_id == interview.id)
        .count()
    )

    if total_questions > 0 and answered >= total_questions:
        interview.status = InterviewStatus.completed
        interview.completed_at = datetime.now(timezone.utc)
        _run_final_evaluation(db, interview)


def _run_final_evaluation(db: Session, interview: Interview) -> InterviewEvaluation:
    job = db.query(Job).filter(Job.id == interview.job_id).first()

    answers = (
        db.query(InterviewAnswer)
        .join(InterviewQuestion, InterviewAnswer.question_id == InterviewQuestion.id)
        .filter(InterviewQuestion.interview_id == interview.id)
        .all()
    )

    answer_evaluations = []
    for answer in answers:
        feedback = json.loads(answer.feedback) if answer.feedback else {}
        answer_evaluations.append(
            {
                "overall_score": answer.answer_score or 0,
                "technical_score": answer.answer_score or 0,
                "relevance_score": answer.answer_score or 0,
                "problem_solving_score": answer.answer_score or 0,
                "communication_score": answer.answer_score or 0,
                "strengths": feedback.get("strengths", []),
                "improvements": feedback.get("improvements", []),
            }
        )

    summary = evaluate_interview(job.title if job else "this role", answer_evaluations)

    existing_eval = db.query(InterviewEvaluation).filter(InterviewEvaluation.interview_id == interview.id).first()
    if existing_eval:
        db.delete(existing_eval)
        db.flush()

    evaluation = InterviewEvaluation(
        interview_id=interview.id,
        technical_score=summary["technical_score"],
        communication_score=summary["communication_score"],
        relevance_score=summary["relevance_score"],
        problem_solving_score=summary["problem_solving_score"],
        overall_score=summary["overall_score"],
        strengths=json.dumps(summary["strengths"]),
        weaknesses=json.dumps(summary["weaknesses"]),
        recommendation=summary["recommendation"],
        source=summary["source"],
    )
    db.add(evaluation)
    interview.overall_score = summary["overall_score"]
    db.flush()
    return evaluation


def force_evaluate(db: Session, interview: Interview) -> Interview:
    """Recruiter-triggered explicit (re-)evaluation, e.g. after answers were updated."""
    _run_final_evaluation(db, interview)
    db.commit()
    return load_interview(db, interview.id)


def build_report(interview: Interview) -> dict:
    questions_with_answers = []
    for q in interview.questions:
        answer = q.answer
        feedback = json.loads(answer.feedback) if answer and answer.feedback else {}
        questions_with_answers.append(
            {
                "question": q.question,
                "type": q.question_type,
                "difficulty": q.difficulty,
                "expected_topics": json.loads(q.expected_topics) if q.expected_topics else [],
                "answer_text": answer.answer_text if answer else None,
                "answer_score": answer.answer_score if answer else None,
                "strengths": feedback.get("strengths", []),
                "improvements": feedback.get("improvements", []),
            }
        )

    evaluation = interview.evaluation
    return {
        "interview_id": interview.id,
        "candidate_name": interview.candidate.user.name if interview.candidate and interview.candidate.user else None,
        "job_title": interview.job.title if interview.job else None,
        "status": interview.status,
        "started_at": interview.started_at,
        "completed_at": interview.completed_at,
        "questions": questions_with_answers,
        "evaluation": {
            "technical_score": evaluation.technical_score if evaluation else None,
            "communication_score": evaluation.communication_score if evaluation else None,
            "relevance_score": evaluation.relevance_score if evaluation else None,
            "problem_solving_score": evaluation.problem_solving_score if evaluation else None,
            "overall_score": evaluation.overall_score if evaluation else None,
            "strengths": json.loads(evaluation.strengths) if evaluation and evaluation.strengths else [],
            "weaknesses": json.loads(evaluation.weaknesses) if evaluation and evaluation.weaknesses else [],
            "recommendation": evaluation.recommendation if evaluation else None,
            "source": evaluation.source if evaluation else None,
        }
        if evaluation
        else None,
        "human_review_required": True,
    }
