from typing import Optional

from pydantic import BaseModel

from src.schemas.request.job_request import EmploymentType


class JobResponse(BaseModel):
    id: str
    jobTitle: str
    jobDetails: str
    jobRole: str
    requiredSkills: list[str]
    experienceRequired: str
    employmentType: EmploymentType
    location: str
    updated_at: Optional[str] = None
