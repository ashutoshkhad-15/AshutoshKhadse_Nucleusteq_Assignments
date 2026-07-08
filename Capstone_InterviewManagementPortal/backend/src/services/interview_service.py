"""Service layer for interview scheduling workflows."""

import logging
from datetime import date, datetime, timedelta, timezone

from src.enums.app_enums import CandidateStatus, UserRole
from src.exceptions.custom_exceptions import AppBaseException
from src.repositories.interview_repository import InterviewRepository
from src.schemas.request.interview_request import InterviewCreateRequest, InterviewUpdateRequest
from src.services.candidate_service import CandidateService
from src.repositories.user_repository import UserRepository

logger = logging.getLogger(__name__)
IST = timezone(timedelta(hours=5, minutes=30))


class InterviewService:
    """Coordinate interview business rules and persistence operations."""

    def __init__(self):
        """Initialize the service with the interview repository dependency."""
        self.interview_repo = InterviewRepository()
        self.candidate_service = CandidateService()
        self.user_repo = UserRepository()

    @staticmethod
    def _build_meta(page: int, limit: int, total_items: int) -> dict:
        """Build pagination metadata for list responses."""
        total_pages = max(1, (total_items + limit - 1) // limit)
        return {"page": page, "limit": limit, "total_items": total_items, "total_pages": total_pages}

    async def create_interview(self, request: InterviewCreateRequest) -> dict:
        """Create a new interview schedule."""
        await self._validate_references(request.candidate_id, request.job_id, request.interviewer_id)
        candidate = await self.interview_repo.get_candidate_by_id(request.candidate_id)
        scheduled_time = self._build_scheduled_datetime(request.interview_date, request.interview_time)
        if scheduled_time <= self._now_ist():
            raise AppBaseException("Interview date cannot be in the past", "INVALID_INTERVIEW_DATE", 400)
        if await self.interview_repo.find_overlapping_interview(request.candidate_id, scheduled_time, request.interview_time):
            raise AppBaseException("Candidate already has an interview at this time", "INTERVIEW_CONFLICT", 400)
        interviewer = await self.interview_repo.get_user_by_id(request.interviewer_id)
        job = await self.interview_repo.get_job_by_id(request.job_id)

        if not candidate:
            raise AppBaseException("Candidate not found", "CANDIDATE_NOT_FOUND", 404)
        if not job:
            raise AppBaseException("Job not found", "JOB_NOT_FOUND", 404)
        if not interviewer:
            raise AppBaseException("Interviewer not found", "USER_NOT_FOUND", 404)

        payload = {
            "candidate_id": candidate["_id"],
            "candidate_name": f"{candidate.get('first_name', '')} {candidate.get('last_name', '')}".strip(),
            "job_id": request.job_id,
            "job_title": job.get("jobTitle", ""),
            "interviewer_id": request.interviewer_id,
            "interviewer_name": interviewer.get("name", ""),
            "interview_date": scheduled_time,
            "interview_time": request.interview_time,
            "focus_tech_areas": request.focus_tech_areas,
            "status": "SCHEDULED",
        }
        result = await self.interview_repo.create_interview(payload)
        await self.candidate_service.update_candidate_status(candidate["_id"], CandidateStatus.INTERVIEW_SCHEDULED.value, source="system")
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
        candidate_id = update_data.get("candidate_id", existing["candidate_id"])
        interview_date_value = update_data.get("interview_date", existing["interview_date"])
        interview_time = update_data.get("interview_time", existing["interview_time"])
        interview_date = self._coerce_date(interview_date_value)
        scheduled_time = self._build_scheduled_datetime(interview_date, interview_time)
        if scheduled_time <= self._now_ist():
            raise AppBaseException("Interview time cannot be in the past.", "INVALID_INTERVIEW_TIME", 400)
        if await self.interview_repo.find_overlapping_interview(candidate_id, scheduled_time, interview_time, exclude_id=interview_id):
            raise AppBaseException("Candidate already has an interview at this time", "INTERVIEW_CONFLICT", 400)
        if "interview_date" in update_data:
            update_data["interview_date"] = scheduled_time
        elif "interview_time" in update_data and existing.get("interview_date"):
            update_data["interview_date"] = scheduled_time
        result = await self.interview_repo.update_interview(interview_id, update_data)
        if not result:
            raise AppBaseException("Interview not found", "INTERVIEW_NOT_FOUND", 404)
        logger.info("Interview updated successfully: %s", interview_id)
        return result

    async def get_interview_by_id(self, interview_id: str) -> dict:
        """Return a single interview by identifier."""
        await self._sync_overdue_interviews()
        interview = await self.interview_repo.get_interview_by_id(interview_id)
        if not interview:
            raise AppBaseException("Interview not found", "INTERVIEW_NOT_FOUND", 404)
        return interview

    async def get_interview_for_user(self, interview_id: str, current_user: dict) -> dict:
        """Return an interview with interviewer scoping enforced when required."""
        role = current_user.get("role")
        if role == UserRole.INTERVIEWER.value:
            interviewer_id = str(current_user.get("_id") or current_user.get("id") or "")
            return await self.get_interview_for_interviewer(interview_id, interviewer_id)
        return await self.get_interview_by_id(interview_id)

    async def get_all_interviews(self, search: str | None = None, page: int = 1, limit: int = 10) -> tuple[list, dict]:
        """Return interviews with optional server-side search."""
        await self._sync_overdue_interviews()
        query = await self._build_search_query(search)
        interviews, total_items = await self.interview_repo.get_all_interviews(query, page=page, limit=limit)
        logger.info("Interview list retrieved successfully")
        return interviews, self._build_meta(page, limit, total_items)

    async def get_assigned_interviews(self, interviewer_id: str, page: int = 1, limit: int = 10) -> tuple[list, dict]:
        """Return interviews assigned to a single interviewer."""
        await self._sync_overdue_interviews()
        query = {"interviewer_id": interviewer_id}
        interviews, total_items = await self.interview_repo.get_all_interviews(query, page=page, limit=limit)
        return interviews, self._build_meta(page, limit, total_items)

    async def get_interviewers(self, search: str | None = None, page: int = 1, limit: int = 100) -> tuple[list, dict]:
        """Return interviewer users for scheduling dropdowns."""
        query = {"role": UserRole.INTERVIEWER.value}
        if search and search.strip():
            search_term = search.strip()
            query["$or"] = [
                {"name": {"$regex": search_term, "$options": "i"}},
                {"email": {"$regex": search_term, "$options": "i"}},
            ]
        total_items = await self.user_repo.collection.count_documents(query)
        cursor = (
            self.user_repo.collection.find(query, {"password_base64": 0})
            .sort([("name", 1), ("_id", 1)])
            .skip((page - 1) * limit)
            .limit(limit)
        )
        users = []
        async for user in cursor:
            user["_id"] = str(user["_id"])
            users.append(user)
        return users, self._build_meta(page, limit, total_items)

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

    async def get_interview_for_feedback(self, interview_id: str) -> dict:
        """Return an interview and ensure it can accept feedback."""
        interview = await self.get_interview_by_id(interview_id)
        self._ensure_feedback_window_has_opened(interview)
        return interview

    async def get_interview_for_interviewer(self, interview_id: str, interviewer_id: str) -> dict:
        """Return an interview only if it belongs to the interviewer."""
        await self._sync_overdue_interviews()
        interview = await self.interview_repo.get_interview_by_id_and_interviewer(interview_id, interviewer_id)
        if not interview:
            raise AppBaseException("Interview not found", "INTERVIEW_NOT_FOUND", 404)
        return interview

    def _ensure_feedback_window_has_opened(self, interview: dict) -> None:
        """Reject feedback submissions before the scheduled interview time."""
        scheduled_time = self._get_scheduled_datetime(interview)
        if scheduled_time and scheduled_time > self._now_ist():
            raise AppBaseException(
                "Feedback can only be submitted after the scheduled interview has been completed.",
                "FEEDBACK_NOT_ALLOWED",
                400,
            )

    def _get_scheduled_datetime(self, interview: dict) -> datetime | None:
        """Return the scheduled interview datetime in IST."""
        interview_date = interview.get("interview_date")
        interview_time = interview.get("interview_time")
        if not interview_date or not interview_time:
            return None
        return self._build_scheduled_datetime(self._coerce_date(interview_date), interview_time)

    @staticmethod
    def _coerce_date(value: date | datetime | str) -> date:
        """Convert an interview date into a date value."""
        if isinstance(value, date) and not isinstance(value, datetime):
            return value
        if isinstance(value, datetime):
            return value.astimezone(IST).date() if value.tzinfo else value.date()
        if isinstance(value, str):
            return date.fromisoformat(value[:10])
        return value

    @staticmethod
    def _now_ist() -> datetime:
        """Return the current server time in IST."""
        return datetime.now(IST)

    @staticmethod
    def _build_scheduled_datetime(interview_date: date, interview_time: str) -> datetime:
        """Build a timezone-aware interview datetime in IST."""
        scheduled_time = datetime.strptime(interview_time, "%H:%M").time()
        return datetime.combine(interview_date, scheduled_time, tzinfo=IST)

    async def _sync_overdue_interviews(self) -> None:
        """Advance overdue interviews to completed status before reads."""
        overdue_interviews = await self.interview_repo.complete_overdue_interviews(self._now_ist())
        for interview in overdue_interviews:
            if not interview:
                continue
            candidate_id = interview.get("candidate_id")
            if not candidate_id:
                continue
            try:
                await self.candidate_service.update_candidate_status(
                    candidate_id,
                    CandidateStatus.INTERVIEW_COMPLETED.value,
                    source="system",
                )
            except AppBaseException as exc:
                if exc.error_code != "INVALID_STATUS_TRANSITION":
                    raise
