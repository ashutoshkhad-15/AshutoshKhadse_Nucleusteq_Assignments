"""Request schemas for candidate management endpoints."""

from typing import Optional

from pydantic import BaseModel, Field, field_validator

from src.enums.app_enums import CandidateStatus
from src.utils.validators import validate_mobile_number, validate_nucleusteq_email


class CandidateCreateRequest(BaseModel):
    """Validate the payload required to create a candidate profile.

    Args:
        name: Candidate full name.
        email: Candidate company email address.
        mobile: Candidate unique mobile number.
        status: Candidate workflow status.
    """

    name: str = Field(..., min_length=2, max_length=100)
    email: str
    mobile: str
    status: CandidateStatus = CandidateStatus.PROFILE_CREATED

    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        """Normalize and validate the candidate name."""
        normalized_name = value.strip()
        if not normalized_name:
            raise ValueError("Candidate name is required")
        return normalized_name

    @field_validator("email")
    def validate_email(cls, value: str) -> str:
        """Validate the candidate email address."""
        return validate_nucleusteq_email(value)

    @field_validator("mobile")
    def validate_mobile(cls, value: str) -> str:
        """Validate the candidate mobile number."""
        return validate_mobile_number(value)


class CandidateUpdateRequest(BaseModel):
    """Validate the payload used to partially update a candidate profile.

    Args:
        name: Updated candidate full name.
        email: Updated candidate email address.
        mobile: Updated candidate mobile number.
        status: Updated candidate workflow status.
    """

    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[str] = None
    mobile: Optional[str] = None
    status: Optional[CandidateStatus] = None

    @field_validator("name")
    def validate_name(cls, value: Optional[str]) -> Optional[str]:
        """Normalize the candidate name when present."""
        if value is None:
            return value
        normalized_name = value.strip()
        if not normalized_name:
            raise ValueError("Candidate name is required")
        return normalized_name

    @field_validator("email")
    def validate_email(cls, value: Optional[str]) -> Optional[str]:
        """Validate the candidate email address when present."""
        if value is None:
            return value
        return validate_nucleusteq_email(value)

    @field_validator("mobile")
    def validate_mobile(cls, value: Optional[str]) -> Optional[str]:
        """Validate the candidate mobile number when present."""
        if value is None:
            return value
        return validate_mobile_number(value)
