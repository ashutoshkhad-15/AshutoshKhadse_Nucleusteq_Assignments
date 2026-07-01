"""Service layer for Job Description management workflows.

The JobService coordinates business rules and delegates persistence to the
repository layer. Docstrings describe the expected behavior without altering
business logic.
"""

from src.repositories.job_repository import JobRepository
from src.schemas.request.job_request import CreateJobRequest, UpdateJobRequest
from src.exceptions.custom_exceptions import AppBaseException


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
        # Convert Pydantic model to a standard dictionary
        job_data = request.model_dump()

        # All new jobs are active/open by default
        job_data["is_active"] = True

        return await self.job_repo.create_job(job_data)

    async def get_all_jobs(self, search: str | None = None, is_active: bool | None = None) -> list:
        """Return all job descriptions sorted newest-first.

        This method delegates directly to the repository and does not apply
        additional business rules.
        """
        query: dict = {}

        if search:
            query["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"department": {"$regex": search, "$options": "i"}},
                {"location": {"$regex": search, "$options": "i"}},
                {"experience_required": {"$regex": search, "$options": "i"}},
                {"skills": {"$elemMatch": {"$regex": search, "$options": "i"}}},
            ]

        if is_active is not None:
            query["is_active"] = is_active

        return await self.job_repo.get_all_jobs(query)

    async def get_job_by_id(self, job_id: str) -> dict:
        """Fetch a single job by its identifier.

        Raises:
            AppBaseException: When the job cannot be found.
        """
        job = await self.job_repo.get_job_by_id(job_id)
        if not job:
            # Surface a consistent application-level error when missing
            raise AppBaseException("Job description not found", "JOB_NOT_FOUND", 404)
        return job

    async def update_job(self, job_id: str, request: UpdateJobRequest) -> dict:
        """Apply partial updates to an existing job description.

        The method first confirms the job exists. It then extracts only the
        fields present in the patch request (to avoid overwriting omitted
        fields) and delegates the update to the repository.

        Raises:
            AppBaseException: When the job is not found or no valid fields
            were supplied for the update.
        """
        # Ensure the job exists before attempting to update it
        existing_job = await self.job_repo.get_job_by_id(job_id)
        if not existing_job:
            raise AppBaseException("Job description not found", "JOB_NOT_FOUND", 404)

        # Drop any fields that were not provided in the patch request
        update_data = request.model_dump(exclude_unset=True)

        if not update_data:
            # Prevent empty PATCH operations which are likely client errors
            raise AppBaseException("No valid fields provided for update", "BAD_REQUEST", 400)

        return await self.job_repo.update_job(job_id, update_data)
