"""Router layer for Job Description APIs.

This module implements job creation, listing, retrieval, and update routes.
Role-based access control: HR can create/update; HR, ADMIN, and INTERVIEWER can view.
"""

from fastapi import APIRouter, Depends, status
from typing import Optional
from src.schemas.request.job_request import CreateJobRequest, UpdateJobRequest
from src.schemas.response.common_response import SuccessResponse
from src.services.job_service import JobService
from src.utils.security import require_role, get_current_user
from src.enums.app_enums import UserRole

router = APIRouter(prefix="/api/v1/jobs", tags=["Jobs"])


def get_job_service() -> JobService:
    """Resolve the JobService dependency for job routes."""
    return JobService()


@router.post("/", response_model=SuccessResponse[dict], status_code=status.HTTP_201_CREATED)
async def create_job(
    request: CreateJobRequest,
    job_service: JobService = Depends(get_job_service),
    _current_user: dict = Depends(require_role([UserRole.HR.value]))
):
    """Create a new job description.

    Requires HR permission to execute.
    """
    data = await job_service.create_job(request)
    return SuccessResponse(message="Job created successfully", data=data)


@router.get("/", response_model=SuccessResponse[list], status_code=status.HTTP_200_OK)
async def get_all_jobs(
    search: Optional[str] = None,
    status_filter: Optional[str] = None,
    job_service: JobService = Depends(get_job_service),
    _current_user: dict = Depends(require_role([UserRole.HR.value, UserRole.ADMIN.value, UserRole.INTERVIEWER.value]))
):
    """Retrieve all job descriptions.

    Accessible by HR, ADMIN, and INTERVIEWER roles.
    """
    is_active = None
    if status_filter == "ACTIVE":
        is_active = True
    elif status_filter == "INACTIVE":
        is_active = False

    data = await job_service.get_all_jobs(search=search, is_active=is_active)
    return SuccessResponse(message="Jobs retrieved successfully", data=data)


@router.get("/{job_id}", response_model=SuccessResponse[dict], status_code=status.HTTP_200_OK)
async def get_job(
    job_id: str,
    job_service: JobService = Depends(get_job_service),
    _current_user: dict = Depends(require_role([UserRole.HR.value, UserRole.ADMIN.value, UserRole.INTERVIEWER.value]))
):
    """Retrieve a specific job description by ID.

    Accessible by HR, ADMIN, and INTERVIEWER roles.
    """
    data = await job_service.get_job_by_id(job_id)
    return SuccessResponse(message="Job retrieved successfully", data=data)


@router.patch("/{job_id}", response_model=SuccessResponse[dict], status_code=status.HTTP_200_OK)
async def update_job(
    job_id: str,
    request: UpdateJobRequest,
    job_service: JobService = Depends(get_job_service),
    _current_user: dict = Depends(require_role([UserRole.HR.value]))
):
    """Update an existing job description.

    Requires HR permission.
    """
    data = await job_service.update_job(job_id, request)
    return SuccessResponse(message="Job updated successfully", data=data)
