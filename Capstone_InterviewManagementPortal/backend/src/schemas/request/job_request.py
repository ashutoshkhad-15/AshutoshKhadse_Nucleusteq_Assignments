"""Request schemas for job description endpoints."""

import re
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from src.utils.validators import (
    normalize_required_text,
    normalize_skill_text,
    normalize_string_list,
    normalize_text_with_pattern,
)


class EmploymentType(str, Enum):
    """Supported employment types for job descriptions."""

    FULL_TIME = "Full Time"
    INTERNSHIP = "Internship"


JOB_TITLE_PATTERN = re.compile(r"^(?=.*[A-Za-z])[A-Za-z0-9&()/+\- ]{3,100}$")
JOB_ROLE_PATTERN = re.compile(r"^(?=.*[A-Za-z])[A-Za-z0-9 ]{2,60}$")
JOB_DETAILS_PATTERN = re.compile(r"^.{20,1000}$", re.DOTALL)
LOCATION_PATTERN = re.compile(r"^(?=.*[A-Za-z])[A-Za-z0-9.,'()\- ]{2,80}$")
EXPERIENCE_PATTERN = re.compile(r"^(?:\d+ month|\d+ months|\d+ year|\d+ years|\d+ year \d+ month|\d+ years \d+ months|\d+ years \d+ month|\d+ year \d+ months|\d+\+ years|\d+-\d+ years)$")


def _validate_experience_required(value: str) -> str:
    """Validate the canonical job experience string format."""
    if not isinstance(value, str):
        raise ValueError("Experience Required must be a string.")

    normalized = value.strip()
    if not normalized:
        raise ValueError("Experience Required is required.")

    if not EXPERIENCE_PATTERN.fullmatch(normalized):
        raise ValueError("Experience Required must be in one of these formats: '3 months', '1 year', '3 years', '3 year 6 months', '3+ years', or '3-5 years'")

    return normalized


def _validate_skill(value: str) -> str:
    return normalize_skill_text(value)


class CreateJobRequest(BaseModel):
    """Validate the payload used to create a new job description."""

    jobTitle: str = Field(..., min_length=3, max_length=100)
    jobDetails: str = Field(..., min_length=20, max_length=1000)
    jobRole: str = Field(..., min_length=2, max_length=60)
    requiredSkills: list[str] = Field(..., min_length=1)
    experienceRequired: str = Field(...)
    employmentType: EmploymentType
    location: str = Field(..., min_length=2, max_length=80)

    @field_validator("jobTitle")
    @classmethod
    def validate_job_title(cls, value: str) -> str:
        return normalize_text_with_pattern(
            value,
            "Job Title",
            3,
            100,
            JOB_TITLE_PATTERN,
            'Job Title must contain at least one letter and may include numbers, spaces, and symbols like - / & ( ) +.',
        )

    @field_validator("jobDetails")
    @classmethod
    def validate_job_details(cls, value: str) -> str:
        normalized = normalize_required_text(value, "Job Details", 20, 1000)
        normalized = re.sub(r"\s+", " ", normalized).strip()
        return normalized

    @field_validator("jobRole")
    @classmethod
    def validate_job_role(cls, value: str) -> str:
        normalized = normalize_text_with_pattern(
            value,
            "Job Role",
            2,
            60,
            JOB_ROLE_PATTERN,
            "Job Role must contain letters and can include digits and spaces only.",
        )
        if normalized.isdigit():
            raise ValueError("Job Role cannot contain digits only")
        return normalized

    @field_validator("location")
    @classmethod
    def validate_location(cls, value: str) -> str:
        normalized = normalize_text_with_pattern(
            value,
            "Location",
            2,
            80,
            LOCATION_PATTERN,
            "Location must contain at least one alphabetic character and may include commas, periods, hyphens, apostrophes, parentheses, and spaces.",
        )
        if normalized.isdigit():
            raise ValueError("Location cannot contain digits only")
        return normalized

    @field_validator("requiredSkills", mode="before")
    @classmethod
    def normalize_skills(cls, value):
        """Normalize skill chips by trimming, deduplicating, and validating."""
        raw_values = value if isinstance(value, list) else str(value).split(",")
        skills = []
        for item in raw_values or []:
            if not isinstance(item, str):
                continue
            normalized = re.sub(r"\s+", " ", item.strip())
            if not normalized:
                continue
            validated = _validate_skill(normalized)
            if validated.lower() not in {skill.lower() for skill in skills}:
                skills.append(validated)
        if not skills:
            raise ValueError("At least one required skill is needed.")
        if len(skills) > 20:
            raise ValueError("A maximum of 20 skills is allowed.")
        return skills

    @field_validator("experienceRequired", mode="before")
    @classmethod
    def validate_experience_required(cls, value):
        return _validate_experience_required(value)


class UpdateJobRequest(BaseModel):
    """Validate the payload used to update an existing job description."""

    jobTitle: Optional[str] = Field(None, min_length=3, max_length=100)
    jobDetails: Optional[str] = Field(None, min_length=20, max_length=1000)
    jobRole: Optional[str] = Field(None, min_length=2, max_length=60)
    requiredSkills: Optional[list[str]] = None
    experienceRequired: Optional[str] = None
    employmentType: Optional[EmploymentType] = None
    location: Optional[str] = Field(None, min_length=2, max_length=80)

    @field_validator("jobTitle")
    @classmethod
    def validate_job_title(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return normalize_text_with_pattern(
            value,
            "Job Title",
            3,
            100,
            JOB_TITLE_PATTERN,
            'Job Title must contain at least one letter and may include numbers, spaces, and symbols like - / & ( ) +.',
        )

    @field_validator("jobDetails")
    @classmethod
    def validate_job_details(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        normalized = normalize_required_text(value, "Job Details", 20, 1000)
        return re.sub(r"\s+", " ", normalized).strip()

    @field_validator("jobRole")
    @classmethod
    def validate_job_role(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        normalized = normalize_text_with_pattern(
            value,
            "Job Role",
            2,
            60,
            JOB_ROLE_PATTERN,
            "Job Role must contain letters and can include digits and spaces only.",
        )
        if normalized.isdigit():
            raise ValueError("Job Role cannot contain digits only")
        return normalized

    @field_validator("location")
    @classmethod
    def validate_location(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        normalized = normalize_text_with_pattern(
            value,
            "Location",
            2,
            80,
            LOCATION_PATTERN,
            "Location must contain at least one alphabetic character and may include commas, periods, hyphens, apostrophes, parentheses, and spaces.",
        )
        if normalized.isdigit():
            raise ValueError("Location cannot contain digits only")
        return normalized

    @field_validator("requiredSkills", mode="before")
    @classmethod
    def normalize_optional_skills(cls, value):
        if value is None:
            return value
        raw_values = value if isinstance(value, list) else str(value).split(",")
        skills = []
        for item in raw_values or []:
            if not isinstance(item, str):
                continue
            normalized = re.sub(r"\s+", " ", item.strip())
            if not normalized:
                continue
            validated = _validate_skill(normalized)
            if validated.lower() not in {skill.lower() for skill in skills}:
                skills.append(validated)
        if len(skills) > 20:
            raise ValueError("A maximum of 20 skills is allowed.")
        if not skills:
            raise ValueError("At least one required skill is needed.")
        return skills

    @field_validator("experienceRequired", mode="before")
    @classmethod
    def validate_optional_experience_required(cls, value):
        if value is None:
            return value
        return _validate_experience_required(value)
