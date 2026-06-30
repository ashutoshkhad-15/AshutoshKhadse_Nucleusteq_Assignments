"""Pydantic request schemas for Job Description APIs.

Defines the payloads accepted by the job creation and update endpoints.
These models apply the same validation rules used by the production API.
"""

from pydantic import BaseModel, Field
from typing import List, Optional


class CreateJobRequest(BaseModel):
    """Request body for creating a new job description.

    Attributes:
        title: Human-friendly job title.
        department: Owning department or team name.
        description: Full job description text; must be reasonably long.
        skills: Required technical skills list; at least one item.
        experience_required: Short experience expectation string.
        location: Location text (city/state or 'Remote').
    """

    title: str = Field(..., min_length=3, max_length=100, description="Job title, e.g., Senior Data Engineer")
    department: str = Field(..., min_length=2, max_length=50)
    description: str = Field(..., min_length=10)
    skills: List[str] = Field(..., min_length=1, description="List of required technical skills")
    experience_required: str = Field(..., description="e.g., 2-4 years")
    location: str = Field(..., description="e.g., Indore, MP or Remote")


class UpdateJobRequest(BaseModel):
    """Patch-style request for updating fields on an existing job.

    All fields are optional to support partial updates via `PATCH`.
    Use `is_active` to open or close a posting without changing other fields.
    """

    title: Optional[str] = None
    department: Optional[str] = None
    description: Optional[str] = None
    skills: Optional[List[str]] = None
    experience_required: Optional[str] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None  # Used to open/close a job posting