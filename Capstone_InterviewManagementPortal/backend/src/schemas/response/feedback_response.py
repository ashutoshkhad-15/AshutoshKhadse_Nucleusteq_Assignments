"""Feedback response DTOs."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class FeedbackDetailsResponse(BaseModel):
    """Embedded feedback payload returned by feedback endpoints."""

    technical_rating: int
    communication_rating: int
    problem_solving: int
    tech_areas_covered: list[str]
    comments: Optional[str] = None
    recommendation: str


class FeedbackResponse(BaseModel):
    """Feedback response model used by feedback endpoints."""

    id: str = Field(alias="_id")
    feedback: FeedbackDetailsResponse
    feedback_by: Optional[str] = None
    feedback_submitted_at: Optional[datetime] = None
