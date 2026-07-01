"""Service tests for the Job Description workflow.

Tests cover creation, retrieval, and update behavior for the JobService
while stubbing repository interactions.
"""

import pytest
from unittest.mock import AsyncMock, patch
from src.services.job_service import JobService
from src.schemas.request.job_request import CreateJobRequest, UpdateJobRequest
from src.exceptions.custom_exceptions import AppBaseException

@pytest.fixture
def job_service():
    with patch('src.services.job_service.JobRepository') as mock_repo_class:
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
        """Create a job and return the stored job metadata."""
        request_data = CreateJobRequest(
            title="Senior Backend Engineer",
            department="Engineering",
            description="Looking for an experienced Python developer.",
            skills=["Python", "FastAPI", "MongoDB"],
            experience_required="3-5 years",
            location="Indore, MP"
        )
        
        # Setup mock return
        mock_return = request_data.model_dump()
        mock_return["_id"] = "64abcdef1234567890"
        mock_return["is_active"] = True
        job_service.job_repo.create_job.return_value = mock_return
        
        # Execute
        result = await job_service.create_job(request_data)
        
        # Assertions
        assert result["_id"] == "64abcdef1234567890"
        assert result["title"] == "Senior Backend Engineer"
        assert result["is_active"] is True
        job_service.job_repo.create_job.assert_called_once()

    async def test_get_all_jobs(self, job_service):
        """Return all job descriptions from the repository."""
        job_service.job_repo.get_all_jobs.return_value = [{"title": "Job 1"}, {"title": "Job 2"}]
        
        result = await job_service.get_all_jobs()
        
        assert len(result) == 2
        job_service.job_repo.get_all_jobs.assert_called_once()

    async def test_get_job_by_id_success(self, job_service):
        """Return a job document when a valid ID is provided."""
        job_service.job_repo.get_job_by_id.return_value = {"title": "Software Engineer"}
        
        result = await job_service.get_job_by_id("valid_id")
        
        assert result["title"] == "Software Engineer"
        job_service.job_repo.get_job_by_id.assert_called_once_with("valid_id")

    async def test_get_job_by_id_not_found(self, job_service):
        """Raise AppBaseException when the requested job does not exist."""
        job_service.job_repo.get_job_by_id.return_value = None
        
        with pytest.raises(AppBaseException) as exc_info:
            await job_service.get_job_by_id("invalid_id")
            
        assert exc_info.value.status_code == 404
        assert exc_info.value.error_code == "JOB_NOT_FOUND"

    async def test_update_job_success(self, job_service):
        """Return updated job data when the update request is valid."""
        update_request = UpdateJobRequest(title="Lead Engineer")
        
        # Mock finding the existing job
        job_service.job_repo.get_job_by_id.return_value = {"_id": "123", "title": "Senior Engineer"}
        # Mock the successful update return
        job_service.job_repo.update_job.return_value = {"_id": "123", "title": "Lead Engineer"}
        
        result = await job_service.update_job("123", update_request)
        
        assert result["title"] == "Lead Engineer"
        job_service.job_repo.update_job.assert_called_once()

    async def test_update_job_not_found(self, job_service):
        """Raise AppBaseException when attempting to update a missing job."""
        update_request = UpdateJobRequest(title="Lead Engineer")
        
        # Mock failing to find the job
        job_service.job_repo.get_job_by_id.return_value = None
        
        with pytest.raises(AppBaseException) as exc_info:
            await job_service.update_job("invalid_id", update_request)
            
        assert exc_info.value.status_code == 404
        assert exc_info.value.error_code == "JOB_NOT_FOUND"
        job_service.job_repo.update_job.assert_not_called()