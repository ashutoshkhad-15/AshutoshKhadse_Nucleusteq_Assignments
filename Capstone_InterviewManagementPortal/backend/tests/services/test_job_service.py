"""Service tests for the Job Description workflow."""

import pytest
from unittest.mock import AsyncMock, patch

from src.exceptions.custom_exceptions import AppBaseException
from src.schemas.request.job_request import CreateJobRequest, UpdateJobRequest
from src.services.job_service import JobService


@pytest.fixture
def job_service():
    """Provide a job service backed by mocked repository methods."""
    with patch("src.services.job_service.JobRepository") as mock_repo_class:
        mock_repo_instance = mock_repo_class.return_value
        mock_repo_instance.create_job = AsyncMock()
        mock_repo_instance.get_all_jobs = AsyncMock()
        mock_repo_instance.get_job_by_id = AsyncMock()
        mock_repo_instance.update_job = AsyncMock()
        service = JobService()
        service.job_repo = mock_repo_instance
        yield service


@pytest.mark.asyncio
class TestJobService:
    async def test_create_job_success(self, job_service):
        request_data = CreateJobRequest(
            jobTitle="Senior Backend Engineer",
            jobDetails="Design and implement scalable backend services.",
            jobRole="Backend Development",
            requiredSkills=["Python", "FastAPI", "MongoDB"],
            experienceRequired="3+ years",
            employmentType="Full Time",
            location="Indore, MP",
        )

        mock_return = request_data.model_dump()
        mock_return["_id"] = "64abcdef1234567890"
        job_service.job_repo.create_job.return_value = mock_return

        result = await job_service.create_job(request_data)

        assert result["_id"] == "64abcdef1234567890"
        assert result["jobTitle"] == "Senior Backend Engineer"
        job_service.job_repo.create_job.assert_called_once()

    async def test_get_all_jobs(self, job_service):
        job_service.job_repo.get_all_jobs.return_value = ([{"jobTitle": "Job 1"}, {"jobTitle": "Job 2"}], 2)

        result = await job_service.get_all_jobs(search="backend", page=1, limit=10)

        assert len(result[0]) == 2
        assert result[1]["total_items"] == 2
        job_service.job_repo.get_all_jobs.assert_called_once()

    async def test_get_job_by_id_success(self, job_service):
        job_service.job_repo.get_job_by_id.return_value = {"jobTitle": "Software Engineer"}

        result = await job_service.get_job_by_id("valid_id")

        assert result["jobTitle"] == "Software Engineer"
        job_service.job_repo.get_job_by_id.assert_called_once_with("valid_id")

    async def test_get_job_by_id_not_found(self, job_service):
        job_service.job_repo.get_job_by_id.return_value = None

        with pytest.raises(AppBaseException) as exc_info:
            await job_service.get_job_by_id("invalid_id")

        assert exc_info.value.status_code == 404
        assert exc_info.value.error_code == "JOB_NOT_FOUND"

    async def test_update_job_success(self, job_service):
        update_request = UpdateJobRequest(jobTitle="Lead Engineer")
        job_service.job_repo.get_job_by_id.return_value = {"_id": "123", "jobTitle": "Senior Engineer"}
        job_service.job_repo.update_job.return_value = {"_id": "123", "jobTitle": "Lead Engineer"}

        result = await job_service.update_job("123", update_request)

        assert result["jobTitle"] == "Lead Engineer"
        job_service.job_repo.update_job.assert_called_once()

    async def test_update_job_not_found(self, job_service):
        update_request = UpdateJobRequest(jobTitle="Lead Engineer")
        job_service.job_repo.get_job_by_id.return_value = None

        with pytest.raises(AppBaseException) as exc_info:
            await job_service.update_job("invalid_id", update_request)

        assert exc_info.value.status_code == 404
        assert exc_info.value.error_code == "JOB_NOT_FOUND"
        job_service.job_repo.update_job.assert_not_called()
