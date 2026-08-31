"""
Custom application exceptions and global FastAPI exception handlers,
so every error response follows the same {success, message, error_code} shape.
"""
import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("ai_recruiter")


class AppError(Exception):
    """Base class for predictable, user-facing application errors."""

    def __init__(self, message: str, error_code: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code


class AuthError(AppError):
    def __init__(self, message: str = "Authentication failed", error_code: str = "AUTH_ERROR"):
        super().__init__(message, error_code, status.HTTP_401_UNAUTHORIZED)


class PermissionDeniedError(AppError):
    def __init__(self, message: str = "You do not have access to this resource"):
        super().__init__(message, "PERMISSION_DENIED", status.HTTP_403_FORBIDDEN)


class NotFoundError(AppError):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, "NOT_FOUND", status.HTTP_404_NOT_FOUND)


class ConflictError(AppError):
    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, "CONFLICT", status.HTTP_409_CONFLICT)


class BadRequestError(AppError):
    def __init__(self, message: str = "Bad request"):
        super().__init__(message, "BAD_REQUEST", status.HTTP_400_BAD_REQUEST)



def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "message": exc.message, "error_code": exc.error_code},
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError):
        # Pydantic v2 can include a raw exception object in an error's `ctx`
        # (e.g. when a field_validator raises ValueError) — that's not
        # JSON-serializable, so stringify it before it hits JSONResponse.
        sanitized_errors = []
        for error in exc.errors():
            error = dict(error)
            ctx = error.get("ctx")
            if isinstance(ctx, dict) and "error" in ctx:
                ctx = {**ctx, "error": str(ctx["error"])}
                error["ctx"] = ctx
            sanitized_errors.append(error)

        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "success": False,
                "message": "Invalid request data",
                "error_code": "VALIDATION_ERROR",
                "details": sanitized_errors,
            },
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "message": str(exc.detail), "error_code": "HTTP_ERROR"},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled server error")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"success": False, "message": "Internal server error", "error_code": "INTERNAL_ERROR"},
        )
