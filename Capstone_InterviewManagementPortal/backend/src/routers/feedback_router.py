"""API routes for interview feedback management."""

import logging

from fastapi import APIRouter, Depends

from src.enums.app_enums import UserRole
from src.schemas.request.feedback_request import FeedbackRequest
from src.schemas.response.feedback_response import FeedbackResponse
from src.schemas.response.common_response import SuccessResponse
from src.services.feedback_service import FeedbackService
from src.utils.security import require_role

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/interviews", tags=["Feedback"])


def get_feedback_service() -> FeedbackService:
    """Resolve the feedback service dependency for feedback routes."""
    return FeedbackService()


@router.post("/{interview_id}/feedback", response_model=SuccessResponse[FeedbackResponse])
async def submit_feedback(interview_id: str, request: FeedbackRequest, feedback_service: FeedbackService = Depends(get_feedback_service), current_user: dict = Depends(require_role([UserRole.INTERVIEWER.value]))):
    """Submit feedback for an assigned interview."""
    logger.info("Feedback submission request received for interview: %s", interview_id)
    data = await feedback_service.submit_feedback(interview_id, request, current_user)
    logger.info("Feedback submission request completed successfully for interview: %s", interview_id)
    return SuccessResponse(message="Feedback submitted successfully", data=data)


@router.get("/{interview_id}/feedback", response_model=SuccessResponse[FeedbackResponse])
async def view_feedback(interview_id: str, feedback_service: FeedbackService = Depends(get_feedback_service), _current_user: dict = Depends(require_role([UserRole.HR.value, UserRole.ADMIN.value, UserRole.INTERVIEWER.value]))):
    """View feedback for an interview."""
    logger.info("Feedback view request received for interview: %s", interview_id)
    data = await feedback_service.view_feedback(interview_id)
    logger.info("Feedback view request completed successfully for interview: %s", interview_id)
    return SuccessResponse(message="Feedback retrieved successfully", data=data)
