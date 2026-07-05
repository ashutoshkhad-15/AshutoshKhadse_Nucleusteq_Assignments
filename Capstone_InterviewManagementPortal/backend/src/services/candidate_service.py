"""Service layer for candidate management workflows."""

import logging

from src.exceptions.custom_exceptions import AppBaseException
from src.repositories.candidate_repository import CandidateRepository
from src.schemas.request.candidate_request import CandidateCreateRequest, CandidateUpdateRequest

logger = logging.getLogger(__name__)


class CandidateService:
    """Coordinate candidate business rules and persistence operations."""

    def __init__(self):
        """Initialize the candidate service with repository dependencies."""
        self.candidate_repo = CandidateRepository()

    async def create_candidate(self, request: CandidateCreateRequest) -> dict:
        """Create a new candidate after validating uniqueness and job existence."""
        await self._ensure_unique_email(request.email)
        await self._ensure_unique_mobile(request.mobile)
        await self._ensure_valid_job(request.applied_job_id)
        candidate_data = request.model_dump(by_alias=False)
        try:
            logger.info("Creating candidate profile")
            return await self.candidate_repo.create_candidate(candidate_data)
        except Exception:
            logger.exception("Unexpected repository failure during candidate creation")
            raise

    async def get_all_candidates(self, search: str | None = None, page: int = 1, limit: int = 10) -> tuple[list[dict], dict]:
        """Return all candidates matching an optional search term."""
        query = await self._build_search_query(search)
        try:
            candidates, total_items = await self.candidate_repo.get_all_candidates(query, page=page, limit=limit)
            total_pages = max(1, (total_items + limit - 1) // limit)
            return candidates, {"page": page, "limit": limit, "total_items": total_items, "total_pages": total_pages}
        except Exception:
            logger.exception("Unexpected error while fetching all candidates")
            raise

    async def get_candidate_by_id(self, candidate_id: str) -> dict:
        """Fetch a single candidate by identifier."""
        try:
            candidate = await self.candidate_repo.get_candidate_by_id(candidate_id)
            if not candidate:
                raise AppBaseException("Candidate not found", "CANDIDATE_NOT_FOUND", 404)
            return candidate
        except AppBaseException:
            raise
        except Exception:
            logger.exception("Unexpected error while fetching candidate by ID: %s", candidate_id)
            raise

    async def update_candidate(self, candidate_id: str, request: CandidateUpdateRequest) -> dict:
        """Apply partial updates to an existing candidate."""
        existing_candidate = await self.get_candidate_by_id(candidate_id)
        update_data = request.model_dump(exclude_unset=True, by_alias=False)
        if not update_data:
            raise AppBaseException("No valid fields provided for update", "INVALID_UPDATE", 400)

        if "email" in update_data and update_data["email"] != existing_candidate["email"]:
            await self._ensure_unique_email(update_data["email"], candidate_id)
        if "mobile" in update_data and update_data["mobile"] != existing_candidate["mobile"]:
            await self._ensure_unique_mobile(update_data["mobile"], candidate_id)
        if "applied_job_id" in update_data:
            await self._ensure_valid_job(update_data["applied_job_id"])

        try:
            logger.info("Updating candidate profile: %s", candidate_id)
            candidate = await self.candidate_repo.update_candidate(candidate_id, update_data)
            if not candidate:
                raise AppBaseException("Candidate not found", "CANDIDATE_NOT_FOUND", 404)
            return candidate
        except AppBaseException:
            raise
        except Exception:
            logger.exception("Unexpected repository failure during candidate update")
            raise

    async def get_jobs_for_dropdown(self, search: str | None = None) -> list[dict]:
        """Return job options for the applied-job searchable dropdown."""
        try:
            return await self.candidate_repo.get_jobs_by_title((search or "").strip())
        except Exception:
            logger.exception("Unexpected error while fetching job dropdown data")
            raise

    async def _build_search_query(self, search: str | None) -> dict:
        """Build a Mongo query for candidate search."""
        search_term = (search or "").strip()
        if not search_term:
            return {}
        job_id_matches = await self.candidate_repo.get_jobs_by_title(search_term)
        job_ids = [job["_id"] for job in job_id_matches]
        return {
            "$or": [
                {"first_name": {"$regex": search_term, "$options": "i"}},
                {"last_name": {"$regex": search_term, "$options": "i"}},
                {"email": {"$regex": search_term, "$options": "i"}},
                {"mobile": {"$regex": search_term, "$options": "i"}},
                {"current_company": {"$regex": search_term, "$options": "i"}},
                {"applied_job_id": {"$in": job_ids}},
            ]
        }

    async def _ensure_unique_email(self, email: str, candidate_id: str | None = None) -> None:
        """Reject duplicate candidate emails."""
        existing_candidate = await self.candidate_repo.get_candidate_by_email(email)
        if existing_candidate and existing_candidate.get("_id") != candidate_id:
            raise AppBaseException("Candidate email already exists", "CANDIDATE_EMAIL_EXISTS", 400)

    async def _ensure_unique_mobile(self, mobile: str, candidate_id: str | None = None) -> None:
        """Reject duplicate candidate mobile numbers."""
        existing_candidate = await self.candidate_repo.get_candidate_by_mobile(mobile)
        if existing_candidate and existing_candidate.get("_id") != candidate_id:
            raise AppBaseException("Candidate mobile already exists", "CANDIDATE_MOBILE_EXISTS", 400)

    async def _ensure_valid_job(self, applied_job_id: str) -> None:
        """Reject invalid applied-job selections."""
        if not await self.candidate_repo.get_job_by_id(applied_job_id):
            raise AppBaseException("Applied job not found", "APPLIED_JOB_NOT_FOUND", 400)
