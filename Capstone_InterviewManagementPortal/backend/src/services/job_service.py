"""Service layer for Job Description management workflows.

The JobService coordinates business rules and delegates persistence to the
repository layer. Docstrings describe the expected behavior without altering
business logic.
"""

import logging

from src.repositories.job_repository import JobRepository
from src.schemas.request.job_request import CreateJobRequest, UpdateJobRequest
from src.exceptions.custom_exceptions import AppBaseException

logger = logging.getLogger(__name__)


class JobService:
    """Coordinate job description business rules and persistence operations."""

    def __init__(self):
        # Repository instance used for all persistence operations.
        self.job_repo = JobRepository()

    async def create_job(self, request: CreateJobRequest) -> dict:
        """Create a new job description after applying default business rules.

        Converts the validated Pydantic `CreateJobRequest` to a plain dictionary
        and enforces service-level defaults. Currently the only default applied
        is `is_active = True` so newly created postings are open by default.

        Args:
            request: Validated create-job payload.

        Returns:
            The persisted job document as a dictionary (includes `_id`).
        """
        logger.info("Creating job description")
        try:
            job_data = request.model_dump()
            job_data["is_active"] = True
            return await self.job_repo.create_job(job_data)
        except Exception:
            logger.exception("Unexpected error while creating job")
            raise

    async def get_all_jobs(self) -> list:
        """Return all job descriptions sorted newest-first.

        This method delegates directly to the repository and does not apply
        additional business rules.
        """
        logger.info("Fetching all job descriptions")
        try:
            return await self.job_repo.get_all_jobs()
        except Exception:
            logger.exception("Unexpected error while fetching all jobs")
            raise

    async def get_job_by_id(self, job_id: str) -> dict:
        """Fetch a single job by its identifier.

        Raises:
            AppBaseException: When the job cannot be found.
        """
        logger.info("Fetching job description by ID: %s", job_id)
        try:
            job = await self.job_repo.get_job_by_id(job_id)
            if not job:
                logger.warning("Job description not found for ID: %s", job_id)
                raise AppBaseException("Job description not found", "JOB_NOT_FOUND", 404)
            return job
        except AppBaseException:
            raise
        except Exception:
            logger.exception("Unexpected error while fetching job by ID: %s", job_id)
            raise

    async def update_job(self, job_id: str, request: UpdateJobRequest) -> dict:
        """Apply partial updates to an existing job description.

        The method first confirms the job exists. It then extracts only the
        fields present in the patch request (to avoid overwriting omitted
        fields) and delegates the update to the repository.

        Raises:
            AppBaseException: When the job is not found or no valid fields
            were supplied for the update.
        """
        logger.info("Updating job description: %s", job_id)
        try:
            existing_job = await self.job_repo.get_job_by_id(job_id)
            if not existing_job:
                logger.warning("Job description not found for update: %s", job_id)
                raise AppBaseException("Job description not found", "JOB_NOT_FOUND", 404)

            update_data = request.model_dump(exclude_unset=True)
            if not update_data:
                logger.warning("Empty update payload received for job ID: %s", job_id)
                raise AppBaseException("No valid fields provided for update", "BAD_REQUEST", 400)

            return await self.job_repo.update_job(job_id, update_data)
        except AppBaseException:
            raise
        except Exception:
            logger.exception("Unexpected error while updating job: %s", job_id)
            raise
