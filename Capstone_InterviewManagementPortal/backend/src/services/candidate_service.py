"""Service layer for candidate management workflows."""

import logging

from src.exceptions.custom_exceptions import AppBaseException
from src.repositories.candidate_repository import CandidateRepository
from src.schemas.request.candidate_request import (
    CandidateCreateRequest,
    CandidateUpdateRequest,
)

logger = logging.getLogger(__name__)


class CandidateService:
    """Coordinate candidate business rules and persistence operations."""

    def __init__(self):
        """Initialize the candidate service with repository dependencies."""
        self.candidate_repo = CandidateRepository()

    async def create_candidate(self, request: CandidateCreateRequest) -> dict:
        """Create a new candidate after validating uniqueness rules.

        Args:
            request: Candidate details submitted by the client.

        Returns:
            dict: Newly created candidate document.
        """
        await self._ensure_unique_email(request.email)
        await self._ensure_unique_mobile(request.mobile)

        candidate_data = request.model_dump()
        candidate_data["status"] = request.status.value

        try:
            candidate = await self.candidate_repo.create_candidate(candidate_data)
            logger.info("Candidate created successfully")
            return candidate
        except Exception:
            logger.exception("Unexpected repository failure during candidate creation")
            raise

    async def get_all_candidates(self, search: str | None = None) -> list[dict]:
        """Return all candidates matching the optional search term.

        Args:
            search: Optional search term applied in the repository layer.

        Returns:
            list[dict]: Candidate records returned by the repository.
        """
        candidates = await self.candidate_repo.get_all_candidates(search=search)
        logger.info("Candidates retrieved successfully")
        return candidates

    async def get_candidate_by_id(self, candidate_id: str) -> dict:
        """Return a candidate by identifier or raise a not-found error.

        Args:
            candidate_id: Candidate ObjectId string.

        Returns:
            dict: Matching candidate document.
        """
        candidate = await self.candidate_repo.get_candidate_by_id(candidate_id)
        if not candidate:
            raise AppBaseException("Candidate not found", "CANDIDATE_NOT_FOUND", 404)

        logger.info("Candidate retrieved successfully")
        return candidate

    async def update_candidate(self, candidate_id: str, request: CandidateUpdateRequest) -> dict:
        """Update an existing candidate after applying business validations.

        Args:
            candidate_id: Candidate ObjectId string.
            request: Partial candidate update payload.

        Returns:
            dict: Updated candidate document.
        """
        existing_candidate = await self.get_candidate_by_id(candidate_id)
        update_data = request.model_dump(exclude_unset=True)
        if not update_data:
            raise AppBaseException("No valid fields provided for update", "INVALID_UPDATE", 400)

        if "email" in update_data and update_data["email"] != existing_candidate["email"]:
            await self._ensure_unique_email(update_data["email"], candidate_id)

        if "mobile" in update_data and update_data["mobile"] != existing_candidate["mobile"]:
            await self._ensure_unique_mobile(update_data["mobile"], candidate_id)

        if "status" in update_data:
            update_data["status"] = update_data["status"].value

        try:
            candidate = await self.candidate_repo.update_candidate(candidate_id, update_data)
            logger.info("Candidate updated successfully")
            return candidate
        except Exception:
            logger.exception("Unexpected repository failure during candidate update")
            raise

    async def _ensure_unique_email(self, email: str, candidate_id: str | None = None) -> None:
        """Reject duplicate candidate emails.

        Args:
            email: Candidate email address to validate.
            candidate_id: Optional current candidate id for update exclusions.

        Returns:
            None
        """
        existing_candidate = await self.candidate_repo.get_candidate_by_email(email)
        if existing_candidate and existing_candidate.get("_id") != candidate_id:
            logger.warning("Duplicate email attempted")
            raise AppBaseException("Candidate email already exists", "CANDIDATE_EMAIL_EXISTS", 400)

    async def _ensure_unique_mobile(self, mobile: str, candidate_id: str | None = None) -> None:
        """Reject duplicate candidate mobile numbers.

        Args:
            mobile: Candidate mobile number to validate.
            candidate_id: Optional current candidate id for update exclusions.

        Returns:
            None
        """
        existing_candidate = await self.candidate_repo.get_candidate_by_mobile(mobile)
        if existing_candidate and existing_candidate.get("_id") != candidate_id:
            logger.warning("Duplicate mobile attempted")
            raise AppBaseException("Candidate mobile already exists", "CANDIDATE_MOBILE_EXISTS", 400)
