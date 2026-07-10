"""Service layer for interview feedback workflows."""

import logging

from src.enums.app_enums import CandidateStatus, UserRole
from src.exceptions.custom_exceptions import AppBaseException
from src.repositories.feedback_repository import FeedbackRepository
from src.schemas.request.interview_request import FeedbackRequest
from src.services.candidate_service import CandidateService
from src.services.interview_service import InterviewService
from src.utils.common import get_user_role

logger = logging.getLogger(__name__)


class FeedbackService:
    """Coordinate interview feedback business rules and persistence."""

    def __init__(self):
        """Initialize the service with repository and service dependencies."""
        self.feedback_repo = FeedbackRepository()
        self.interview_service = InterviewService()
        self.candidate_service = CandidateService()

    async def submit_feedback(self, interview_id: str, request: FeedbackRequest, current_user: dict) -> dict:
        """Submit interview feedback for the assigned interviewer."""
        interview = await self.interview_service.get_interview_by_id(interview_id)
        if str(interview.get("interviewer_id")) != str(current_user.get("_id") or current_user.get("id")):
            raise AppBaseException("Only the assigned interviewer can submit feedback", "FORBIDDEN", 403)
        if interview.get("status") != CandidateStatus.INTERVIEW_COMPLETED.value:
            raise AppBaseException("Feedback can only be submitted after the interview is completed", "INVALID_INTERVIEW_STATUS", 400)
        if await self.feedback_repo.feedback_exists(interview_id):
            raise AppBaseException("Feedback already exists for this interview", "FEEDBACK_EXISTS", 400)

        feedback = request.model_dump(by_alias=False)
        payload = {
            "feedback": {
                "technical_rating": feedback["technical_rating"],
                "communication_rating": feedback["communication_rating"],
                "problem_solving": feedback["problem_solving"],
                "tech_areas_covered": feedback["tech_areas_covered"],
                "comments": feedback.get("comments"),
                "recommendation": feedback["recommendation"].value,
            },
            "feedback_by": current_user.get("_id") or current_user.get("id"),
        }
        result = await self.feedback_repo.submit_feedback(interview_id, payload)
        if not result:
            raise AppBaseException("Feedback not found", "FEEDBACK_NOT_FOUND", 404)
        await self._apply_post_feedback_status(interview, result["feedback"]["recommendation"], current_user)
        logger.info("Feedback submitted successfully: %s", interview_id)
        return result

    async def view_feedback(self, interview_id: str, current_user: dict) -> dict:
        """Return submitted feedback for an interview, or null when absent."""
        if get_user_role(current_user) == UserRole.INTERVIEWER:
            await self.interview_service.get_interview_for_interviewer(
                interview_id,
                str(current_user.get("_id") or current_user.get("id") or ""),
            )
        interview = await self.feedback_repo.get_feedback_by_interview_id(interview_id)
        if not interview or not interview.get("feedback"):
            return None
        return interview

    async def _apply_post_feedback_status(self, interview: dict, recommendation: str, current_user: dict) -> None:
        """Update interview and candidate status after feedback submission."""
        candidate_id = interview["candidate_id"]
        if recommendation == "SELECT":
            await self.candidate_service.update_candidate_status(
                candidate_id,
                CandidateStatus.SELECTED.value,
                updated_by=current_user.get("_id") or current_user.get("id"),
            )
        elif recommendation == "REJECT":
            await self.candidate_service.update_candidate_status(
                candidate_id,
                CandidateStatus.REJECTED.value,
                updated_by=current_user.get("_id") or current_user.get("id"),
            )
