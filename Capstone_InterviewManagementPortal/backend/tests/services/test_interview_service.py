"""Service tests for interview scheduling workflows."""

from unittest.mock import AsyncMock, patch

import pytest

from src.enums.app_enums import UserRole
from src.exceptions.custom_exceptions import AppBaseException
from src.schemas.request.interview_request import InterviewCreateRequest, InterviewUpdateRequest
from src.services.interview_service import InterviewService


@pytest.fixture
def interview_service():
    with patch("src.services.interview_service.InterviewRepository") as mock_repo_class:
        mock_repo = mock_repo_class.return_value
        mock_repo.create_interview = AsyncMock()
        mock_repo.update_interview = AsyncMock()
        mock_repo.get_interview_by_id = AsyncMock()
        mock_repo.get_all_interviews = AsyncMock()
        mock_repo.find_overlapping_interview = AsyncMock()
        mock_repo.get_candidate_by_id = AsyncMock()
        mock_repo.get_job_by_id = AsyncMock()
        mock_repo.get_user_by_id = AsyncMock()
        service = InterviewService()
        service.interview_repo = mock_repo
        yield service


@pytest.mark.asyncio
class TestInterviewService:
    async def test_create_interview_success(self, interview_service):
        interview_service.interview_repo.get_candidate_by_id.return_value = {"_id": "cand1", "first_name": "Ashutosh", "last_name": "Khadse"}
        interview_service.interview_repo.get_job_by_id.return_value = {"_id": "job1", "jobTitle": "Backend Developer"}
        interview_service.interview_repo.get_user_by_id.return_value = {"_id": "usr1", "name": "Interviewer One", "role": UserRole.INTERVIEWER.value}
        interview_service.interview_repo.find_overlapping_interview.return_value = None
        interview_service.interview_repo.create_interview.return_value = {"_id": "int1"}

        request = InterviewCreateRequest(
            candidateId="cand1",
            jobId="job1",
            interviewDate="2099-01-01",
            interviewTime="10:30",
            interviewerId="usr1",
            focusTechAreas=["Python", "FastAPI"],
        )
        result = await interview_service.create_interview(request)
        assert result["_id"] == "int1"

    async def test_create_interview_rejects_past_date(self, interview_service):
        interview_service.interview_repo.get_candidate_by_id.return_value = {"_id": "cand1"}
        interview_service.interview_repo.get_job_by_id.return_value = {"_id": "job1"}
        interview_service.interview_repo.get_user_by_id.return_value = {"_id": "usr1", "role": UserRole.INTERVIEWER.value}
        interview_service.interview_repo.find_overlapping_interview.return_value = None

        request = InterviewCreateRequest(
            candidateId="cand1",
            jobId="job1",
            interviewDate="2000-01-01",
            interviewTime="10:30",
            interviewerId="usr1",
            focusTechAreas=["Python"],
        )
        with pytest.raises(AppBaseException) as excinfo:
            await interview_service.create_interview(request)
        assert excinfo.value.error_code == "INVALID_INTERVIEW_DATE"

    async def test_create_interview_requires_interviewer_role(self, interview_service):
        interview_service.interview_repo.get_candidate_by_id.return_value = {"_id": "cand1"}
        interview_service.interview_repo.get_job_by_id.return_value = {"_id": "job1"}
        interview_service.interview_repo.get_user_by_id.return_value = {"_id": "usr1", "role": UserRole.HR.value}
        request = InterviewCreateRequest(
            candidateId="cand1",
            jobId="job1",
            interviewDate="2099-01-01",
            interviewTime="10:30",
            interviewerId="usr1",
            focusTechAreas=["Python"],
        )
        with pytest.raises(AppBaseException) as excinfo:
            await interview_service.create_interview(request)
        assert excinfo.value.error_code == "INVALID_INTERVIEWER_ROLE"

    async def test_create_interview_conflict(self, interview_service):
        interview_service.interview_repo.get_candidate_by_id.return_value = {"_id": "cand1"}
        interview_service.interview_repo.get_job_by_id.return_value = {"_id": "job1"}
        interview_service.interview_repo.get_user_by_id.return_value = {"_id": "usr1", "role": UserRole.INTERVIEWER.value}
        interview_service.interview_repo.find_overlapping_interview.return_value = {"_id": "existing"}
        request = InterviewCreateRequest(
            candidateId="cand1",
            jobId="job1",
            interviewDate="2099-01-01",
            interviewTime="10:30",
            interviewerId="usr1",
            focusTechAreas=["Python"],
        )
        with pytest.raises(AppBaseException) as excinfo:
            await interview_service.create_interview(request)
        assert excinfo.value.error_code == "INTERVIEW_CONFLICT"

    async def test_get_interview_by_id_not_found(self, interview_service):
        interview_service.interview_repo.get_interview_by_id.return_value = None
        with pytest.raises(AppBaseException) as excinfo:
            await interview_service.get_interview_by_id("missing")
        assert excinfo.value.error_code == "INTERVIEW_NOT_FOUND"

    async def test_update_interview_success(self, interview_service):
        interview_service.interview_repo.get_interview_by_id.return_value = {
            "_id": "int1",
            "candidate_id": "cand1",
            "job_id": "job1",
            "interviewer_id": "usr1",
            "interview_date": __import__("datetime").date(2099, 1, 1),
            "interview_time": "10:30",
        }
        interview_service.interview_repo.find_overlapping_interview.return_value = None
        interview_service.interview_repo.update_interview.return_value = {"_id": "int1"}
        request = InterviewUpdateRequest(interviewTime="11:00")
        result = await interview_service.update_interview("int1", request)
        assert result["_id"] == "int1"
