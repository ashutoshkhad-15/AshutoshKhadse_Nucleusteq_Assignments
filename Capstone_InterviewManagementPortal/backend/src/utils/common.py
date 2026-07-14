"""Shared helpers for request normalization, roles, and API responses."""

from __future__ import annotations

from typing import Iterable

from src.enums.app_enums import UserRole
from src.schemas.response.common_response import SuccessResponse


def normalize_search_term(search: str | None) -> str:
    """Return a trimmed search term or an empty string."""
    return (search or "").strip()


def build_pagination_meta(page: int, limit: int, total_items: int) -> dict:
    """Build canonical pagination metadata."""
    total_pages = max(1, (total_items + limit - 1) // limit)
    return {"page": page, "limit": limit, "total_items": total_items, "total_pages": total_pages}


def build_success_response(message: str, data=None, meta: dict | None = None) -> SuccessResponse:
    """Create the shared success envelope."""
    return SuccessResponse(message=message, data=data, meta=meta)


def get_user_role(current_user: dict | None) -> UserRole | None:
    """Convert a raw stored role to the canonical enum when possible."""
    if not current_user:
        return None
    role = current_user.get("role")
    if isinstance(role, UserRole):
        return role
    if isinstance(role, str):
        try:
            return UserRole(role)
        except ValueError:
            return None
    return None


def has_role(current_user: dict | None, allowed_roles: Iterable[UserRole]) -> bool:
    """Check whether a user has one of the allowed enum roles."""
    role = get_user_role(current_user)
    return role in set(allowed_roles)
