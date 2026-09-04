"""
Messaging & Chat endpoints for Recruiter <-> Candidate communication.
"""
import uuid
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, desc, func

from app.core.database import get_db
from app.core.deps import get_current_user
from app.core.exceptions import NotFoundError, BadRequestError
from app.models.user import User, UserRole
from app.models.message import ChatMessage
from app.models.candidate import CandidateProfile
from app.models.recruiter import RecruiterProfile
from app.models.application import Application
from app.models.job import Job
from app.schemas.common import APIResponse
from app.schemas.message import (
    ContactResponse,
    ConversationResponse,
    MessageCreate,
    MessageResponse,
    UnreadCountResponse,
)
from app.services.notification_service import create_notification
from app.utils.audit import log_action

router = APIRouter(prefix="/messages", tags=["Messaging & Chat"])


def _get_user_headline_or_company(db: Session, user: User) -> str:
    if user.role == UserRole.candidate:
        prof = db.query(CandidateProfile).filter(CandidateProfile.user_id == user.id).first()
        if prof:
            return prof.headline or prof.current_role or "Candidate"
        return "Candidate"
    elif user.role in [UserRole.recruiter, UserRole.company_admin]:
        prof = db.query(RecruiterProfile).filter(RecruiterProfile.user_id == user.id).first()
        if prof:
            return prof.company_name or prof.job_title or "Recruiter"
        return "Recruiter"
    return "System Administrator"


@router.post("/send", response_model=APIResponse[MessageResponse], status_code=status.HTTP_201_CREATED)
def send_message(
    payload: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Sends a chat message to another candidate or recruiter."""
    if not payload.content or not payload.content.strip():
        raise BadRequestError("Message content cannot be empty")

    receiver = db.get(User, payload.receiver_id)
    if not receiver:
        raise NotFoundError("Recipient user not found")

    if receiver.id == current_user.id:
        raise BadRequestError("You cannot send a message to yourself")

    msg = ChatMessage(
        sender_id=current_user.id,
        receiver_id=receiver.id,
        application_id=payload.application_id,
        content=payload.content.strip(),
        is_read=False,
    )
    db.add(msg)
    db.commit()
    db.refresh(msg)

    # Notify recipient
    create_notification(
        db=db,
        user_id=receiver.id,
        title=f"New Message from {current_user.name}",
        message=msg.content[:100] + ("..." if len(msg.content) > 100 else ""),
        notification_type="info",
        link="/candidate-dashboard.html" if receiver.role == UserRole.candidate else "/recruiter-dashboard.html",
    )

    log_action(db, "message.send", user_id=current_user.id, details={"receiver_id": str(receiver.id)})

    resp = MessageResponse(
        id=msg.id,
        sender_id=msg.sender_id,
        sender_name=current_user.name,
        sender_role=current_user.role.value,
        receiver_id=msg.receiver_id,
        receiver_name=receiver.name,
        receiver_role=receiver.role.value,
        application_id=msg.application_id,
        content=msg.content,
        is_read=msg.is_read,
        created_at=msg.created_at,
    )
    return APIResponse(success=True, message="Message sent successfully", data=resp)


@router.get("/thread/{other_user_id}", response_model=APIResponse[List[MessageResponse]])
def get_message_thread(
    other_user_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieves full conversation thread between current user and another user."""
    other_user = db.get(User, other_user_id)
    if not other_user:
        raise NotFoundError("User not found")

    # Mark incoming messages from other_user to current_user as read
    unread_messages = (
        db.query(ChatMessage)
        .filter(
            ChatMessage.sender_id == other_user_id,
            ChatMessage.receiver_id == current_user.id,
            ChatMessage.is_read == False,
        )
        .all()
    )
    if unread_messages:
        for m in unread_messages:
            m.is_read = True
        db.commit()

    messages = (
        db.query(ChatMessage)
        .filter(
            or_(
                and_(ChatMessage.sender_id == current_user.id, ChatMessage.receiver_id == other_user_id),
                and_(ChatMessage.sender_id == other_user_id, ChatMessage.receiver_id == current_user.id),
            )
        )
        .order_by(ChatMessage.created_at.asc())
        .all()
    )

    user_cache = {
        current_user.id: (current_user.name, current_user.role.value),
        other_user.id: (other_user.name, other_user.role.value),
    }

    result = []
    for m in messages:
        s_name, s_role = user_cache.get(m.sender_id, ("User", "user"))
        r_name, r_role = user_cache.get(m.receiver_id, ("User", "user"))
        result.append(
            MessageResponse(
                id=m.id,
                sender_id=m.sender_id,
                sender_name=s_name,
                sender_role=s_role,
                receiver_id=m.receiver_id,
                receiver_name=r_name,
                receiver_role=r_role,
                application_id=m.application_id,
                content=m.content,
                is_read=m.is_read,
                created_at=m.created_at,
            )
        )

    return APIResponse(success=True, message="Message thread", data=result)


@router.get("/conversations", response_model=APIResponse[List[ConversationResponse]])
def get_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieves list of active conversation channels for current user."""
    # Find all distinct partners
    sent_msgs = db.query(ChatMessage.receiver_id.label("partner_id")).filter(ChatMessage.sender_id == current_user.id)
    recv_msgs = db.query(ChatMessage.sender_id.label("partner_id")).filter(ChatMessage.receiver_id == current_user.id)
    partners_query = sent_msgs.union(recv_msgs).distinct()
    partner_ids = [r.partner_id for r in partners_query.all()]

    conversations = []
    for partner_id in partner_ids:
        partner = db.get(User, partner_id)
        if not partner:
            continue

        last_msg = (
            db.query(ChatMessage)
            .filter(
                or_(
                    and_(ChatMessage.sender_id == current_user.id, ChatMessage.receiver_id == partner_id),
                    and_(ChatMessage.sender_id == partner_id, ChatMessage.receiver_id == current_user.id),
                )
            )
            .order_by(desc(ChatMessage.created_at))
            .first()
        )

        if not last_msg:
            continue

        unread = (
            db.query(func.count(ChatMessage.id))
            .filter(
                ChatMessage.sender_id == partner_id,
                ChatMessage.receiver_id == current_user.id,
                ChatMessage.is_read == False,
            )
            .scalar()
            or 0
        )

        company_or_hl = _get_user_headline_or_company(db, partner)

        conversations.append(
            ConversationResponse(
                other_user_id=partner.id,
                other_user_name=partner.name,
                other_user_role=partner.role.value,
                other_user_email=partner.email,
                company_or_headline=company_or_hl,
                last_message=last_msg.content,
                last_message_at=last_msg.created_at,
                unread_count=unread,
                application_id=last_msg.application_id,
            )
        )

    conversations.sort(key=lambda c: c.last_message_at, reverse=True)
    return APIResponse(success=True, message="Conversations list", data=conversations)


@router.get("/contacts", response_model=APIResponse[List[ContactResponse]])
def get_contacts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Retrieves eligible contacts for current candidate or recruiter."""
    contacts = []
    seen_user_ids = set()

    if current_user.role == UserRole.candidate:
        # Candidate contacts: Recruiters who posted jobs candidate applied for + other active recruiters & candidates
        applied_recruiters = (
            db.query(User, Job.title, Application.id)
            .join(Job, Job.recruiter_id == User.id)
            .join(Application, Application.job_id == Job.id)
            .join(CandidateProfile, Application.candidate_id == CandidateProfile.id)
            .filter(CandidateProfile.user_id == current_user.id)
            .all()
        )
        for rec_user, job_title, app_id in applied_recruiters:
            if rec_user.id not in seen_user_ids:
                seen_user_ids.add(rec_user.id)
                comp = _get_user_headline_or_company(db, rec_user)
                contacts.append(
                    ContactResponse(
                        user_id=rec_user.id,
                        name=rec_user.name,
                        email=rec_user.email,
                        role=rec_user.role.value,
                        company_or_headline=comp,
                        application_id=app_id,
                        job_title=job_title,
                    )
                )

        all_recruiters = db.query(User).filter(User.role.in_([UserRole.recruiter, UserRole.company_admin])).all()
        for rec_user in all_recruiters:
            if rec_user.id not in seen_user_ids and rec_user.id != current_user.id:
                seen_user_ids.add(rec_user.id)
                comp = _get_user_headline_or_company(db, rec_user)
                contacts.append(
                    ContactResponse(
                        user_id=rec_user.id,
                        name=rec_user.name,
                        email=rec_user.email,
                        role=rec_user.role.value,
                        company_or_headline=comp,
                    )
                )

    elif current_user.role in [UserRole.recruiter, UserRole.company_admin]:
        # Recruiter contacts: Candidates who applied to recruiter's jobs + all active candidates
        applicant_candidates = (
            db.query(User, Job.title, Application.id)
            .join(CandidateProfile, CandidateProfile.user_id == User.id)
            .join(Application, Application.candidate_id == CandidateProfile.id)
            .join(Job, Application.job_id == Job.id)
            .filter(Job.recruiter_id == current_user.id)
            .all()
        )
        for cand_user, job_title, app_id in applicant_candidates:
            if cand_user.id not in seen_user_ids:
                seen_user_ids.add(cand_user.id)
                hl = _get_user_headline_or_company(db, cand_user)
                contacts.append(
                    ContactResponse(
                        user_id=cand_user.id,
                        name=cand_user.name,
                        email=cand_user.email,
                        role=cand_user.role.value,
                        company_or_headline=hl,
                        application_id=app_id,
                        job_title=job_title,
                    )
                )

        all_candidates = db.query(User).filter(User.role == UserRole.candidate).all()
        for cand_user in all_candidates:
            if cand_user.id not in seen_user_ids and cand_user.id != current_user.id:
                seen_user_ids.add(cand_user.id)
                hl = _get_user_headline_or_company(db, cand_user)
                contacts.append(
                    ContactResponse(
                        user_id=cand_user.id,
                        name=cand_user.name,
                        email=cand_user.email,
                        role=cand_user.role.value,
                        company_or_headline=hl,
                    )
                )

    # General fallback: include all other users so messaging is completely open and unified
    all_users = db.query(User).all()
    for u in all_users:
        if u.id not in seen_user_ids and u.id != current_user.id:
            seen_user_ids.add(u.id)
            hl_or_comp = _get_user_headline_or_company(db, u)
            contacts.append(
                ContactResponse(
                    user_id=u.id,
                    name=u.name,
                    email=u.email,
                    role=u.role.value,
                    company_or_headline=hl_or_comp,
                )
            )

    return APIResponse(success=True, message="Contacts list", data=contacts)


@router.get("/unread-count", response_model=APIResponse[UnreadCountResponse])
def get_unread_count(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Returns total unread messages count for logged-in user across all conversations."""
    unread = (
        db.query(func.count(ChatMessage.id))
        .filter(ChatMessage.receiver_id == current_user.id, ChatMessage.is_read == False)
        .scalar()
        or 0
    )
    return APIResponse(success=True, message="Unread count", data=UnreadCountResponse(unread_count=unread))
