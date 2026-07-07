"""Service layer for interview scheduling workflows."""

import logging
from datetime import date

from src.enums.app_enums import CandidateStatus, UserRole
from src.exceptions.custom_exceptions import AppBaseException
from src.repositories.interview_repository import InterviewRepository
from src.schemas.request.interview_request import InterviewCreateRequest, InterviewUpdateRequest

logger = logging.getLogger(__name__)


class InterviewService:
    """Coordinate interview business rules and persistence operations."""

    def __init__(self):
        """Initialize the service with the interview repository dependency."""
        self.interview_repo = InterviewRepository()

    @staticmethod
    def _build_meta(page: int, limit: int, total_items: int) -> dict:
        """Build pagination metadata for list responses."""
        total_pages = max(1, (total_items + limit - 1) // limit)
        return {"page": page, "limit": limit, "total_items": total_items, "total_pages": total_pages}

    async def create_interview(self, request: InterviewCreateRequest) -> dict:
        """Create a new interview schedule."""
        await self._validate_references(request.candidate_id, request.job_id, request.interviewer_id)
        candidate = await self.interview_repo.get_candidate_by_id(request.candidate_id)
        if await self.interview_repo.find_overlapping_interview(request.candidate_id, request.interview_date, request.interview_time):
            raise AppBaseException("Candidate already has an interview at this time", "INTERVIEW_CONFLICT", 400)
        if request.interview_date < date.today():
            raise AppBaseException("Interview date cannot be in the past", "INVALID_INTERVIEW_DATE", 400)

        payload = {
            "candidate_id": candidate["_id"],
            "candidate_name": f"{candidate.get('first_name', '')} {candidate.get('last_name', '')}".strip(),
            "job_id": request.job_id,
            "job_title": (await self.interview_repo.get_job_by_id(request.job_id)).get("jobTitle", ""),
            "interviewer_id": request.interviewer_id,
            "interviewer_name": (await self.interview_repo.get_user_by_id(request.interviewer_id)).get("name", ""),
            "interview_date": request.interview_date,
            "interview_time": request.interview_time,
            "focus_tech_areas": request.focus_tech_areas,
            "status": CandidateStatus.INTERVIEW_SCHEDULED.value,
        }
        result = await self.interview_repo.create_interview(payload)
        logger.info("Interview scheduled successfully: %s", result.get("_id"))
        return result

    async def update_interview(self, interview_id: str, request: InterviewUpdateRequest) -> dict:
        """Update an existing interview schedule."""
        existing = await self.get_interview_by_id(interview_id)
        update_data = request.model_dump(exclude_unset=True, by_alias=False)
        if not update_data:
            raise AppBaseException("No valid fields provided for update", "INVALID_UPDATE", 400)
        if "candidate_id" in update_data or "job_id" in update_data or "interviewer_id" in update_data:
            candidate_id = update_data.get("candidate_id", existing["candidate_id"])
            job_id = update_data.get("job_id", existing["job_id"])
            interviewer_id = update_data.get("interviewer_id", existing["interviewer_id"])
            await self._validate_references(candidate_id, job_id, interviewer_id)
        if "interview_date" in update_data and update_data["interview_date"] < date.today():
            raise AppBaseException("Interview date cannot be in the past", "INVALID_INTERVIEW_DATE", 400)
        candidate_id = update_data.get("candidate_id", existing["candidate_id"])
        interview_date = update_data.get("interview_date", existing["interview_date"])
        interview_time = update_data.get("interview_time", existing["interview_time"])
        if await self.interview_repo.find_overlapping_interview(candidate_id, interview_date, interview_time, exclude_id=interview_id):
            raise AppBaseException("Candidate already has an interview at this time", "INTERVIEW_CONFLICT", 400)
        result = await self.interview_repo.update_interview(interview_id, update_data)
        if not result:
            raise AppBaseException("Interview not found", "INTERVIEW_NOT_FOUND", 404)
        logger.info("Interview updated successfully: %s", interview_id)
        return result

    async def get_interview_by_id(self, interview_id: str) -> dict:
        """Return a single interview by identifier."""
        interview = await self.interview_repo.get_interview_by_id(interview_id)
        if not interview:
            raise AppBaseException("Interview not found", "INTERVIEW_NOT_FOUND", 404)
        return interview

    async def get_all_interviews(self, search: str | None = None, page: int = 1, limit: int = 10) -> tuple[list, dict]:
        """Return interviews with optional server-side search."""
        query = await self._build_search_query(search)
        interviews, total_items = await self.interview_repo.get_all_interviews(query, page=page, limit=limit)
        logger.info("Interview list retrieved successfully")
        return interviews, self._build_meta(page, limit, total_items)

    async def _validate_references(self, candidate_id: str, job_id: str, interviewer_id: str) -> None:
        """Validate candidate, job, and interviewer references."""
        candidate = await self.interview_repo.get_candidate_by_id(candidate_id)
        if not candidate:
            raise AppBaseException("Candidate not found", "CANDIDATE_NOT_FOUND", 404)
        job = await self.interview_repo.get_job_by_id(job_id)
        if not job:
            raise AppBaseException("Job not found", "JOB_NOT_FOUND", 404)
        interviewer = await self.interview_repo.get_user_by_id(interviewer_id)
        if not interviewer:
            raise AppBaseException("Interviewer not found", "USER_NOT_FOUND", 404)
        if interviewer.get("role") != UserRole.INTERVIEWER.value:
            raise AppBaseException("Assigned interviewer must have INTERVIEWER role", "INVALID_INTERVIEWER_ROLE", 400)

    async def _build_search_query(self, search: str | None) -> dict:
        """Build the MongoDB query for interview search."""
        search_term = (search or "").strip()
        if not search_term:
            return {}
        return {
            "$or": [
                {"candidate_name": {"$regex": search_term, "$options": "i"}},
                {"job_title": {"$regex": search_term, "$options": "i"}},
                {"interviewer_name": {"$regex": search_term, "$options": "i"}},
                {"focus_tech_areas": {"$elemMatch": {"$regex": search_term, "$options": "i"}}},
            ]
        }
