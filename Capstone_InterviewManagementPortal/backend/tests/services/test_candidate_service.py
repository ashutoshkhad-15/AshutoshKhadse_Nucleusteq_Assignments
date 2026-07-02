"""Service tests for candidate management workflows."""

from unittest.mock import AsyncMock, patch

import pytest

from src.enums.app_enums import CandidateStatus
from src.exceptions.custom_exceptions import AppBaseException
from src.schemas.request.candidate_request import (
    CandidateCreateRequest,
    CandidateUpdateRequest,
)
from src.services.candidate_service import CandidateService


@pytest.fixture
def candidate_service():
    """Provide a candidate service backed by a mocked repository."""
    with patch("src.services.candidate_service.CandidateRepository") as mock_repo_class:
        mock_repo_instance = mock_repo_class.return_value
        mock_repo_instance.create_candidate = AsyncMock()
        mock_repo_instance.get_all_candidates = AsyncMock()
        mock_repo_instance.get_candidate_by_id = AsyncMock()
        mock_repo_instance.update_candidate = AsyncMock()
        mock_repo_instance.get_candidate_by_email = AsyncMock()
        mock_repo_instance.get_candidate_by_mobile = AsyncMock()

        service = CandidateService()
        service.candidate_repo = mock_repo_instance
        yield service


@pytest.mark.asyncio
class TestCandidateService:
    async def test_create_candidate_success(self, candidate_service):
        """Create a candidate when email and mobile are unique."""
        candidate_service.candidate_repo.get_candidate_by_email.return_value = None
        candidate_service.candidate_repo.get_candidate_by_mobile.return_value = None
        candidate_service.candidate_repo.create_candidate.return_value = {
            "_id": "123",
            "name": "Ashutosh Khadse",
            "email": "ashutosh.khadse@nucleusteq.com",
            "mobile": "9876543210",
            "status": "PROFILE_CREATED",
        }

        request = CandidateCreateRequest(
            name="Ashutosh Khadse",
            email="ashutosh.khadse@nucleusteq.com",
            mobile="9876543210",
        )
        result = await candidate_service.create_candidate(request)

        assert result["_id"] == "123"
        assert result["status"] == "PROFILE_CREATED"
        candidate_service.candidate_repo.create_candidate.assert_called_once()

    async def test_create_candidate_duplicate_email(self, candidate_service):
        """Reject candidate creation when the email already exists."""
        candidate_service.candidate_repo.get_candidate_by_email.return_value = {"_id": "1"}

        request = CandidateCreateRequest(
            name="Ashutosh Khadse",
            email="ashutosh.khadse@nucleusteq.com",
            mobile="9876543210",
        )

        with pytest.raises(AppBaseException) as exc_info:
            await candidate_service.create_candidate(request)

        assert exc_info.value.error_code == "CANDIDATE_EMAIL_EXISTS"

    async def test_create_candidate_duplicate_mobile(self, candidate_service):
        """Reject candidate creation when the mobile number already exists."""
        candidate_service.candidate_repo.get_candidate_by_email.return_value = None
        candidate_service.candidate_repo.get_candidate_by_mobile.return_value = {"_id": "1"}

        request = CandidateCreateRequest(
            name="Ashutosh Khadse",
            email="ashutosh.khadse@nucleusteq.com",
            mobile="9876543210",
        )

        with pytest.raises(AppBaseException) as exc_info:
            await candidate_service.create_candidate(request)

        assert exc_info.value.error_code == "CANDIDATE_MOBILE_EXISTS"

    async def test_get_all_candidates_with_search(self, candidate_service):
        """Delegate candidate search to the repository layer."""
        candidate_service.candidate_repo.get_all_candidates.return_value = [{"_id": "123"}]

        result = await candidate_service.get_all_candidates(search="ashu")

        assert result == [{"_id": "123"}]
        candidate_service.candidate_repo.get_all_candidates.assert_called_once_with(search="ashu")

    async def test_get_candidate_by_id_not_found(self, candidate_service):
        """Raise a not-found error for unknown candidate identifiers."""
        candidate_service.candidate_repo.get_candidate_by_id.return_value = None

        with pytest.raises(AppBaseException) as exc_info:
            await candidate_service.get_candidate_by_id("missing-id")

        assert exc_info.value.error_code == "CANDIDATE_NOT_FOUND"

    async def test_update_candidate_success(self, candidate_service):
        """Update a candidate when unique fields remain valid."""
        candidate_service.candidate_repo.get_candidate_by_id.side_effect = [
            {
                "_id": "123",
                "name": "Ashutosh Khadse",
                "email": "ashutosh.khadse@nucleusteq.com",
                "mobile": "9876543210",
                "status": "PROFILE_CREATED",
            }
        ]
        candidate_service.candidate_repo.get_candidate_by_email.return_value = None
        candidate_service.candidate_repo.get_candidate_by_mobile.return_value = None
        candidate_service.candidate_repo.update_candidate.return_value = {
            "_id": "123",
            "name": "Ashu Khadse",
            "email": "ashutosh.khadse@nucleusteq.com",
            "mobile": "9876543210",
            "status": "INTERVIEW_SCHEDULED",
        }

        request = CandidateUpdateRequest(
            name="Ashu Khadse",
            status=CandidateStatus.INTERVIEW_SCHEDULED,
        )
        result = await candidate_service.update_candidate("123", request)

        assert result["status"] == "INTERVIEW_SCHEDULED"
        candidate_service.candidate_repo.update_candidate.assert_called_once_with(
            "123",
            {"name": "Ashu Khadse", "status": "INTERVIEW_SCHEDULED"},
        )

    async def test_update_candidate_duplicate_email(self, candidate_service):
        """Reject candidate updates when the new email belongs to another record."""
        candidate_service.candidate_repo.get_candidate_by_id.return_value = {
            "_id": "123",
            "name": "Ashutosh Khadse",
            "email": "ashutosh.khadse@nucleusteq.com",
            "mobile": "9876543210",
            "status": "PROFILE_CREATED",
        }
        candidate_service.candidate_repo.get_candidate_by_email.return_value = {"_id": "999"}

        request = CandidateUpdateRequest(email="john123@nucleusteq.com")

        with pytest.raises(AppBaseException) as exc_info:
            await candidate_service.update_candidate("123", request)

        assert exc_info.value.error_code == "CANDIDATE_EMAIL_EXISTS"

    async def test_update_candidate_duplicate_mobile(self, candidate_service):
        """Reject candidate updates when the new mobile belongs to another record."""
        candidate_service.candidate_repo.get_candidate_by_id.return_value = {
            "_id": "123",
            "name": "Ashutosh Khadse",
            "email": "ashutosh.khadse@nucleusteq.com",
            "mobile": "9876543210",
            "status": "PROFILE_CREATED",
        }
        candidate_service.candidate_repo.get_candidate_by_mobile.return_value = {"_id": "999"}

        request = CandidateUpdateRequest(mobile="9999999999")

        with pytest.raises(AppBaseException) as exc_info:
            await candidate_service.update_candidate("123", request)

        assert exc_info.value.error_code == "CANDIDATE_MOBILE_EXISTS"

    async def test_update_candidate_empty_payload(self, candidate_service):
        """Reject candidate update requests with no mutable fields."""
        candidate_service.candidate_repo.get_candidate_by_id.return_value = {
            "_id": "123",
            "name": "Ashutosh Khadse",
            "email": "ashutosh.khadse@nucleusteq.com",
            "mobile": "9876543210",
            "status": "PROFILE_CREATED",
        }

        with pytest.raises(AppBaseException) as exc_info:
            await candidate_service.update_candidate("123", CandidateUpdateRequest())

        assert exc_info.value.error_code == "INVALID_UPDATE"
