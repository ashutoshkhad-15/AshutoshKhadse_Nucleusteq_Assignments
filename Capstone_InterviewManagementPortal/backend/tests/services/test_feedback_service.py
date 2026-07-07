"""Service tests for interview feedback workflows."""

from unittest.mock import AsyncMock, patch

import pytest
from pydantic import ValidationError

from src.enums.app_enums import Recommendation, UserRole, CandidateStatus
from src.exceptions.custom_exceptions import AppBaseException
from src.schemas.request.feedback_request import FeedbackRequest
from src.services.feedback_service import FeedbackService


@pytest.fixture
def feedback_service():
    with patch("src.services.feedback_service.FeedbackRepository") as mock_repo_class, \
         patch("src.services.feedback_service.InterviewService") as mock_interview_class, \
         patch("src.services.feedback_service.CandidateService") as mock_candidate_class:
        repo = mock_repo_class.return_value
        repo.feedback_exists = AsyncMock()
        repo.submit_feedback = AsyncMock()
        repo.get_feedback_by_interview_id = AsyncMock()

        interview_service = mock_interview_class.return_value
        interview_service.get_interview_by_id = AsyncMock()

        candidate_service = mock_candidate_class.return_value
        candidate_service.update_candidate_status = AsyncMock()

        service = FeedbackService()
        service.feedback_repo = repo
        service.interview_service = interview_service
        service.candidate_service = candidate_service
        yield service


@pytest.mark.asyncio
class TestFeedbackService:
    async def test_submit_feedback_success(self, feedback_service):
        feedback_service.interview_service.get_interview_by_id.return_value = {"_id": "int1", "interviewer_id": "usr1", "candidate_id": "cand1"}
        feedback_service.feedback_repo.feedback_exists.return_value = False
        feedback_service.feedback_repo.submit_feedback.return_value = {"_id": "int1", "feedback": {"recommendation": "SELECT"}}
        feedback_service.candidate_service.update_candidate_status.return_value = {"_id": "cand1"}
        request = FeedbackRequest(technicalRating=5, communicationRating=4, problemSolving=5, techAreasCovered=["Python"], comments="Good", recommendation=Recommendation.SELECT)
        result = await feedback_service.submit_feedback("int1", request, {"_id": "usr1", "role": UserRole.INTERVIEWER.value})
        assert result["_id"] == "int1"

    async def test_submit_feedback_duplicate(self, feedback_service):
        feedback_service.interview_service.get_interview_by_id.return_value = {"_id": "int1", "interviewer_id": "usr1"}
        feedback_service.feedback_repo.feedback_exists.return_value = True
        request = FeedbackRequest(technicalRating=5, communicationRating=4, problemSolving=5, techAreasCovered=["Python"], comments="Good", recommendation=Recommendation.SELECT)
        with pytest.raises(AppBaseException) as excinfo:
            await feedback_service.submit_feedback("int1", request, {"_id": "usr1", "role": UserRole.INTERVIEWER.value})
        assert excinfo.value.error_code == "FEEDBACK_EXISTS"

    async def test_submit_feedback_wrong_user(self, feedback_service):
        feedback_service.interview_service.get_interview_by_id.return_value = {"_id": "int1", "interviewer_id": "usr1"}
        request = FeedbackRequest(technicalRating=5, communicationRating=4, problemSolving=5, techAreasCovered=["Python"], comments="Good", recommendation=Recommendation.SELECT)
        with pytest.raises(AppBaseException) as excinfo:
            await feedback_service.submit_feedback("int1", request, {"_id": "usr2", "role": UserRole.INTERVIEWER.value})
        assert excinfo.value.status_code == 403

    async def test_view_feedback_not_found(self, feedback_service):
        feedback_service.feedback_repo.get_feedback_by_interview_id.return_value = None
        with pytest.raises(AppBaseException):
            await feedback_service.view_feedback("missing")

    async def test_feedback_rating_validation(self):
        with pytest.raises(ValidationError):
            FeedbackRequest(technicalRating=0, communicationRating=4, problemSolving=5, techAreasCovered=["Python"], comments="Good", recommendation=Recommendation.SELECT)
