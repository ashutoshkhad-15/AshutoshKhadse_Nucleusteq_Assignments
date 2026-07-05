"""Candidate response DTOs."""

from typing import Optional

from pydantic import BaseModel


class AppliedJobSummary(BaseModel):
    """Minimal applied-job payload returned alongside candidate data."""

    _id: str
    job_title: str


class CandidateResponse(BaseModel):
    """Candidate response model used by list and detail endpoints."""

    _id: str
    first_name: str
    last_name: str
    email: str
    mobile: str
    current_company: Optional[str] = None
    total_experience: str
    applied_job_id: str
    applied_job: Optional[AppliedJobSummary] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
