"""Request schemas for interview scheduling and feedback workflows."""

import re
from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from src.utils.validators import validate_required_text
from src.schemas.request.feedback_request import FeedbackRequest


TIME_PATTERN = re.compile(r"^(?:[01]?\d|2[0-3]):[0-5]\d$")


def _validate_time(value: str) -> str:
    """Validate a 24-hour time value."""
    normalized = validate_required_text(value, "Interview Time")
    if not TIME_PATTERN.fullmatch(normalized):
        raise ValueError("Interview Time must use HH:MM in 24-hour format")
    return normalized


class InterviewCreateRequest(BaseModel):
    """Validate the payload used to create an interview schedule."""

    candidate_id: str = Field(..., alias="candidateId")
    job_id: str = Field(..., alias="jobId")
    interview_date: date = Field(..., alias="interviewDate")
    interview_time: str = Field(..., alias="interviewTime")
    interviewer_id: str = Field(..., alias="interviewerId")
    focus_tech_areas: list[str] = Field(..., alias="focusTechAreas")

    @field_validator("candidate_id", "job_id", "interviewer_id")
    @classmethod
    def validate_required_ids(cls, value: str) -> str:
        return validate_required_text(value, "Identifier")

    @field_validator("interview_time")
    @classmethod
    def validate_time(cls, value: str) -> str:
        return _validate_time(value)

    @field_validator("focus_tech_areas", mode="before")
    @classmethod
    def validate_focus_areas(cls, value):
        from src.schemas.request.feedback_request import _validate_focus_areas

        return _validate_focus_areas(value)


class InterviewUpdateRequest(BaseModel):
    """Validate the payload used to update an interview schedule."""

    candidate_id: Optional[str] = Field(None, alias="candidateId")
    job_id: Optional[str] = Field(None, alias="jobId")
    interview_date: Optional[date] = Field(None, alias="interviewDate")
    interview_time: Optional[str] = Field(None, alias="interviewTime")
    interviewer_id: Optional[str] = Field(None, alias="interviewerId")
    focus_tech_areas: Optional[list[str]] = Field(None, alias="focusTechAreas")

    @field_validator("candidate_id", "job_id", "interviewer_id")
    @classmethod
    def validate_optional_ids(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return validate_required_text(value, "Identifier")

    @field_validator("interview_time")
    @classmethod
    def validate_time(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return _validate_time(value)

    @field_validator("focus_tech_areas", mode="before")
    @classmethod
    def validate_focus_areas(cls, value):
        if value is None:
            return value
        from src.schemas.request.feedback_request import _validate_focus_areas

        return _validate_focus_areas(value)
