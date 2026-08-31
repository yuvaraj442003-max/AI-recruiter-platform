"""
File validation utilities for resume uploads.
"""
import re
import uuid

from app.core.exceptions import AppError

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


class FileValidationError(AppError):
    def __init__(self, message: str, error_code: str = "INVALID_FILE"):
        super().__init__(message, error_code, 400)


def validate_extension(filename: str) -> str:
    """Returns the lowercase extension if allowed, else raises."""
    if "." not in filename:
        raise FileValidationError("File has no extension.")
    ext = "." + filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise FileValidationError(
            f"Unsupported file type '{ext}'. Only PDF and DOCX resumes are accepted.",
            "UNSUPPORTED_FILE_TYPE",
        )
    return ext


def validate_size(file_size_bytes: int, max_mb: int) -> None:
    max_bytes = max_mb * 1024 * 1024
    if file_size_bytes > max_bytes:
        raise FileValidationError(f"File is too large. Maximum allowed size is {max_mb}MB.", "FILE_TOO_LARGE")
    if file_size_bytes == 0:
        raise FileValidationError("Uploaded file is empty.", "EMPTY_FILE")


_UNSAFE_CHARS_RE = re.compile(r"[^A-Za-z0-9._-]")


def secure_filename(original_filename: str) -> str:
    """
    Builds a safe, unique on-disk filename: strips any directory
    components and unsafe characters, and prefixes a UUID so two
    candidates uploading "resume.pdf" never collide or overwrite
    each other.
    """
    base = original_filename.replace("\\", "/").split("/")[-1]
    base = _UNSAFE_CHARS_RE.sub("_", base)
    if not base:
        base = "resume"
    return f"{uuid.uuid4().hex}_{base}"
