"""
Interview endpoints: recruiter starts an interview (auto-generates
questions), candidate views/answers questions, and either side views
the final report once complete.
"""
import json
import uuid

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_role
from app.core.exceptions import NotFoundError, PermissionDeniedError
from app.models.candidate import CandidateProfile
from app.models.interview import Interview, InterviewStatus
from app.models.job import Job
from app.models.user import User, UserRole
from app.schemas.common import APIResponse
from app.schemas.interview import (
    AnswerResponse,
    AnswerSubmit,
    InterviewCreate,
    InterviewQuestionOut,
    InterviewReport,
    InterviewResponse,
)
from app.services.interview_service import (
    build_report,
    create_interview,
    force_evaluate,
    regenerate_questions,
    submit_answer,
)
from app.services import interview_service

router = APIRouter(prefix="/interviews", tags=["Interviews"])


def _is_owning_recruiter(interview: Interview, user: User) -> bool:
    return user.role == UserRole.recruiter and interview.job and interview.job.recruiter_id == user.id


def _is_owning_candidate(interview: Interview, user: User) -> bool:
    return (
        user.role == UserRole.candidate
        and interview.candidate
        and interview.candidate.user_id == user.id
    )


def _to_response(interview: Interview, include_answers: bool) -> InterviewResponse:
    questions = []
    for q in interview.questions:
        topics = json.loads(q.expected_topics) if q.expected_topics else []
        questions.append(
            InterviewQuestionOut(
                id=q.id,
                question=q.question,
                question_type=q.question_type,
                difficulty=q.difficulty,
                expected_topics=topics,
                order_number=q.order_number,
                answered=q.answer is not None,
                answer_text=q.answer.answer_text if include_answers and q.answer else None,
                answer_score=q.answer.answer_score if include_answers and q.answer else None,
            )
        )

    return InterviewResponse(
        id=interview.id,
        candidate_id=interview.candidate_id,
        job_id=interview.job_id,
        candidate_name=interview.candidate.user.name if interview.candidate and interview.candidate.user else None,
        job_title=interview.job.title if interview.job else None,
        interview_type=interview.interview_type,
        status=interview.status,
        overall_score=interview.overall_score,
        started_at=interview.started_at,
        completed_at=interview.completed_at,
        questions=questions,
    )


@router.post("", response_model=APIResponse[InterviewResponse], status_code=201)
def start_interview(
    payload: InterviewCreate,
    current_user: User = Depends(require_role(UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    interview = create_interview(
        db,
        recruiter_id=current_user.id,
        candidate_profile_id=payload.candidate_id,
        job_id=payload.job_id,
        interview_type=payload.interview_type,
        num_questions=payload.num_questions,
    )
    from datetime import datetime
    try:
        from app.services.email_service import send_interview_invitation_email
        from app.core.config import settings

        cand_user = interview.candidate.user if (interview.candidate and interview.candidate.user) else None
        if cand_user and cand_user.email:
            comp_name = (
                interview.job.company.name if (interview.job and getattr(interview.job, "company", None))
                else f"{current_user.name}'s Company"
            )
            job_title = interview.job.title if interview.job else "Position"
            link = f"{settings.FRONTEND_URL.rstrip('/')}/interview.html?id={interview.id}"
            sched_date = datetime.now().strftime("%B %d, %Y")
            sched_time = "Flexible / Instant Online Session"

            send_interview_invitation_email(
                to_email=cand_user.email,
                candidate_name=cand_user.name,
                company_name=comp_name,
                job_title=job_title,
                interview_date=sched_date,
                interview_time=sched_time,
                location_or_link=link,
                instructions="Log in to your candidate portal and complete the online AI technical & behavioral interview session.",
                db=db,
            )
    except Exception as err:
        print(f"Warning: Failed to dispatch interview invitation email: {err}")

    return APIResponse(
        success=True, message="Interview started and questions generated", data=_to_response(interview, include_answers=True)
    )


@router.get("/{interview_id}", response_model=APIResponse[InterviewResponse])
def get_interview(
    interview_id: str,
    current_user: User = Depends(require_role(UserRole.candidate, UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    try:
        parsed_id = uuid.UUID(interview_id)
    except ValueError:
        raise NotFoundError("Interview not found")

    interview = interview_service.load_interview(db, parsed_id)
    if not interview:
        raise NotFoundError("Interview not found")

    is_recruiter = _is_owning_recruiter(interview, current_user)
    is_candidate = _is_owning_candidate(interview, current_user)
    if not (is_recruiter or is_candidate):
        raise PermissionDeniedError("You don't have access to this interview.")

    # Candidates taking an in-progress interview shouldn't see scores/answers
    # for questions ahead of them; recruiters and completed interviews show everything.
    include_answers = is_recruiter or interview.status == InterviewStatus.completed
    return APIResponse(success=True, message="Interview", data=_to_response(interview, include_answers))


@router.post("/{interview_id}/generate-questions", response_model=APIResponse[InterviewResponse])
def regenerate_interview_questions(
    interview_id: str,
    num_questions: int = Query(default=6, ge=1, le=15),
    current_user: User = Depends(require_role(UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    try:
        parsed_id = uuid.UUID(interview_id)
    except ValueError:
        raise NotFoundError("Interview not found")

    interview = interview_service.load_interview(db, parsed_id)
    if not interview:
        raise NotFoundError("Interview not found")
    if not _is_owning_recruiter(interview, current_user):
        raise PermissionDeniedError("You can only manage interviews for your own job postings.")

    interview = regenerate_questions(db, interview, num_questions)
    return APIResponse(success=True, message="Questions regenerated", data=_to_response(interview, include_answers=True))


@router.post("/{interview_id}/answers", response_model=APIResponse[AnswerResponse], status_code=201)
def submit_interview_answer(
    interview_id: str,
    payload: AnswerSubmit,
    current_user: User = Depends(require_role(UserRole.candidate)),
    db: Session = Depends(get_db),
):
    try:
        parsed_id = uuid.UUID(interview_id)
    except ValueError:
        raise NotFoundError("Interview not found")

    interview = interview_service.load_interview(db, parsed_id)
    if not interview:
        raise NotFoundError("Interview not found")
    if not _is_owning_candidate(interview, current_user):
        raise PermissionDeniedError("You can only answer your own interview questions.")

    answer = submit_answer(db, interview, payload.question_id, payload.answer_text, answer_source="text")

    # Re-fetch to get the (possibly just-updated) interview status.
    refreshed = interview_service.load_interview(db, parsed_id)
    feedback = json.loads(answer.feedback) if answer.feedback else {}

    return APIResponse(
        success=True,
        message="Answer submitted",
        data=AnswerResponse(
            id=answer.id,
            question_id=answer.question_id,
            answer_text=answer.answer_text,
            answer_source=answer.answer_source,
            answer_score=answer.answer_score,
            strengths=feedback.get("strengths", []),
            improvements=feedback.get("improvements", []),
            interview_status=refreshed.status,
        ),
    )


@router.post("/{interview_id}/evaluate", response_model=APIResponse[InterviewResponse])
def evaluate_interview_endpoint(
    interview_id: str,
    current_user: User = Depends(require_role(UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    try:
        parsed_id = uuid.UUID(interview_id)
    except ValueError:
        raise NotFoundError("Interview not found")

    interview = interview_service.load_interview(db, parsed_id)
    if not interview:
        raise NotFoundError("Interview not found")
    if not _is_owning_recruiter(interview, current_user):
        raise PermissionDeniedError("You can only evaluate interviews for your own job postings.")

    interview = force_evaluate(db, interview)
    return APIResponse(success=True, message="Interview evaluated", data=_to_response(interview, include_answers=True))


@router.get("/{interview_id}/report", response_model=APIResponse[InterviewReport])
def get_interview_report(
    interview_id: str,
    current_user: User = Depends(require_role(UserRole.candidate, UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    try:
        parsed_id = uuid.UUID(interview_id)
    except ValueError:
        raise NotFoundError("Interview not found")

    interview = interview_service.load_interview(db, parsed_id)
    if not interview:
        raise NotFoundError("Interview not found")

    is_recruiter = _is_owning_recruiter(interview, current_user)
    is_candidate = _is_owning_candidate(interview, current_user)
    if not (is_recruiter or is_candidate):
        raise PermissionDeniedError("You don't have access to this interview report.")

    report = build_report(interview)
    return APIResponse(success=True, message="Interview report", data=InterviewReport(**report))


@router.get("", response_model=APIResponse[list[InterviewResponse]])
def list_interviews(
    current_user: User = Depends(require_role(UserRole.candidate, UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    query = db.query(Interview)
    if current_user.role == UserRole.candidate:
        profile = db.query(CandidateProfile).filter(CandidateProfile.user_id == current_user.id).first()
        if not profile:
            return APIResponse(success=True, message="Interviews", data=[])
        interviews = query.filter(Interview.candidate_id == profile.id).all()
        return APIResponse(
            success=True,
            message="Interviews",
            data=[
                _to_response(
                    interview_service.load_interview(db, i.id), include_answers=i.status == InterviewStatus.completed
                )
                for i in interviews
            ],
        )

    # Recruiter: interviews across their own jobs.
    interviews = query.join(Job, Interview.job_id == Job.id).filter(Job.recruiter_id == current_user.id).all()
    return APIResponse(
        success=True,
        message="Interviews",
        data=[_to_response(interview_service.load_interview(db, i.id), include_answers=True) for i in interviews],
    )
