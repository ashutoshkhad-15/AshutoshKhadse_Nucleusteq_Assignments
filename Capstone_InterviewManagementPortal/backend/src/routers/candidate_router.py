"""Router layer for candidate management APIs."""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, status

from src.enums.app_enums import UserRole
from src.schemas.request.candidate_request import (
    CandidateCreateRequest,
    CandidateUpdateRequest,
)
from src.schemas.response.common_response import SuccessResponse
from src.services.candidate_service import CandidateService
from src.utils.security import require_role

router = APIRouter(prefix="/api/v1/candidates", tags=["Candidates"])
logger = logging.getLogger(__name__)


def get_candidate_service() -> CandidateService:
    """Resolve the candidate service dependency for candidate routes.

    Returns:
        CandidateService: Service instance used by the route handlers.
    """
    return CandidateService()


@router.post("/", response_model=SuccessResponse[dict], status_code=status.HTTP_201_CREATED)
async def create_candidate(
    request: CandidateCreateRequest,
    candidate_service: CandidateService = Depends(get_candidate_service),
    _current_user: dict = Depends(require_role([UserRole.HR.value])),
):
    """Create a new candidate profile.

    Args:
        request: Validated candidate create payload.
        candidate_service: Candidate service dependency.

    Returns:
        SuccessResponse[dict]: Standard success response with candidate data.
    """
    logger.info("Candidate creation request received")
    data = await candidate_service.create_candidate(request)
    logger.info("Candidate created successfully via router")
    return SuccessResponse(message="Candidate created successfully", data=data)


@router.get("/", response_model=SuccessResponse[list], status_code=status.HTTP_200_OK)
async def get_all_candidates(
    search: Optional[str] = None,
    candidate_service: CandidateService = Depends(get_candidate_service),
    _current_user: dict = Depends(
        require_role([UserRole.HR.value, UserRole.ADMIN.value, UserRole.INTERVIEWER.value])
    ),
):
    """Retrieve all candidates with optional search filtering.

    Args:
        search: Optional case-insensitive search term.
        candidate_service: Candidate service dependency.

    Returns:
        SuccessResponse[list]: Standard success response with candidate data.
    """
    logger.info("Candidate list request received")
    data = await candidate_service.get_all_candidates(search=search)
    logger.info("Candidates retrieved successfully via router")
    return SuccessResponse(message="Candidates retrieved successfully", data=data)


@router.get("/{candidate_id}", response_model=SuccessResponse[dict], status_code=status.HTTP_200_OK)
async def get_candidate(
    candidate_id: str,
    candidate_service: CandidateService = Depends(get_candidate_service),
    _current_user: dict = Depends(
        require_role([UserRole.HR.value, UserRole.ADMIN.value, UserRole.INTERVIEWER.value])
    ),
):
    """Retrieve a candidate profile by identifier.

    Args:
        candidate_id: Candidate ObjectId string.
        candidate_service: Candidate service dependency.

    Returns:
        SuccessResponse[dict]: Standard success response with candidate data.
    """
    logger.info("Candidate lookup request received")
    data = await candidate_service.get_candidate_by_id(candidate_id)
    logger.info("Candidate retrieved successfully via router")
    return SuccessResponse(message="Candidate retrieved successfully", data=data)


@router.patch("/{candidate_id}", response_model=SuccessResponse[dict], status_code=status.HTTP_200_OK)
async def update_candidate(
    candidate_id: str,
    request: CandidateUpdateRequest,
    candidate_service: CandidateService = Depends(get_candidate_service),
    _current_user: dict = Depends(require_role([UserRole.HR.value])),
):
    """Update a candidate profile.

    Args:
        candidate_id: Candidate ObjectId string.
        request: Validated candidate update payload.
        candidate_service: Candidate service dependency.

    Returns:
        SuccessResponse[dict]: Standard success response with updated candidate data.
    """
    logger.info("Candidate update request received")
    data = await candidate_service.update_candidate(candidate_id, request)
    logger.info("Candidate updated successfully via router")
    return SuccessResponse(message="Candidate updated successfully", data=data)
