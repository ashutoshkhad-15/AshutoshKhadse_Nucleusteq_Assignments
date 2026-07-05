"""Request schemas for user management endpoints."""

import re
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from src.constants.app_constants import AppConstants
from src.enums.app_enums import UserRole
from src.utils.validators import validate_nucleusteq_email, validate_required_text


NAME_PATTERN = re.compile(r"^[A-Za-z]+(?: [A-Za-z]+)*$")


def _validate_user_email(value: str) -> str:
    """Apply the shared corporate email rules with the expected error wording."""
    try:
        return validate_nucleusteq_email(value)
    except ValueError as exc:
        if not value.strip().lower().endswith(f"@{AppConstants.DOMAIN_NAME}"):
            raise ValueError(f"Email must belong to {AppConstants.DOMAIN_NAME} domain") from exc
        raise ValueError("Email must be a valid NucleusTeq address") from exc


class CreateUserRequest(BaseModel):
    """Validate the data required to create a new user account."""

    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    role: UserRole

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        normalized = validate_required_text(value, "Name")
        if len(normalized) < 2 or len(normalized) > 100:
            raise ValueError("Name must be between 2 and 100 characters")
        if not NAME_PATTERN.fullmatch(normalized):
            raise ValueError("Name must contain alphabets only")
        return normalized

    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, value: str) -> str:
        """Restrict account creation to the approved corporate email format."""
        return _validate_user_email(value)


class UpdateUserRequest(BaseModel):
    """Capture optional fields that can be updated for an existing user."""

    name: Optional[str] = Field(None, min_length=2, max_length=100)
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    email: Optional[str] = None

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        normalized = validate_required_text(value, "Name")
        if len(normalized) < 2 or len(normalized) > 100:
            raise ValueError("Name must be between 2 and 100 characters")
        if not NAME_PATTERN.fullmatch(normalized):
            raise ValueError("Name must contain alphabets only")
        return normalized

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return _validate_user_email(value)
