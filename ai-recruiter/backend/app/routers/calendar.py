"""
calendar.py — API Router for Google & Outlook OAuth Calendar Integration.
"""
from typing import Optional
from fastapi import APIRouter, Depends, Query, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import require_role
from app.models.user import User, UserRole
from app.schemas.common import APIResponse
from app.services.calendar_service import CalendarService

router = APIRouter(prefix="/calendar", tags=["Calendar Integration"])


@router.get("/connect/google")
def connect_google_calendar(current_user: User = Depends(require_role(UserRole.recruiter))):
    auth_url = CalendarService.get_google_auth_url(current_user.id)
    return APIResponse(success=True, message="Google OAuth URL", data={"auth_url": auth_url})


@router.get("/connect/outlook")
def connect_outlook_calendar(current_user: User = Depends(require_role(UserRole.recruiter))):
    auth_url = CalendarService.get_outlook_auth_url(current_user.id)
    return APIResponse(success=True, message="Outlook OAuth URL", data={"auth_url": auth_url})


@router.get("/callback/google")
def google_calendar_callback(
    code: str = Query(..., description="Authorization code"),
    state: str = Query(..., description="Recruiter ID"),
    db: Session = Depends(get_db),
):
    conn = CalendarService.process_oauth_callback(db, state, provider="google", code=code)
    return APIResponse(success=True, message="Google Calendar connected successfully", data={"connected": conn.connected, "provider": conn.provider})


@router.get("/callback/outlook")
def outlook_calendar_callback(
    code: str = Query(..., description="Authorization code"),
    state: str = Query(..., description="Recruiter ID"),
    db: Session = Depends(get_db),
):
    conn = CalendarService.process_oauth_callback(db, state, provider="outlook", code=code)
    return APIResponse(success=True, message="Outlook Calendar connected successfully", data={"connected": conn.connected, "provider": conn.provider})


@router.post("/disconnect")
def disconnect_calendar(
    provider: str = Query(default="google"),
    current_user: User = Depends(require_role(UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    success = CalendarService.disconnect_calendar(db, current_user.id, provider)
    return APIResponse(success=success, message=f"{provider.capitalize()} Calendar disconnected" if success else "Not connected")


@router.get("/status")
def get_calendar_status(
    current_user: User = Depends(require_role(UserRole.recruiter)),
    db: Session = Depends(get_db),
):
    status = CalendarService.get_recruiter_calendar_status(db, current_user.id)
    return APIResponse(success=True, message="Calendar Status", data=status)
