"""Shared API response schemas."""

from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import Generic, TypeVar, Optional, Any

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    """Standard success response envelope.

    Attributes:
        success: Indicates that the request completed successfully.
        message: Human-readable response message.
        data: Optional typed payload returned by the endpoint.
        meta: Optional pagination or response metadata.
    """

    success: bool = True
    message: str
    data: Optional[T] = None
    meta: Optional[dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Standard error response envelope.

    Attributes:
        success: Indicates that the request failed.
        error_code: Stable machine-readable error code.
        message: Human-readable error message.
        details: Optional structured error details, such as validation errors.
    """

    success: bool = False
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: int
    error_code: str
    message: str
    details: Optional[Any] = None


class PaginationMeta(BaseModel):
    """Metadata describing a paginated list response."""

    page: int
    limit: int
    total_items: int
    total_pages: int
