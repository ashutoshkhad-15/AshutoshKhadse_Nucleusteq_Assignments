"""Candidate response DTOs."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from src.enums.app_enums import CandidateStatus


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


class ResumeMetadataResponse(BaseModel):
    """Metadata returned for a candidate resume document."""

    candidate_id: str
    original_filename: str
    stored_filename: str
    content_type: str
    uploaded_at: datetime
    uploaded_by: Optional[str] = None


class CandidateStatusHistoryResponse(BaseModel):
    """Immutable audit row for candidate status changes."""

    candidate_id: str
    previous_status: Optional[CandidateStatus] = None
    new_status: CandidateStatus
    timestamp: datetime
    updated_by: Optional[str] = None
