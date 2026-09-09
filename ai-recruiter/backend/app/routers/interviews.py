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


# --- Schedule & Calendar Extensions ---

from datetime import datetime, timedelta, timezone
from pydantic import BaseModel, Field
from fastapi.responses import Response
from sqlalchemy import select
from app.models.calendar import ScheduledInterview, ScheduledInterviewStatus
from app.services.calendar_service import CalendarService, generate_google_calendar_add_url, generate_outlook_calendar_add_url
from app.services.ics_service import generate_ics_content
from app.services.email_service import (
    send_interview_invitation_email,
    send_interview_rescheduled_email,
    send_interview_cancelled_email,
)
from app.services.reminder_service import _dispatch_reminder, check_and_send_interview_reminders


class ScheduleInterviewRequest(BaseModel):
    candidate_id: str
    job_id: str
    start_time_iso: str # e.g. 2026-09-10T10:00:00Z
    duration_minutes: int = 30
    timezone_name: str = "Asia/Kolkata"
    interview_type: str = "AI Technical Interview"
    send_email: bool = True
    sync_calendar: bool = True


class RescheduleInterviewRequest(BaseModel):
    new_start_time_iso: str
    duration_minutes: int = 30
    timezone_name: str = "Asia/Kolkata"
    send_email: bool = True


@router.post("/schedule", status_code=201)
def schedule_interview(
    payload: ScheduleInterviewRequest,
    current_user: User = Depends(require_role(UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    cand_id = uuid.UUID(payload.candidate_id)
    job_id = uuid.UUID(payload.job_id)

    cand_profile = db.scalar(select(CandidateProfile).where(CandidateProfile.id == cand_id))
    if not cand_profile:
        raise NotFoundError("Candidate profile not found")
    job = db.scalar(select(Job).where(Job.id == job_id))
    if not job:
        raise NotFoundError("Job not found")

    start_dt = datetime.fromisoformat(payload.start_time_iso.replace("Z", "+00:00"))
    if not start_dt.tzinfo:
        start_dt = start_dt.replace(tzinfo=timezone.utc)
    end_dt = start_dt + timedelta(minutes=payload.duration_minutes)

    # Create base Interview record if none exists
    existing_interview = db.scalar(
        select(Interview).where(Interview.candidate_id == cand_id, Interview.job_id == job_id)
    )
    if not existing_interview:
        base_type = payload.interview_type if payload.interview_type in ["technical", "behavioral", "mixed", "ai_interview"] else "mixed"
        existing_interview = create_interview(
            db, recruiter_id=current_user.id, candidate_profile_id=cand_id, job_id=job_id, interview_type=base_type
        )

    title = f"{job.title} Interview - {cand_profile.user.name if cand_profile.user else 'Candidate'}"

    scheduled = ScheduledInterview(
        interview_id=existing_interview.id,
        candidate_id=cand_id,
        recruiter_id=current_user.id,
        job_id=job_id,
        title=title,
        interview_type=payload.interview_type,
        duration_minutes=payload.duration_minutes,
        start_time_utc=start_dt,
        end_time_utc=end_dt,
        timezone=payload.timezone_name,
        status=ScheduledInterviewStatus.scheduled,
    )
    db.add(scheduled)
    db.commit()
    db.refresh(scheduled)

    if payload.sync_calendar:
        CalendarService.sync_calendar_event(db, scheduled, action="create")

    # Dispatch email if requested
    from app.core.config import settings
    room_link = f"{settings.FRONTEND_URL.rstrip('/')}/live-interview-room.html?interview_id={existing_interview.id}"
    cand_user = cand_profile.user
    if payload.send_email and cand_user and cand_user.email:
        date_str = start_dt.strftime("%B %d, %Y")
        time_str = f"{start_dt.strftime('%I:%M %p')} ({payload.timezone_name})"
        comp_name = job.company_name or f"{current_user.name}'s Company"

        send_interview_invitation_email(
            to_email=cand_user.email,
            candidate_name=cand_user.name,
            company_name=comp_name,
            job_title=job.title,
            interview_date=date_str,
            interview_time=time_str,
            location_or_link=room_link,
            duration=payload.duration_minutes,
            interview_type=payload.interview_type,
            candidate_id=cand_id,
            job_id=job_id,
            interview_id=existing_interview.id,
            recruiter_id=current_user.id,
            db=db,
        )

    return APIResponse(
        success=True,
        message="Interview scheduled successfully",
        data={
            "scheduled_id": str(scheduled.id),
            "interview_id": str(existing_interview.id),
            "title": scheduled.title,
            "start_time_utc": scheduled.start_time_utc,
            "timezone": scheduled.timezone,
            "status": scheduled.status.value,
            "calendar_sync_status": scheduled.calendar_sync_status,
            "join_link": room_link,
        },
    )


@router.put("/{interview_id}/reschedule")
def reschedule_interview(
    interview_id: str,
    payload: RescheduleInterviewRequest,
    current_user: User = Depends(require_role(UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    parsed_id = uuid.UUID(interview_id)
    scheduled = db.scalar(select(ScheduledInterview).where(ScheduledInterview.interview_id == parsed_id))
    if not scheduled:
        scheduled = db.scalar(select(ScheduledInterview).where(ScheduledInterview.id == parsed_id))
    if not scheduled:
        raise NotFoundError("Scheduled interview record not found")

    if scheduled.recruiter_id != current_user.id:
        raise PermissionDeniedError("You can only reschedule your own interviews.")

    start_dt = datetime.fromisoformat(payload.new_start_time_iso.replace("Z", "+00:00"))
    if not start_dt.tzinfo:
        start_dt = start_dt.replace(tzinfo=timezone.utc)
    end_dt = start_dt + timedelta(minutes=payload.duration_minutes)

    scheduled.start_time_utc = start_dt
    scheduled.end_time_utc = end_dt
    scheduled.timezone = payload.timezone_name
    scheduled.duration_minutes = payload.duration_minutes
    scheduled.status = ScheduledInterviewStatus.rescheduled
    scheduled.reminder_24h_sent = False
    scheduled.reminder_1h_sent = False

    db.commit()

    CalendarService.sync_calendar_event(db, scheduled, action="update")

    if payload.send_email and scheduled.candidate and scheduled.candidate.user:
        cand_user = scheduled.candidate.user
        job = scheduled.job
        date_str = start_dt.strftime("%B %d, %Y")
        time_str = f"{start_dt.strftime('%I:%M %p')} ({payload.timezone_name})"

        from app.core.config import settings
        link = f"{settings.FRONTEND_URL.rstrip('/')}/live-interview-room.html?interview_id={scheduled.interview_id or scheduled.id}"

        send_interview_rescheduled_email(
            to_email=cand_user.email,
            candidate_name=cand_user.name,
            job_title=job.title if job else "Position",
            company_name=job.company_name if (job and job.company_name) else "AI Recruiter",
            new_date=date_str,
            new_time=time_str,
            duration=payload.duration_minutes,
            interview_link=link,
            candidate_id=scheduled.candidate_id,
            job_id=scheduled.job_id,
            interview_id=scheduled.interview_id,
            recruiter_id=current_user.id,
            db=db,
        )

    return APIResponse(success=True, message="Interview rescheduled successfully", data={"status": scheduled.status.value, "new_start": start_dt})


@router.post("/{interview_id}/cancel")
def cancel_interview(
    interview_id: str,
    current_user: User = Depends(require_role(UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    parsed_id = uuid.UUID(interview_id)
    scheduled = db.scalar(select(ScheduledInterview).where(ScheduledInterview.interview_id == parsed_id))
    if not scheduled:
        scheduled = db.scalar(select(ScheduledInterview).where(ScheduledInterview.id == parsed_id))
    if not scheduled:
        raise NotFoundError("Scheduled interview record not found")

    if scheduled.recruiter_id != current_user.id:
        raise PermissionDeniedError("You can only cancel your own interviews.")

    scheduled.status = ScheduledInterviewStatus.cancelled
    scheduled.cancelled_at = datetime.now(timezone.utc)
    db.commit()

    CalendarService.sync_calendar_event(db, scheduled, action="cancel")

    if scheduled.candidate and scheduled.candidate.user:
        cand_user = scheduled.candidate.user
        job = scheduled.job
        send_interview_cancelled_email(
            to_email=cand_user.email,
            candidate_name=cand_user.name,
            job_title=job.title if job else "Position",
            company_name=job.company_name if (job and job.company_name) else "AI Recruiter",
            candidate_id=scheduled.candidate_id,
            job_id=scheduled.job_id,
            interview_id=scheduled.interview_id,
            recruiter_id=current_user.id,
            db=db,
        )

    return APIResponse(success=True, message="Interview cancelled successfully")


@router.post("/{interview_id}/reminder")
def trigger_manual_reminder(
    interview_id: str,
    current_user: User = Depends(require_role(UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    parsed_id = uuid.UUID(interview_id)
    scheduled = db.scalar(select(ScheduledInterview).where(ScheduledInterview.interview_id == parsed_id))
    if not scheduled:
        scheduled = db.scalar(select(ScheduledInterview).where(ScheduledInterview.id == parsed_id))
    if not scheduled:
        raise NotFoundError("Scheduled interview record not found")

    sent = _dispatch_reminder(db, scheduled, reminder_type="manual")
    return APIResponse(success=sent, message="Reminder sent" if sent else "Failed to send reminder")


@router.get("/{interview_id}/ics")
def download_interview_ics(
    interview_id: str,
    db: Session = Depends(get_db),
):
    parsed_id = uuid.UUID(interview_id)
    scheduled = db.scalar(select(ScheduledInterview).where(ScheduledInterview.interview_id == parsed_id))
    if not scheduled:
        scheduled = db.scalar(select(ScheduledInterview).where(ScheduledInterview.id == parsed_id))
    
    if not scheduled:
        # Fallback dummy event
        ics_text = generate_ics_content(
            summary="AI Recruiter Technical Interview",
            description="Live AI Voice Interview",
            start_time_utc=datetime.now(timezone.utc) + timedelta(days=1),
            end_time_utc=datetime.now(timezone.utc) + timedelta(days=1, minutes=30),
        )
    else:
        from app.core.config import settings
        link = f"{settings.FRONTEND_URL.rstrip('/')}/live-interview-room.html?interview_id={scheduled.interview_id or scheduled.id}"
        cand_name = scheduled.candidate.user.name if (scheduled.candidate and scheduled.candidate.user) else "Candidate"
        cand_email = scheduled.candidate.user.email if (scheduled.candidate and scheduled.candidate.user) else None

        ics_text = generate_ics_content(
            summary=scheduled.title,
            description=f"Interview for {scheduled.job.title if scheduled.job else 'Position'}. Join link: {link}",
            start_time_utc=scheduled.start_time_utc,
            end_time_utc=scheduled.end_time_utc,
            location_or_url=link,
            attendee_name=cand_name,
            attendee_email=cand_email,
            uid=f"interview_{scheduled.id}@airecruiter.com",
        )

    return Response(
        content=ics_text,
        media_type="text/calendar",
        headers={"Content-Disposition": 'attachment; filename="Interview_Invitation.ics"'},
    )


@router.get("/upcoming")
def list_upcoming_interviews(
    current_user: User = Depends(require_role(UserRole.candidate, UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    from app.core.config import settings
    query = select(ScheduledInterview).where(ScheduledInterview.status != ScheduledInterviewStatus.cancelled)

    if current_user.role == UserRole.candidate:
        cand_profile = db.scalar(select(CandidateProfile).where(CandidateProfile.user_id == current_user.id))
        if not cand_profile:
            return APIResponse(success=True, message="Upcoming interviews", data=[])
        sessions = db.scalars(query.where(ScheduledInterview.candidate_id == cand_profile.id).order_by(ScheduledInterview.start_time_utc.asc())).all()
    else:
        sessions = db.scalars(query.where(ScheduledInterview.recruiter_id == current_user.id).order_by(ScheduledInterview.start_time_utc.asc())).all()

    result = []
    for s in sessions:
        room_link = f"{settings.FRONTEND_URL.rstrip('/')}/live-interview-room.html?interview_id={s.interview_id or s.id}"
        google_add = generate_google_calendar_add_url(s.title, f"Join: {room_link}", s.start_time_utc, s.end_time_utc, room_link)
        outlook_add = generate_outlook_calendar_add_url(s.title, f"Join: {room_link}", s.start_time_utc, s.end_time_utc, room_link)

        result.append({
            "id": str(s.id),
            "interview_id": str(s.interview_id) if s.interview_id else None,
            "title": s.title,
            "candidate_name": s.candidate.user.name if (s.candidate and s.candidate.user) else "Candidate",
            "job_title": s.job.title if s.job else "Role",
            "interview_type": s.interview_type,
            "duration_minutes": s.duration_minutes,
            "start_time_utc": s.start_time_utc,
            "end_time_utc": s.end_time_utc,
            "timezone": s.timezone,
            "status": s.status.value,
            "calendar_provider": s.calendar_provider,
            "calendar_sync_status": s.calendar_sync_status,
            "join_link": room_link,
            "google_calendar_url": google_add,
            "outlook_calendar_url": outlook_add,
            "ics_download_url": f"{settings.FRONTEND_URL.rstrip('/')}/api/v1/interviews/{s.id}/ics",
        })

    return APIResponse(success=True, message="Upcoming interviews", data=result)

