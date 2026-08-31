"""
Reusable FastAPI dependencies for authentication and role-based access control.
"""
import uuid

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import AuthError, PermissionDeniedError
from app.core.security import decode_token
from app.models.user import User, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    if not token:
        raise AuthError("Not authenticated")

    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        raise AuthError("Invalid or expired token")

    try:
        user_id = uuid.UUID(payload.get("sub"))
    except (TypeError, ValueError):
        raise AuthError("Invalid token subject")

    user = db.get(User, user_id)
    if not user:
        raise AuthError("User no longer exists")

    return user


def get_optional_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User | None:
    if not token:
        return None
    try:
        payload = decode_token(token)
        if not payload or payload.get("type") != "access":
            return None
        user_id = uuid.UUID(payload.get("sub"))
        return db.get(User, user_id)
    except Exception:
        return None



def require_role(*allowed_roles: UserRole):
    """Dependency factory: restricts an endpoint to one or more roles."""

    def _check(current_user: User = Depends(get_current_user)) -> User:
        user_role = current_user.role
        # Check if user is active
        if not getattr(current_user, "is_active", True):
            raise PermissionDeniedError("Your account has been suspended. Please contact support.")

        if user_role == UserRole.superadmin:
            return current_user

        if user_role not in allowed_roles:
            raise PermissionDeniedError(
                f"This action requires one of the following roles: {[r.value for r in allowed_roles]}"
            )
        return current_user

    return _check

