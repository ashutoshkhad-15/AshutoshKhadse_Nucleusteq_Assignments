"""Request schemas for interview feedback workflows."""

import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from src.enums.app_enums import Recommendation
from src.utils.validators import validate_required_text, normalize_string_list


FOCUS_AREA_PATTERN = re.compile(r"^(?=.*[A-Za-z])[A-Za-z0-9 .,&()/+\-]{2,100}$")


def _validate_focus_areas(values) -> list[str]:
    """Validate the list of interview focus tech areas."""
    normalized_values = normalize_string_list(values if isinstance(values, list) else str(values).split(","))
    if not normalized_values:
        raise ValueError("Tech Areas Covered is required")
    validated: list[str] = []
    for value in normalized_values:
        candidate = re.sub(r"\s+", " ", value).strip()
        if len(candidate) < 2 or len(candidate) > 100:
            raise ValueError("Tech Areas Covered must be between 2 and 100 characters")
        if not FOCUS_AREA_PATTERN.fullmatch(candidate):
            raise ValueError("Tech Areas Covered must contain alphabetic characters and may include common symbols")
        if candidate.lower() not in {item.lower() for item in validated}:
            validated.append(candidate)
    if not validated:
        raise ValueError("Tech Areas Covered is required")
    return validated


def _validate_rating(value, field_name: str) -> int:
    """Validate a feedback rating between 1 and 5."""
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"{field_name} must be an integer")
    if value < 1 or value > 5:
        raise ValueError(f"{field_name} must be between 1 and 5")
    return value


class FeedbackRequest(BaseModel):
    """Validate the payload used to submit interview feedback."""

    technical_rating: int = Field(..., alias="technicalRating")
    communication_rating: int = Field(..., alias="communicationRating")
    problem_solving: int = Field(..., alias="problemSolving")
    tech_areas_covered: list[str] = Field(..., alias="techAreasCovered")
    comments: Optional[str] = None
    recommendation: Recommendation

    @field_validator("technical_rating", "communication_rating", "problem_solving")
    @classmethod
    def validate_rating(cls, value: int, info) -> int:
        return _validate_rating(value, info.field_name.replace("_", " ").title())

    @field_validator("tech_areas_covered", mode="before")
    @classmethod
    def validate_areas(cls, value):
        return _validate_focus_areas(value)

    @field_validator("comments")
    @classmethod
    def validate_comments(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        return validate_required_text(value, "Comments")
