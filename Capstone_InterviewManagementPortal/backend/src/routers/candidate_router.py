"""Router layer for candidate management APIs."""

import logging
from typing import Optional

from fastapi import APIRouter, Depends, File, Query, UploadFile, status

from src.enums.app_enums import CandidateStatus, UserRole
from src.schemas.request.candidate_request import CandidateCreateRequest, CandidateUpdateRequest
from src.schemas.response.common_response import SuccessResponse
from src.services.candidate_service import CandidateService
from src.utils.common import build_success_response
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
    _current_user: dict = Depends(require_role([UserRole.HR])),
):
    """Create a new candidate profile."""
    logger.info("Candidate creation request received")
    data = await candidate_service.create_candidate(request)
    return build_success_response("Candidate created successfully", data)


@router.get("/", response_model=SuccessResponse[list], status_code=status.HTTP_200_OK)
async def get_all_candidates(
    search: Optional[str] = Query(default=None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    candidate_service: CandidateService = Depends(get_candidate_service),
    _current_user: dict = Depends(require_role([UserRole.HR, UserRole.ADMIN, UserRole.INTERVIEWER])),
):
    """Retrieve candidates with optional search filtering and pagination."""
    logger.info("Candidate list request received")
    data, meta = await candidate_service.get_all_candidates(search=search, page=page, limit=limit)
    return build_success_response("Candidates retrieved successfully", data, meta)


@router.get("/{candidate_id}", response_model=SuccessResponse[dict], status_code=status.HTTP_200_OK)
async def get_candidate(
    candidate_id: str,
    candidate_service: CandidateService = Depends(get_candidate_service),
    _current_user: dict = Depends(require_role([UserRole.HR, UserRole.ADMIN, UserRole.INTERVIEWER])),
):
    """Retrieve a candidate profile by identifier."""
    logger.info("Candidate lookup request received")
    data = await candidate_service.get_candidate_by_id(candidate_id)
    return build_success_response("Candidate retrieved successfully", data)


@router.patch("/{candidate_id}", response_model=SuccessResponse[dict], status_code=status.HTTP_200_OK)
async def update_candidate(
    candidate_id: str,
    request: CandidateUpdateRequest,
    candidate_service: CandidateService = Depends(get_candidate_service),
    _current_user: dict = Depends(require_role([UserRole.HR])),
):
    """Update a candidate profile."""
    logger.info("Candidate update request received")
    data = await candidate_service.update_candidate(candidate_id, request)
    return build_success_response("Candidate updated successfully", data)


@router.get("/jobs/search", response_model=SuccessResponse[list], status_code=status.HTTP_200_OK)
async def search_jobs_for_candidates(
    search: Optional[str] = Query(default=None),
    candidate_service: CandidateService = Depends(get_candidate_service),
    _current_user: dict = Depends(require_role([UserRole.HR, UserRole.ADMIN, UserRole.INTERVIEWER])),
):
    """Return searchable job options for the applied-job selector."""
    logger.info("Candidate job search request received")
    data = await candidate_service.get_jobs_for_dropdown(search)
    return build_success_response("Jobs retrieved successfully", data)


@router.post("/{candidate_id}/resume", response_model=SuccessResponse[dict], status_code=status.HTTP_201_CREATED)
async def upload_resume(
    candidate_id: str,
    resume_file: UploadFile = File(...),
    candidate_service: CandidateService = Depends(get_candidate_service),
    current_user: dict = Depends(require_role([UserRole.HR])),
):
    """Upload a candidate resume and store it separately from the profile."""
    logger.info("Candidate resume upload request received")
    data = await candidate_service.upload_resume(candidate_id, resume_file, uploaded_by=current_user.get("_id") or current_user.get("id"))
    return build_success_response("Resume uploaded successfully", data)


@router.get("/{candidate_id}/resume", response_model=SuccessResponse[dict], status_code=status.HTTP_200_OK)
async def get_resume(
    candidate_id: str,
    candidate_service: CandidateService = Depends(get_candidate_service),
    _current_user: dict = Depends(require_role([UserRole.HR, UserRole.ADMIN, UserRole.INTERVIEWER])),
):
    """Return stored resume metadata and binary payload for a candidate."""
    logger.info("Candidate resume view request received")
    data = await candidate_service.get_resume(candidate_id)
    return build_success_response("Resume retrieved successfully", data)


@router.patch("/{candidate_id}/status", response_model=SuccessResponse[dict], status_code=status.HTTP_200_OK)
async def update_candidate_status(
    candidate_id: str,
    status: CandidateStatus,
    candidate_service: CandidateService = Depends(get_candidate_service),
    current_user: dict = Depends(require_role([UserRole.HR])),
):
    """Update a candidate status and record the transition history."""
    logger.info("Candidate status update request received")
    data = await candidate_service.update_candidate_status(candidate_id, status, updated_by=current_user.get("_id") or current_user.get("id"))
    return build_success_response("Candidate status updated successfully", data)


@router.get("/{candidate_id}/status-history", response_model=SuccessResponse[list], status_code=status.HTTP_200_OK)
async def get_candidate_status_history(
    candidate_id: str,
    candidate_service: CandidateService = Depends(get_candidate_service),
    _current_user: dict = Depends(require_role([UserRole.HR, UserRole.ADMIN, UserRole.INTERVIEWER])),
):
    """Return the complete candidate status audit trail."""
    logger.info("Candidate status history request received")
    data = await candidate_service.get_candidate_status_history(candidate_id)
    return build_success_response("Candidate status history retrieved successfully", data)
