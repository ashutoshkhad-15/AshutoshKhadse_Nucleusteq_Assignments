"""Request schemas for job description endpoints."""

from enum import Enum
from typing import Optional
import re

from pydantic import BaseModel, Field, field_validator

from src.utils.validators import normalize_required_text, normalize_string_list


class EmploymentType(str, Enum):
    """Supported employment types for job descriptions."""

    FULL_TIME = "Full Time"
    INTERNSHIP = "Internship"


def _validate_experience_required(value: str) -> str:
    """Validate the canonical job experience string format."""
    if not isinstance(value, str):
        raise ValueError("Experience Required must be a string.")

    normalized = value.strip()
    if not normalized:
        raise ValueError("Experience Required is required.")

    if not re.fullmatch(r"^(?:\d{1,2}\s+year|\d{1,2}\s+years|\d{1,2}\+\s+years|\d{1,2}-\d{1,2}\s+years)$", normalized):
        raise ValueError('Experience Required must use formats like "0 year", "1 year", "2 years", "3+ years", or "5-7 years".')

    return normalized


class CreateJobRequest(BaseModel):
    """Validate the payload used to create a new job description."""

    jobTitle: str = Field(..., min_length=3, max_length=120)
    jobDetails: str = Field(..., min_length=10, max_length=4000)
    jobRole: str = Field(..., min_length=2, max_length=80)
    requiredSkills: list[str] = Field(..., min_length=1)
    experienceRequired: str = Field(...)
    employmentType: EmploymentType
    location: str = Field(..., min_length=2, max_length=120)

    @field_validator("jobTitle")
    @classmethod
    def validate_job_title(cls, value: str) -> str:
        return normalize_required_text(value, "Job Title", 3, 120)

    @field_validator("jobDetails")
    @classmethod
    def validate_job_details(cls, value: str) -> str:
        return normalize_required_text(value, "Job Details", 10, 4000)

    @field_validator("jobRole")
    @classmethod
    def validate_job_role(cls, value: str) -> str:
        return normalize_required_text(value, "Job Role", 2, 80)

    @field_validator("location")
    @classmethod
    def validate_location(cls, value: str) -> str:
        return normalize_required_text(value, "Location", 2, 120)

    @field_validator("requiredSkills", mode="before")
    @classmethod
    def normalize_skills(cls, value):
        """Normalize skill chips by trimming and removing duplicates."""
        skills = normalize_string_list(value)
        if not skills:
            raise ValueError("At least one required skill is needed.")
        return skills

    @field_validator("experienceRequired", mode="before")
    @classmethod
    def validate_experience_required(cls, value):
        return _validate_experience_required(value)


class UpdateJobRequest(BaseModel):
    """Validate the payload used to update an existing job description."""

    jobTitle: Optional[str] = Field(None, min_length=3, max_length=120)
    jobDetails: Optional[str] = Field(None, min_length=10, max_length=4000)
    jobRole: Optional[str] = Field(None, min_length=2, max_length=80)
    requiredSkills: Optional[list[str]] = None
    experienceRequired: Optional[str] = None
    employmentType: Optional[EmploymentType] = None
    location: Optional[str] = Field(None, min_length=2, max_length=120)
    @field_validator("jobTitle", "jobDetails", "jobRole", "location", mode="before")
    @classmethod
    def trim_optional_text(cls, value):
        if value is None:
            return value
        if not isinstance(value, str):
            raise ValueError("Field must be a string.")
        normalized = value.strip()
        if not normalized:
            raise ValueError("Field cannot be empty.")
        return normalized

    @field_validator("requiredSkills", mode="before")
    @classmethod
    def normalize_optional_skills(cls, value):
        if value is None:
            return value
        skills = normalize_string_list(value)
        if not skills:
            raise ValueError("At least one required skill is needed.")
        return skills

    @field_validator("experienceRequired", mode="before")
    @classmethod
    def validate_optional_experience_required(cls, value):
        if value is None:
            return value
        return _validate_experience_required(value)
