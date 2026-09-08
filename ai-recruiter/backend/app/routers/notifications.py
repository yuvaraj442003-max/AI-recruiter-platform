"""
Notification router — endpoints for fetching, managing, and streaming in-app notifications.
"""
import uuid
from typing import Dict, List
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.schemas.common import APIResponse
from app.services import notification_service

router = APIRouter(prefix="/notifications", tags=["Notifications"])


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}

    async def connect(self, user_id: str, websocket: WebSocket):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, user_id: str, websocket: WebSocket):
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)

    async def send_personal_message(self, message: dict, user_id: str):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_json(message)
                except Exception:
                    pass


ws_manager = ConnectionManager()


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await ws_manager.connect(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()
            await websocket.send_json({"type": "pong", "event": "heartbeat"})
    except WebSocketDisconnect:
        ws_manager.disconnect(user_id, websocket)


@router.get("", response_model=APIResponse[list[dict]])
def get_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    notifications = notification_service.get_user_notifications(db, current_user.id)
    data = [
        {
            "id": str(n.id),
            "title": n.title,
            "message": n.message,
            "type": n.type,
            "link": n.link,
            "is_read": n.is_read,
            "created_at": n.created_at.isoformat() if n.created_at else None,
        }
        for n in notifications
    ]
    return APIResponse(success=True, message="Notifications fetched", data=data)


@router.patch("/{notification_id}/read", response_model=APIResponse[dict])
def mark_read(
    notification_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    notification_service.mark_notification_read(db, notification_id, current_user.id)
    return APIResponse(success=True, message="Notification marked as read", data={"id": str(notification_id)})


@router.post("/read-all", response_model=APIResponse[dict])
def mark_all_read(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    count = notification_service.mark_all_notifications_read(db, current_user.id)
    return APIResponse(success=True, message="All notifications marked as read", data={"updated_count": count})


from app.models.email_log import EmailLog
from app.models.user import UserRole


@router.get("/email-logs", response_model=APIResponse[list[dict]])
def list_email_logs(
    to_email: str = None,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(EmailLog)
    if to_email:
        query = query.filter(EmailLog.to_email == to_email.strip().lower())
    elif current_user.role not in [UserRole.admin, UserRole.superadmin]:
        query = query.filter(EmailLog.to_email == current_user.email.strip().lower())
    logs = query.order_by(EmailLog.created_at.desc()).limit(limit).all()
    data = [
        {
            "id": str(l.id),
            "to_email": l.to_email,
            "subject": l.subject,
            "email_type": l.email_type,
            "status": l.status,
            "error_message": l.error_message,
            "created_at": l.created_at.isoformat() if l.created_at else None,
            "sent_at": l.sent_at.isoformat() if l.sent_at else None,
        }
        for l in logs
    ]
    return APIResponse(success=True, message="Email logs fetched", data=data)

