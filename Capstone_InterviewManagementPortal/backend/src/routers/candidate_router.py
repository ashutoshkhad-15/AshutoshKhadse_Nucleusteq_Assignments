"""Router layer for candidate management APIs."""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, Query, status

from src.enums.app_enums import UserRole
from src.schemas.request.candidate_request import CandidateCreateRequest, CandidateUpdateRequest
from src.schemas.response.common_response import SuccessResponse
from src.services.candidate_service import CandidateService
from src.utils.security import require_role

router = APIRouter(prefix="/api/v1/candidates", tags=["Candidates"])
logger = logging.getLogger(__name__)


def get_candidate_service() -> CandidateService:
    """Resolve the candidate service dependency for candidate routes."""
    return CandidateService()


@router.post("/", response_model=SuccessResponse[dict], status_code=status.HTTP_201_CREATED)
async def create_candidate(
    request: CandidateCreateRequest,
    candidate_service: CandidateService = Depends(get_candidate_service),
    _current_user: dict = Depends(require_role([UserRole.HR.value])),
):
    """Create a new candidate profile."""
    logger.info("Candidate creation request received")
    data = await candidate_service.create_candidate(request)
    return SuccessResponse(message="Candidate created successfully", data=data)


@router.get("/", response_model=SuccessResponse[list], status_code=status.HTTP_200_OK)
async def get_all_candidates(
    search: Optional[str] = Query(default=None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    candidate_service: CandidateService = Depends(get_candidate_service),
    _current_user: dict = Depends(require_role([UserRole.HR.value, UserRole.ADMIN.value, UserRole.INTERVIEWER.value])),
):
    """Retrieve candidates with optional search filtering and pagination."""
    logger.info("Candidate list request received")
    data, meta = await candidate_service.get_all_candidates(search=search, page=page, limit=limit)
    return SuccessResponse(message="Candidates retrieved successfully", data=data, meta=meta)


@router.get("/{candidate_id}", response_model=SuccessResponse[dict], status_code=status.HTTP_200_OK)
async def get_candidate(
    candidate_id: str,
    candidate_service: CandidateService = Depends(get_candidate_service),
    _current_user: dict = Depends(require_role([UserRole.HR.value, UserRole.ADMIN.value, UserRole.INTERVIEWER.value])),
):
    """Retrieve a candidate profile by identifier."""
    logger.info("Candidate lookup request received")
    data = await candidate_service.get_candidate_by_id(candidate_id)
    return SuccessResponse(message="Candidate retrieved successfully", data=data)


@router.patch("/{candidate_id}", response_model=SuccessResponse[dict], status_code=status.HTTP_200_OK)
async def update_candidate(
    candidate_id: str,
    request: CandidateUpdateRequest,
    candidate_service: CandidateService = Depends(get_candidate_service),
    _current_user: dict = Depends(require_role([UserRole.HR.value])),
):
    """Update a candidate profile."""
    logger.info("Candidate update request received")
    data = await candidate_service.update_candidate(candidate_id, request)
    return SuccessResponse(message="Candidate updated successfully", data=data)


@router.get("/jobs/search", response_model=SuccessResponse[list], status_code=status.HTTP_200_OK)
async def search_jobs_for_candidates(
    search: Optional[str] = Query(default=None),
    candidate_service: CandidateService = Depends(get_candidate_service),
    _current_user: dict = Depends(require_role([UserRole.HR.value, UserRole.ADMIN.value, UserRole.INTERVIEWER.value])),
):
    """Return searchable job options for the applied-job selector."""
    logger.info("Candidate job search request received")
    data = await candidate_service.get_jobs_for_dropdown(search)
    return SuccessResponse(message="Jobs retrieved successfully", data=data)
