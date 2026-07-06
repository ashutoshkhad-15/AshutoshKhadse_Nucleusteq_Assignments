"""Service tests for candidate management workflows."""

from sys import exc_info
from unittest.mock import AsyncMock, patch

import pytest
from pydantic import ValidationError

from src.enums.app_enums import CandidateStatus
from src.exceptions.custom_exceptions import AppBaseException
from src.schemas.request.candidate_request import CandidateCreateRequest, CandidateUpdateRequest
from src.services.candidate_service import CandidateService


@pytest.fixture
def candidate_service():
    with patch("src.services.candidate_service.CandidateRepository") as mock_repo_class:
        mock_repo_instance = mock_repo_class.return_value
        mock_repo_instance.create_candidate = AsyncMock()
        mock_repo_instance.get_all_candidates = AsyncMock()
        mock_repo_instance.get_candidate_by_id = AsyncMock()
        mock_repo_instance.update_candidate = AsyncMock()
        mock_repo_instance.get_candidate_by_email = AsyncMock()
        mock_repo_instance.get_candidate_by_mobile = AsyncMock()
        mock_repo_instance.get_job_by_id = AsyncMock()
        mock_repo_instance.get_jobs_by_title = AsyncMock()
        mock_repo_instance.get_resume_file = AsyncMock()
        mock_repo_instance.upsert_resume = AsyncMock()
        mock_repo_instance.add_status_history = AsyncMock()
        mock_repo_instance.get_status_history = AsyncMock()
        service = CandidateService()
        service.candidate_repo = mock_repo_instance
        yield service


@pytest.mark.asyncio
class TestCandidateService:
    async def test_create_candidate_success(self, candidate_service):
        candidate_service.candidate_repo.get_candidate_by_email.return_value = None
        candidate_service.candidate_repo.get_candidate_by_mobile.return_value = None
        candidate_service.candidate_repo.get_job_by_id.return_value = {"_id": "job1"}
        candidate_service.candidate_repo.create_candidate.return_value = {"_id": "123"}

        request = CandidateCreateRequest(
            firstName="Ashutosh",
            lastName="Khadse",
            email="ashutosh.khadse@gmail.com",
            mobile="9876543210",
            currentCompany="NucleusTeq",
            totalExperience="2 years",
            appliedJobId="job1",
        )
        result = await candidate_service.create_candidate(request)

        assert result["_id"] == "123"

    async def test_create_candidate_requires_current_company(self, candidate_service):
        with pytest.raises(ValidationError):
            CandidateCreateRequest(
                firstName="Ashutosh",
                lastName="Khadse",
                email="ashutosh.khadse@gmail.com",
                mobile="9876543210",
                currentCompany="",
                totalExperience="2 years",
                appliedJobId="job1",
            )

    async def test_create_candidate_rejects_whitespace_current_company(self, candidate_service):
        with pytest.raises(ValidationError):
            CandidateCreateRequest(
                firstName="Ashutosh",
                lastName="Khadse",
                email="ashutosh.khadse@gmail.com",
                mobile="9876543210",
                currentCompany="   ",
                totalExperience="2 years",
                appliedJobId="job1",
            )

    async def test_create_candidate_accepts_valid_current_company(self, candidate_service):
        candidate_service.candidate_repo.get_candidate_by_email.return_value = None
        candidate_service.candidate_repo.get_candidate_by_mobile.return_value = None
        candidate_service.candidate_repo.get_job_by_id.return_value = {"_id": "job1"}
        candidate_service.candidate_repo.create_candidate.return_value = {"_id": "123"}

        request = CandidateCreateRequest(
            firstName="Ashutosh",
            lastName="Khadse",
            email="ashutosh.khadse@gmail.com",
            mobile="9876543210",
            currentCompany="NucleusTeq",
            totalExperience="2 years",
            appliedJobId="job1",
        )
        result = await candidate_service.create_candidate(request)
        assert result["_id"] == "123"

    async def test_create_candidate_duplicate_email(self, candidate_service):
        candidate_service.candidate_repo.get_candidate_by_email.return_value = {"_id": "1"}
        candidate_service.candidate_repo.get_job_by_id.return_value = {"_id": "job1"}

        request = CandidateCreateRequest(
            firstName="Ashutosh",
            lastName="Khadse",
            email="ashutosh.khadse@gmail.com",
            mobile="9876543210",
            currentCompany="NucleusTeq",
            totalExperience="2 years",
            appliedJobId="job1",
        )

        with pytest.raises(AppBaseException) as exc_info:
            await candidate_service.create_candidate(request)

        assert exc_info.value.error_code == "CANDIDATE_EMAIL_EXISTS"

    async def test_create_candidate_duplicate_mobile(self, candidate_service):
        candidate_service.candidate_repo.get_candidate_by_email.return_value = None
        candidate_service.candidate_repo.get_candidate_by_mobile.return_value = {"_id": "1"}
        candidate_service.candidate_repo.get_job_by_id.return_value = {"_id": "job1"}

        request = CandidateCreateRequest(
            firstName="Ashutosh",
            lastName="Khadse",
            email="ashutosh.khadse@gmail.com",
            mobile="9876543210",
            currentCompany="NucleusTeq",
            totalExperience="2 years",
            appliedJobId="job1",
        )

        with pytest.raises(AppBaseException) as exc_info:
            await candidate_service.create_candidate(request)

        assert exc_info.value.error_code == "CANDIDATE_MOBILE_EXISTS"

    async def test_create_candidate_invalid_job(self, candidate_service):
        candidate_service.candidate_repo.get_candidate_by_email.return_value = None
        candidate_service.candidate_repo.get_candidate_by_mobile.return_value = None
        candidate_service.candidate_repo.get_job_by_id.return_value = None
        request = CandidateCreateRequest(
            firstName="Ashutosh",
            lastName="Khadse",
            email="ashutosh.khadse@gmail.com",
            mobile="9876543210",
            currentCompany="NucleusTeq",
            totalExperience="2 years",
            appliedJobId="missing",
        )

        with pytest.raises(AppBaseException) as exc_info:
            await candidate_service.create_candidate(request)
        assert exc_info.value.error_code == "APPLIED_JOB_NOT_FOUND"

    async def test_get_all_candidates_with_search(self, candidate_service):
        candidate_service.candidate_repo.get_all_candidates.return_value = ([{"_id": "123"}], 1)
        candidate_service.candidate_repo.get_jobs_by_title.return_value = [{"_id": "job1", "jobTitle": "Backend Developer"}]
        result = await candidate_service.get_all_candidates(search="ashu")
        assert result[0] == [{"_id": "123"}]
        assert result[1]["total_items"] == 1
        candidate_service.candidate_repo.get_jobs_by_title.assert_awaited_once_with("ashu")

    async def test_upload_resume_success(self, candidate_service):
        candidate_service.candidate_repo.get_candidate_by_id.return_value = {
            "_id": "123",
            "status": CandidateStatus.PROFILE_CREATED.value,
        }
        candidate_service.candidate_repo.upsert_resume.return_value = {"candidate_id": "123"}

        class FileStub:
            filename = "resume.pdf"
            content_type = "application/pdf"

            async def read(self):
                return b"%PDF-1.4 test"

        result = await candidate_service.upload_resume("123", FileStub())
        assert result["candidate_id"] == "123"
        
    async def test_upload_resume_max_allowed_size(self, candidate_service):
        candidate_service.candidate_repo.get_candidate_by_id.return_value = {
            "_id": "123",
            "status": CandidateStatus.PROFILE_CREATED.value,
        }
        candidate_service.candidate_repo.upsert_resume.return_value = {
            "candidate_id": "123"
        }

        class FileStub:
            filename = "resume.pdf"
            content_type = "application/pdf"

            async def read(self):
                return b"a" * (5 * 1024 * 1024)

        result = await candidate_service.upload_resume("123", FileStub())
        assert result["candidate_id"] == "123"
        
    async def test_upload_resume_exceeds_max_size(self, candidate_service):
        candidate_service.candidate_repo.get_candidate_by_id.return_value = {
            "_id": "123",
            "status": CandidateStatus.PROFILE_CREATED.value,
        }
        
        class FileStub:
            filename = "resume.pdf"
            content_type = "application/pdf"

            async def read(self):
                return b"a" * (5 * 1024 * 1024 + 1)
            
        with pytest.raises(AppBaseException) as exc_info:
            await candidate_service.upload_resume("123", FileStub())
            
        assert exc_info.value.error_code == "RESUME_TOO_LARGE"
        assert exc_info.value.status_code == 400
        assert "5 MB" in exc_info.value.message

    async def test_upload_resume_invalid_extension(self, candidate_service):
        candidate_service.candidate_repo.get_candidate_by_id.return_value = {"_id": "123"}

        class FileStub:
            filename = "resume.docx"
            content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

            async def read(self):
                return b"bad"

        with pytest.raises(AppBaseException) as exc_info:
            await candidate_service.upload_resume("123", FileStub())
        assert exc_info.value.error_code == "INVALID_RESUME_TYPE"

    async def test_upload_resume_empty_file(self, candidate_service):
        candidate_service.candidate_repo.get_candidate_by_id.return_value = {"_id": "123"}

        class FileStub:
            filename = "resume.pdf"
            content_type = "application/pdf"

            async def read(self):
                return b""

        with pytest.raises(AppBaseException) as exc_info:
            await candidate_service.upload_resume("123", FileStub())
        assert exc_info.value.error_code == "EMPTY_RESUME_FILE"

    async def test_get_resume_not_found(self, candidate_service):
        candidate_service.candidate_repo.get_candidate_by_id.return_value = {"_id": "123"}
        candidate_service.candidate_repo.get_resume_file.return_value = None
        with pytest.raises(AppBaseException) as exc_info:
            await candidate_service.get_resume("123")
        assert exc_info.value.error_code == "RESUME_NOT_FOUND"

    async def test_update_candidate_status_success(self, candidate_service):
        candidate_service.candidate_repo.get_candidate_by_id.return_value = {
            "_id": "123",
            "status": CandidateStatus.PROFILE_CREATED.value,
        }
        candidate_service.candidate_repo.update_candidate.return_value = {"_id": "123", "status": CandidateStatus.INTERVIEW_SCHEDULED.value}
        candidate_service.candidate_repo.add_status_history.return_value = {"_id": "history1"}

        result = await candidate_service.update_candidate_status("123", CandidateStatus.INTERVIEW_SCHEDULED)
        assert result["status"] == CandidateStatus.INTERVIEW_SCHEDULED.value

    async def test_update_candidate_status_invalid_transition(self, candidate_service):
        candidate_service.candidate_repo.get_candidate_by_id.return_value = {
            "_id": "123",
            "status": CandidateStatus.SELECTED.value,
        }
        with pytest.raises(AppBaseException) as exc_info:
            await candidate_service.update_candidate_status("123", CandidateStatus.REJECTED)
        assert exc_info.value.error_code == "INVALID_STATUS_TRANSITION"

    async def test_status_history_retrieval(self, candidate_service):
        candidate_service.candidate_repo.get_candidate_by_id.return_value = {"_id": "123"}
        candidate_service.candidate_repo.get_status_history.return_value = [
            {"candidate_id": "123", "previous_status": CandidateStatus.PROFILE_CREATED.value, "new_status": CandidateStatus.INTERVIEW_SCHEDULED.value}
        ]
        history = await candidate_service.get_candidate_status_history("123")
        assert history[0]["new_status"] == CandidateStatus.INTERVIEW_SCHEDULED.value

    async def test_status_history_empty(self, candidate_service):
        candidate_service.candidate_repo.get_candidate_by_id.return_value = {"_id": "123"}
        candidate_service.candidate_repo.get_status_history.return_value = []
        history = await candidate_service.get_candidate_status_history("123")
        assert history == []

    async def test_update_candidate_status_invalid_status(self, candidate_service):
        candidate_service.candidate_repo.get_candidate_by_id.return_value = {
            "_id": "123",
            "status": CandidateStatus.PROFILE_CREATED.value,
        }
        with pytest.raises(AppBaseException) as exc_info:
            await candidate_service.update_candidate_status("123", "NOT_A_STATUS")
        assert exc_info.value.error_code == "INVALID_STATUS"

    async def test_get_candidate_by_id_not_found(self, candidate_service):
        candidate_service.candidate_repo.get_candidate_by_id.return_value = None
        with pytest.raises(AppBaseException):
            await candidate_service.get_candidate_by_id("missing-id")

    async def test_update_candidate_success(self, candidate_service):
        candidate_service.candidate_repo.get_candidate_by_id.return_value = {
            "_id": "123",
            "email": "ashutosh.khadse@gmail.com",
            "mobile": "9876543210",
        }
        candidate_service.candidate_repo.get_candidate_by_email.return_value = None
        candidate_service.candidate_repo.get_candidate_by_mobile.return_value = None
        candidate_service.candidate_repo.get_job_by_id.return_value = {"_id": "job1"}
        candidate_service.candidate_repo.update_candidate.return_value = {"_id": "123"}

        request = CandidateUpdateRequest(totalExperience="3+ years", appliedJobId="job1")
        result = await candidate_service.update_candidate("123", request)

        assert result["_id"] == "123"

    async def test_update_candidate_requires_current_company(self, candidate_service):
        candidate_service.candidate_repo.get_candidate_by_id.return_value = {
            "_id": "123",
            "email": "ashutosh.khadse@gmail.com",
            "mobile": "9876543210",
            "current_company": "NucleusTeq",
        }
        with pytest.raises(ValidationError):
            CandidateUpdateRequest(currentCompany="")

    async def test_update_candidate_rejects_whitespace_current_company(self, candidate_service):
        candidate_service.candidate_repo.get_candidate_by_id.return_value = {
            "_id": "123",
            "email": "ashutosh.khadse@gmail.com",
            "mobile": "9876543210",
            "current_company": "NucleusTeq",
        }
        with pytest.raises(ValidationError):
            CandidateUpdateRequest(currentCompany="   ")

    async def test_update_candidate_duplicate_email(self, candidate_service):
        candidate_service.candidate_repo.get_candidate_by_id.return_value = {
            "_id": "123",
            "email": "ashutosh.khadse@gmail.com",
            "mobile": "9876543210",
        }
        candidate_service.candidate_repo.get_candidate_by_email.return_value = {"_id": "999"}

        with pytest.raises(AppBaseException) as exc_info:
            await candidate_service.update_candidate("123", CandidateUpdateRequest(email="john123@gmail.com"))
        assert exc_info.value.error_code == "CANDIDATE_EMAIL_EXISTS"

    async def test_update_candidate_duplicate_mobile(self, candidate_service):
        candidate_service.candidate_repo.get_candidate_by_id.return_value = {
            "_id": "123",
            "email": "ashutosh.khadse@gmail.com",
            "mobile": "9876543210",
        }
        candidate_service.candidate_repo.get_candidate_by_mobile.return_value = {"_id": "999"}

        with pytest.raises(AppBaseException) as exc_info:
            await candidate_service.update_candidate("123", CandidateUpdateRequest(mobile="9999999999"))
        assert exc_info.value.error_code == "CANDIDATE_MOBILE_EXISTS"

    async def test_update_candidate_empty_payload(self, candidate_service):
        candidate_service.candidate_repo.get_candidate_by_id.return_value = {
            "_id": "123",
            "email": "ashutosh.khadse@gmail.com",
            "mobile": "9876543210",
        }
        with pytest.raises(AppBaseException) as exc_info:
            await candidate_service.update_candidate("123", CandidateUpdateRequest())
        assert exc_info.value.error_code == "INVALID_UPDATE"
