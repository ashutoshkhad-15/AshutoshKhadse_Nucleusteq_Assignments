"""Request schemas for user management endpoints."""

from typing import Optional

from pydantic import BaseModel, EmailStr, field_validator

from src.constants.app_constants import AppConstants
from src.enums.app_enums import UserRole
from src.utils.validators import validate_nucleusteq_email


class CreateUserRequest(BaseModel):
    """Validate the data required to create a new user account."""

    email: EmailStr
    role: UserRole

    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, v):
        """Restrict account creation to the approved corporate email format."""
        try:
            return validate_nucleusteq_email(v)
        except ValueError as exc:
            if not str(v).lower().endswith(f"@{AppConstants.DOMAIN_NAME}"):
                raise ValueError(f"Email must belong to {AppConstants.DOMAIN_NAME} domain") from exc
            raise ValueError("Email must be a valid NucleusTeq address") from exc

class UpdateUserRequest(BaseModel):
    """Capture optional fields that can be updated for an existing user."""

    role: Optional[UserRole] = None
    is_active: Optional[bool] = None
    email: Optional[str] = None
