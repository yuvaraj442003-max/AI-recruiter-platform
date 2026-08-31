"""
Consistent API response envelope used across all endpoints.
"""
from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None


class APIError(BaseModel):
    success: bool = False
    message: str
    error_code: str
    details: Optional[Any] = None
