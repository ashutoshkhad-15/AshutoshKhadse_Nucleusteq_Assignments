"""API routes for interview scheduling."""

import logging

from fastapi import APIRouter, Depends, Query, status

from src.enums.app_enums import UserRole
from src.schemas.request.interview_request import InterviewCreateRequest, InterviewUpdateRequest
from src.schemas.response.interview_response import InterviewResponse
from src.schemas.response.common_response import SuccessResponse
from src.services.interview_service import InterviewService
from src.utils.common import build_success_response, get_user_role
from src.utils.dependencies import get_interview_service
from src.utils.security import require_role

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/interviews", tags=["Interviews"])

@router.post("/", response_model=SuccessResponse[InterviewResponse], status_code=status.HTTP_201_CREATED)
async def create_interview(request: InterviewCreateRequest, interview_service: InterviewService = Depends(get_interview_service), _current_user: dict = Depends(require_role([UserRole.HR]))):
    """Create a new interview schedule."""
    logger.info("Interview creation request received")
    data = await interview_service.create_interview(request)
    logger.info("Interview creation request completed successfully")
    return build_success_response("Interview scheduled successfully", data)


@router.patch("/{interview_id}", response_model=SuccessResponse[InterviewResponse])
async def update_interview(interview_id: str, request: InterviewUpdateRequest, interview_service: InterviewService = Depends(get_interview_service), _current_user: dict = Depends(require_role([UserRole.HR]))):
    """Update an existing interview schedule."""
    logger.info("Interview update request received for interview: %s", interview_id)
    data = await interview_service.update_interview(interview_id, request)
    logger.info("Interview update request completed successfully for interview: %s", interview_id)
    return build_success_response("Interview updated successfully", data)


@router.get("/", response_model=SuccessResponse[list[InterviewResponse]])
async def get_interviews(search: str | None = None, page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100), interview_service: InterviewService = Depends(get_interview_service), current_user: dict = Depends(require_role([UserRole.HR, UserRole.ADMIN, UserRole.INTERVIEWER]))):
    """Return interviews with optional search and pagination."""
    logger.info("Interview list request received")
    if get_user_role(current_user) == UserRole.INTERVIEWER:
        interviewer_id = current_user.get("_id") or current_user.get("id")
        data, meta = await interview_service.get_assigned_interviews(interviewer_id, search=search, page=page, limit=limit)
    else:
        data, meta = await interview_service.get_all_interviews(search=search, page=page, limit=limit)
    logger.info("Interview list request completed successfully")
    return build_success_response("Interviews retrieved successfully", data, meta)


@router.get("/interviewers", response_model=SuccessResponse[list])
async def get_interviewers(search: str | None = None, page: int = Query(1, ge=1), limit: int = Query(100, ge=1, le=100), interview_service: InterviewService = Depends(get_interview_service), _current_user: dict = Depends(require_role([UserRole.HR, UserRole.ADMIN]))):
    """Return interviewer options for interview scheduling."""
    logger.info("Interviewer list request received")
    data, meta = await interview_service.get_interviewers(search=search, page=page, limit=limit)
    logger.info("Interviewer list request completed successfully")
    return build_success_response("Interviewers retrieved successfully", data, meta)


@router.get("/assigned", response_model=SuccessResponse[list[InterviewResponse]])
async def get_assigned_interviews(search: str | None = None, page: int = Query(1, ge=1), limit: int = Query(10, ge=1, le=100), interview_service: InterviewService = Depends(get_interview_service), current_user: dict = Depends(require_role([UserRole.INTERVIEWER]))):
    """Return interviews assigned to the logged-in interviewer."""
    logger.info("Assigned interview list request received")
    interviewer_id = current_user.get("_id") or current_user.get("id")
    data, meta = await interview_service.get_assigned_interviews(interviewer_id, search=search, page=page, limit=limit)
    logger.info("Assigned interview list request completed successfully")
    return build_success_response("Assigned interviews retrieved successfully", data, meta)


@router.get("/{interview_id}", response_model=SuccessResponse[InterviewResponse])
async def get_interview_by_id(interview_id: str, interview_service: InterviewService = Depends(get_interview_service), current_user: dict = Depends(require_role([UserRole.HR, UserRole.ADMIN, UserRole.INTERVIEWER]))):
    """Return a single interview."""
    logger.info("Interview lookup request received for interview: %s", interview_id)
    data = await interview_service.get_interview_for_user(interview_id, current_user)
    logger.info("Interview lookup request completed successfully for interview: %s", interview_id)
    return build_success_response("Interview retrieved successfully", data)
