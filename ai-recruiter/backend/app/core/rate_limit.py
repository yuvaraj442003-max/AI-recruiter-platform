"""
rate_limit.py — two lightweight, in-memory rate limiters:

1. A sliding-window limiter per client IP, used on /auth/register to
   blunt automated mass account creation.
2. A failed-login lockout per email, used on /auth/login — after
   repeated wrong passwords for the same email within a window, further
   attempts are rejected even with the correct password, until the
   window expires. This is the standard defense against credential
   stuffing/brute force and, unlike a blanket per-IP login limit,
   doesn't accidentally lock out a whole office behind one NAT'd IP.

In-memory storage is fine for a single process; a multi-instance
deployment should back this with Redis instead (swap the storage dict
for a Redis client — the counting logic here stays the same).
"""
import time
from collections import defaultdict

from app.core.config import settings
from app.core.exceptions import AppError


class RateLimitError(AppError):
    def __init__(self, message: str = "Too many requests. Please try again later."):
        super().__init__(message, "RATE_LIMITED", 429)


class AccountLockedError(AppError):
    def __init__(self, message: str = "Too many failed login attempts. Please try again in a few minutes."):
        super().__init__(message, "ACCOUNT_TEMPORARILY_LOCKED", 429)


_ip_request_log: dict[str, list[float]] = defaultdict(list)
_failed_login_log: dict[str, list[float]] = defaultdict(list)


def _prune(timestamps: list[float], window_seconds: float) -> list[float]:
    cutoff = time.time() - window_seconds
    return [t for t in timestamps if t > cutoff]


def check_ip_rate_limit(key: str, max_requests: int | None = None, window_seconds: int = 60) -> None:
    limit = max_requests if max_requests is not None else settings.RATE_LIMIT_REGISTER_PER_MINUTE
    timestamps = _prune(_ip_request_log[key], window_seconds)
    if len(timestamps) >= limit:
        _ip_request_log[key] = timestamps
        raise RateLimitError()
    timestamps.append(time.time())
    _ip_request_log[key] = timestamps


def record_failed_login(email: str) -> None:
    key = email.lower()
    timestamps = _prune(_failed_login_log[key], settings.LOGIN_LOCKOUT_WINDOW_SECONDS)
    timestamps.append(time.time())
    _failed_login_log[key] = timestamps


def check_login_lockout(email: str) -> None:
    key = email.lower()
    timestamps = _prune(_failed_login_log[key], settings.LOGIN_LOCKOUT_WINDOW_SECONDS)
    _failed_login_log[key] = timestamps
    if len(timestamps) >= settings.LOGIN_LOCKOUT_MAX_ATTEMPTS:
        raise AccountLockedError()


def clear_failed_logins(email: str) -> None:
    _failed_login_log.pop(email.lower(), None)


def _clear_all_state_for_tests() -> None:
    """Test-only helper: resets both limiters so tests don't leak state into each other."""
    _ip_request_log.clear()
    _failed_login_log.clear()
