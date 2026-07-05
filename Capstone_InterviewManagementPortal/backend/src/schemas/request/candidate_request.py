"""Request schemas for candidate management endpoints."""

import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from src.utils.validators import (
    validate_mobile_number,
    validate_required_text,
)


EMAIL_PATTERN = re.compile(r"^(?!\.)(?!.*\.\.)[A-Za-z0-9]+(?:\.[A-Za-z0-9]+)*@(gmail\.com|outlook\.com|yahoo\.com)$", re.IGNORECASE)
NAME_PATTERN = re.compile(r"^(?=.*[A-Za-z])[A-Za-z]+(?: [A-Za-z]+)*$")
TOTAL_EXPERIENCE_PATTERN = re.compile(
    r"^(?:\d+ year|\d+ years|\d+\+ years|\d+-\d+ years)$"
)
COMPANY_PATTERN = re.compile(r"^(?=.*[A-Za-z])[A-Za-z0-9][A-Za-z0-9\s&().,'/-]*[A-Za-z0-9]$")


def _normalize_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _validate_name(value: str, field_name: str, min_length: int = 2, max_length: int = 50) -> str:
    """Validate a candidate name field."""
    normalized = _normalize_whitespace(validate_required_text(value, field_name))
    if len(normalized) < min_length or len(normalized) > max_length:
        raise ValueError(f"{field_name} must be between {min_length} and {max_length} characters")
    if normalized.replace(" ", "").isdigit():
        raise ValueError(f"{field_name} cannot contain only numbers")
    if not NAME_PATTERN.fullmatch(normalized):
        raise ValueError(f"{field_name} can contain alphabetic characters and single spaces only")
    return normalized


def _validate_email(value: str) -> str:
    """Validate the candidate email format and allowed domains."""
    normalized = validate_required_text(value, "Email Address").strip().lower()
    if not EMAIL_PATTERN.fullmatch(normalized):
        raise ValueError("Email Address must be a valid gmail.com, outlook.com, or yahoo.com address using only letters, numbers, and single dots")
    return normalized


def _validate_current_company(value: str) -> str:
    """Validate the required company field."""
    normalized = _normalize_whitespace(validate_required_text(value, "Current Company"))
    if not normalized:
        raise ValueError("Current Company is required.")
    if len(normalized) > 120:
        raise ValueError("Current Company must be at most 120 characters")
    if not re.search(r"[A-Za-z]", normalized):
        raise ValueError("Current Company is required.")
    if normalized.isdigit():
        raise ValueError("Current Company is required.")
    if not COMPANY_PATTERN.fullmatch(normalized):
        raise ValueError("Current Company must contain alphabetic characters and may include spaces, numbers, and common punctuation")
    return normalized


def _validate_total_experience(value: str) -> str:
    """Validate the canonical candidate experience string format."""
    if not isinstance(value, str):
        raise ValueError("Total Experience must be a string")

    normalized = value.strip()
    if not normalized:
        raise ValueError("Total Experience is required")

    if not TOTAL_EXPERIENCE_PATTERN.fullmatch(normalized):
        raise ValueError('Total Experience must use formats like "0 year", "1 year", "2 years", "3+ years", or "5-7 years"')
    return normalized


def _validate_applied_job_id(value: str) -> str:
    """Validate the applied job identifier."""
    normalized = validate_required_text(value, "Applied Job")
    if len(normalized) < 1:
        raise ValueError("Applied Job is required")
    return normalized


class CandidateCreateRequest(BaseModel):
    """Validate the payload required to create a candidate profile."""

    first_name: str = Field(..., min_length=2, max_length=50, alias="firstName")
    last_name: str = Field(..., min_length=2, max_length=50, alias="lastName")
    email: str
    mobile: str
    current_company: str = Field(..., max_length=120, alias="currentCompany")
    total_experience: str = Field(..., alias="totalExperience")
    applied_job_id: str = Field(..., alias="appliedJobId")

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name(cls, value: str, info) -> str:
        return _validate_name(value, info.field_name.replace("_", " ").title())

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        return _validate_email(value)

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, value: str) -> str:
        return validate_mobile_number(value)

    @field_validator("current_company")
    @classmethod
    def validate_current_company(cls, value: str) -> str:
        return _validate_current_company(value)

    @field_validator("total_experience", mode="before")
    @classmethod
    def validate_total_experience(cls, value):
        return _validate_total_experience(value)

    @field_validator("applied_job_id")
    @classmethod
    def validate_applied_job_id(cls, value: str) -> str:
        return _validate_applied_job_id(value)


class CandidateUpdateRequest(BaseModel):
    """Validate the payload used to partially update a candidate profile."""

    first_name: Optional[str] = Field(None, min_length=2, max_length=50, alias="firstName")
    last_name: Optional[str] = Field(None, min_length=2, max_length=50, alias="lastName")
    email: Optional[str] = None
    mobile: Optional[str] = None
    current_company: Optional[str] = Field(None, min_length=1, max_length=120, alias="currentCompany")
    total_experience: Optional[str] = Field(None, alias="totalExperience")
    applied_job_id: Optional[str] = Field(None, alias="appliedJobId")

    @field_validator("first_name", "last_name")
    @classmethod
    def validate_name(cls, value: Optional[str], info) -> Optional[str]:
        if value is None:
            return value
        return _validate_name(value, info.field_name.replace("_", " ").title())

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return _validate_email(value)

    @field_validator("mobile")
    @classmethod
    def validate_mobile(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return validate_mobile_number(value)

    @field_validator("current_company")
    @classmethod
    def validate_current_company(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return _validate_current_company(value)

    @field_validator("total_experience", mode="before")
    @classmethod
    def validate_total_experience(cls, value):
        if value is None:
            return value
        return _validate_total_experience(value)

    @field_validator("applied_job_id")
    @classmethod
    def validate_applied_job_id(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return _validate_applied_job_id(value)
