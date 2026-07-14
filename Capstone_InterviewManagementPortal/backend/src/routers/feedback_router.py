"""API routes for interview feedback management."""

import logging

from fastapi import APIRouter, Depends

from src.enums.app_enums import UserRole
from src.schemas.request.feedback_request import FeedbackRequest
from src.schemas.response.feedback_response import FeedbackResponse
from src.schemas.response.common_response import SuccessResponse
from src.services.feedback_service import FeedbackService
from src.utils.common import build_success_response
from src.utils.dependencies import get_feedback_service
from src.utils.security import require_role

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/interviews", tags=["Feedback"])

@router.post("/{interview_id}/feedback", response_model=SuccessResponse[FeedbackResponse])
async def submit_feedback(interview_id: str, request: FeedbackRequest, feedback_service: FeedbackService = Depends(get_feedback_service), current_user: dict = Depends(require_role([UserRole.INTERVIEWER]))):
    """Submit feedback for an assigned interview."""
    logger.info("Feedback submission request received for interview: %s", interview_id)
    data = await feedback_service.submit_feedback(interview_id, request, current_user)
    logger.info("Feedback submission request completed successfully for interview: %s", interview_id)
    return build_success_response("Feedback submitted successfully", data)


@router.get("/{interview_id}/feedback", response_model=SuccessResponse[FeedbackResponse | None])
async def view_feedback(interview_id: str, feedback_service: FeedbackService = Depends(get_feedback_service), current_user: dict = Depends(require_role([UserRole.HR, UserRole.ADMIN, UserRole.INTERVIEWER]))):
    """View feedback for an interview."""
    logger.info("Feedback view request received for interview: %s", interview_id)
    data = await feedback_service.view_feedback(interview_id, current_user)
    logger.info("Feedback view request completed successfully for interview: %s", interview_id)
    return build_success_response("Feedback retrieved successfully", data)
