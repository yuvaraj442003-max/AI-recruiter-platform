"""
audit.py — writes AuditLog rows for security-relevant and
recruitment-decision events. Failures here are logged and swallowed,
never raised — an audit-log write must never break the actual request
it's describing.

Never pass passwords, tokens, full resume text, or full interview
answers into `details` — keep it to short, structured facts (e.g. an
old/new status, an email, a role).
"""
import json
import logging

from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog

logger = logging.getLogger("ai_recruiter.audit")


def log_action(db: Session, action: str, user_id=None, details: dict | None = None, ip_address: str | None = None) -> None:
    try:
        entry = AuditLog(
            user_id=user_id,
            action=action,
            details=json.dumps(details) if details else None,
            ip_address=ip_address,
        )
        db.add(entry)
        db.commit()
    except Exception:
        logger.exception("Failed to write audit log for action '%s'", action)
        db.rollback()
