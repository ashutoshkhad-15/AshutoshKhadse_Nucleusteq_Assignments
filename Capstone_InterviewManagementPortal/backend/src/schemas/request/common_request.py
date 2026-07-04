"""Shared request schemas for pagination and list filtering."""

from pydantic import BaseModel, Field

from src.constants.app_constants import AppConstants


class PaginationQuery(BaseModel):
    """Validate common pagination query parameters."""

    page: int = Field(default=AppConstants.PAGINATION_DEFAULT_PAGE, ge=1, le=100000)
    limit: int = Field(default=AppConstants.PAGINATION_DEFAULT_LIMIT, ge=1, le=100)
