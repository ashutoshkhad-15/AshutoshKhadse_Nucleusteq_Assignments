"""Interview response DTOs."""

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class InterviewResponse(BaseModel):
    """Interview response model used by scheduling endpoints."""

    id: str = Field(alias="_id")
    candidate_id: str
    candidate_name: str
    job_id: str
    job_title: str
    interviewer_id: str
    interviewer_name: str
    interview_date: date
    interview_time: str
    focus_tech_areas: list[str]
    status: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
