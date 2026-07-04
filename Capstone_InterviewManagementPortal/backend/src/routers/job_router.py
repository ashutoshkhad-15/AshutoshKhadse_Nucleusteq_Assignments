"""Router layer for Job Description APIs.

This module implements job creation, listing, retrieval, and update routes.
Role-based access control: HR can create/update; HR, ADMIN, and INTERVIEWER can view.
"""

import logging

from fastapi import APIRouter, Depends, status, Query
from typing import Optional

from src.exceptions.custom_exceptions import AppBaseException
from src.schemas.request.job_request import CreateJobRequest, UpdateJobRequest
from src.schemas.response.common_response import SuccessResponse
from src.services.job_service import JobService
from src.utils.security import require_role, get_current_user
from src.enums.app_enums import UserRole

logger = logging.getLogger(__name__)

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
    try:
        data = await job_service.create_job(request)
    except Exception as exc:
        if not isinstance(exc, AppBaseException):
            logger.exception("Unexpected error while creating job through API")
        raise
    logger.info("Job created successfully through API")
    return SuccessResponse(message="Job created successfully", data=data)


@router.get("/", response_model=SuccessResponse[list], status_code=status.HTTP_200_OK)
async def get_all_jobs(
    search: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    job_service: JobService = Depends(get_job_service),
    _current_user: dict = Depends(require_role([UserRole.HR.value, UserRole.ADMIN.value, UserRole.INTERVIEWER.value]))
):
    """Retrieve all job descriptions.

    Accessible by HR, ADMIN, and INTERVIEWER roles.
    """
    try:
        result = await job_service.get_all_jobs(search=search, page=page, limit=limit)
        if isinstance(result, tuple) and len(result) == 2:
            data, meta = result
        else:
            data = result
            meta = {"page": page, "limit": limit, "total_items": len(data or []), "total_pages": 1}
    except Exception as exc:
        if not isinstance(exc, AppBaseException):
            logger.exception("Unexpected error while retrieving jobs through API")
        raise
    logger.info("Jobs retrieved successfully through API")
    return SuccessResponse(message="Jobs retrieved successfully", data=data, meta=meta)


@router.get("/{job_id}", response_model=SuccessResponse[dict], status_code=status.HTTP_200_OK)
async def get_job(
    job_id: str,
    job_service: JobService = Depends(get_job_service),
    _current_user: dict = Depends(require_role([UserRole.HR.value, UserRole.ADMIN.value, UserRole.INTERVIEWER.value]))
):
    """Retrieve a specific job description by ID.

    Accessible by HR, ADMIN, and INTERVIEWER roles.
    """
    try:
        data = await job_service.get_job_by_id(job_id)
    except Exception as exc:
        if not isinstance(exc, AppBaseException):
            logger.exception("Unexpected error while retrieving job %s through API", job_id)
        raise
    logger.info("Job retrieved successfully through API: %s", job_id)
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
    try:
        data = await job_service.update_job(job_id, request)
    except Exception as exc:
        if not isinstance(exc, AppBaseException):
            logger.exception("Unexpected error while updating job %s through API", job_id)
        raise
    logger.info("Job updated successfully through API: %s", job_id)
    return SuccessResponse(message="Job updated successfully", data=data)
