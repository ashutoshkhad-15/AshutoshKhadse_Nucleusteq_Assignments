"""Service layer for interview scheduling workflows."""

import logging
from datetime import datetime, date, timezone, timedelta

from src.enums.app_enums import CandidateStatus, UserRole
from src.exceptions.custom_exceptions import AppBaseException
from src.repositories.interview_repository import InterviewRepository
from src.services.candidate_service import CandidateService
from src.schemas.request.interview_request import InterviewCreateRequest, InterviewUpdateRequest
from src.utils.common import build_pagination_meta, get_user_role, normalize_search_term

logger = logging.getLogger(__name__)


class InterviewService:
    """Coordinate interview business rules and persistence operations."""

    def __init__(self):
        """Initialize the service with the interview repository dependency."""
        self.interview_repo = InterviewRepository()
        self.ist_timezone = timezone(timedelta(hours=5, minutes=30))
        self.candidate_service = CandidateService()

    async def create_interview(self, request: InterviewCreateRequest) -> dict:
        """Create a new interview schedule."""
        await self._validate_references(request.candidate_id, request.job_id, request.interviewer_id)
        candidate = await self.interview_repo.get_candidate_by_id(request.candidate_id)
        job = await self.interview_repo.get_job_by_id(request.job_id)
        interviewer = await self.interview_repo.get_user_by_id(request.interviewer_id)
        candidate_status = candidate.get("status") or CandidateStatus.PROFILE_CREATED.value
        allowed_candidate_statuses = {CandidateStatus.PROFILE_CREATED.value, CandidateStatus.INTERVIEW_COMPLETED.value}
        if candidate_status not in allowed_candidate_statuses:
            raise AppBaseException(
                "Candidate already has an interview scheduled.",
                "INVALID_CANDIDATE_STATUS",
                400,
            )
        if await self.interview_repo.has_active_scheduled_interview(request.candidate_id):
            raise AppBaseException("Candidate already has an interview scheduled", "INTERVIEW_CONFLICT", 400)
        current_ist = datetime.now(self.ist_timezone)
        if request.interview_date < current_ist.date():
            raise AppBaseException("Interview date cannot be in the past", "INVALID_INTERVIEW_DATE", 400)
        if request.interview_date == current_ist.date():
            interview_time = datetime.strptime(request.interview_time, "%H:%M").time()
            if interview_time <= current_ist.time().replace(second=0, microsecond=0):
                raise AppBaseException("Interview time must be in the future", "INVALID_INTERVIEW_TIME", 400)
        if await self.interview_repo.find_overlapping_interview(request.candidate_id, request.interview_date, request.interview_time):
            raise AppBaseException("Candidate already has an interview at this time", "INTERVIEW_CONFLICT", 400)
        if await self.interview_repo.find_interviewer_conflict(request.interviewer_id, request.interview_date, request.interview_time):
            raise AppBaseException("Interviewer already has an interview at this time", "INTERVIEWER_CONFLICT", 400)

        payload = {
            "candidate_id": candidate["_id"],
            "candidate_name": f"{candidate.get('first_name', '')} {candidate.get('last_name', '')}".strip(),
            "job_id": request.job_id,
            "job_title": job.get("jobTitle", ""),
            "interviewer_id": request.interviewer_id,
            "interviewer_name": interviewer.get("name", ""),
            "interview_date": request.interview_date,
            "interview_time": request.interview_time,
            "focus_tech_areas": request.focus_tech_areas,
            "status": CandidateStatus.INTERVIEW_SCHEDULED.value,
        }
        result = await self.interview_repo.create_interview(payload)
        await self.candidate_service.update_candidate_status(candidate["_id"], CandidateStatus.INTERVIEW_SCHEDULED.value, force_transition=True)
        logger.info("Interview scheduled successfully: %s", result.get("_id"))
        return result

    async def update_interview(self, interview_id: str, request: InterviewUpdateRequest) -> dict:
        """Update an existing interview schedule."""
        existing = await self.get_interview_by_id(interview_id)
        if existing.get("status") == CandidateStatus.INTERVIEW_COMPLETED.value:
            raise AppBaseException("Completed interviews cannot be edited", "INTERVIEW_COMPLETED", 400)
        update_data = request.model_dump(exclude_unset=True, by_alias=False)
        if not update_data:
            raise AppBaseException("No valid fields provided for update", "INVALID_UPDATE", 400)
        current_ist = datetime.now(self.ist_timezone)
        candidate_id = update_data.get("candidate_id", existing["candidate_id"])
        job_id = update_data.get("job_id", existing["job_id"])
        interviewer_id = update_data.get("interviewer_id", existing["interviewer_id"])
        if "candidate_id" in update_data or "job_id" in update_data or "interviewer_id" in update_data:
            await self._validate_references(candidate_id, job_id, interviewer_id)
        if await self.interview_repo.has_active_scheduled_interview(update_data.get("candidate_id", existing["candidate_id"]), exclude_id=interview_id):
            raise AppBaseException("Candidate already has an interview scheduled", "INTERVIEW_CONFLICT", 400)
        if "interview_date" in update_data and update_data["interview_date"] < current_ist.date():
            raise AppBaseException("Interview date cannot be in the past", "INVALID_INTERVIEW_DATE", 400)
        if "interview_date" in update_data and update_data["interview_date"] == current_ist.date():
            interview_time = update_data.get("interview_time", existing["interview_time"])
            if datetime.strptime(interview_time, "%H:%M").time() <= current_ist.time().replace(second=0, microsecond=0):
                raise AppBaseException("Interview time must be in the future", "INVALID_INTERVIEW_TIME", 400)
        interview_date_value = update_data.get("interview_date", existing["interview_date"])
        interview_time = update_data.get("interview_time", existing["interview_time"])
        scheduled_time = self._combine_interview_datetime(interview_date_value, interview_time)
        if scheduled_time and scheduled_time <= self._now_ist():
            raise AppBaseException("Interview time cannot be in the past.", "INVALID_INTERVIEW_TIME", 400)
        if await self.interview_repo.find_interviewer_conflict(interviewer_id, interview_date_value, interview_time, exclude_id=interview_id):
            raise AppBaseException("Interviewer already has an interview at this time", "INTERVIEWER_CONFLICT", 400)
        if "candidate_id" in update_data or "job_id" in update_data or "interviewer_id" in update_data:
            candidate_id = update_data.get("candidate_id", existing["candidate_id"])
            candidate = await self.interview_repo.get_candidate_by_id(candidate_id)
            job = await self.interview_repo.get_job_by_id(update_data.get("job_id", existing["job_id"]))
            interviewer = await self.interview_repo.get_user_by_id(update_data.get("interviewer_id", existing["interviewer_id"]))
            update_data["candidate_name"] = f"{candidate.get('first_name', '')} {candidate.get('last_name', '')}".strip()
            update_data["job_title"] = (job or {}).get("jobTitle", "")
            update_data["interviewer_name"] = (interviewer or {}).get("name", "")
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
        return await self._refresh_completed_status(interview_id, interview)

    async def get_interview_for_user(self, interview_id: str, current_user: dict) -> dict:
        """Return an interview with interviewer scoping enforced when required."""
        if get_user_role(current_user) == UserRole.INTERVIEWER:
            interviewer_id = str(current_user.get("_id") or current_user.get("id") or "")
            return await self.get_interview_for_interviewer(interview_id, interviewer_id)
        return await self.get_interview_by_id(interview_id)

    async def get_interview_for_interviewer(self, interview_id: str, interviewer_id: str) -> dict:
        """Return an interview only when it belongs to the logged-in interviewer."""
        await self._sync_overdue_interviews()
        interview = await self.interview_repo.get_interview_by_id_and_interviewer(interview_id, interviewer_id)
        if not interview:
            raise AppBaseException("Interview not found", "INTERVIEW_NOT_FOUND", 404)
        return await self._refresh_completed_status(interview_id, interview)

    async def get_all_interviews(self, search: str | None = None, page: int = 1, limit: int = 10) -> tuple[list, dict]:
        """Return interviews with optional server-side search."""
        await self._sync_overdue_interviews()
        query = await self._build_search_query(search)
        interviews, total_items = await self.interview_repo.get_all_interviews(query, page=page, limit=limit)
        interviews = [await self._refresh_completed_status(interview.get("_id"), interview) for interview in interviews]
        logger.info("Interview list retrieved successfully")
        return interviews, build_pagination_meta(page, limit, total_items)

    async def get_assigned_interviews(self, interviewer_id: str, search: str | None = None, page: int = 1, limit: int = 10) -> tuple[list, dict]:
        """Return interviews assigned to a specific interviewer."""
        query = await self._build_search_query(search)
        interviewer_filter = [interviewer_id, str(interviewer_id)]
        query["interviewer_id"] = {"$in": interviewer_filter}
        interviews, total_items = await self.interview_repo.get_all_interviews(query, page=page, limit=limit)
        interviews = [await self._refresh_completed_status(interview.get("_id"), interview) for interview in interviews]
        logger.info("Assigned interview list retrieved successfully for interviewer: %s", interviewer_id)
        return interviews, build_pagination_meta(page, limit, total_items)

    async def get_interviewers(self, search: str | None = None, page: int = 1, limit: int = 100) -> tuple[list, dict]:
        """Return interviewer users for interview assignment dropdowns."""
        from src.repositories.user_repository import UserRepository

        user_repo = UserRepository()
        search_term = normalize_search_term(search).lower()
        if search_term:
            users, total_items = await user_repo.search_users(search_term, page=page, limit=limit)
        else:
            users, total_items = await user_repo.get_all_users(page=page, limit=limit)
        interviewers = [user for user in users if get_user_role(user) == UserRole.INTERVIEWER]
        logger.info("Interviewer list retrieved successfully")
        return interviewers, build_pagination_meta(page, limit, len(interviewers) if search_term else total_items)

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
        if get_user_role(interviewer) != UserRole.INTERVIEWER:
            raise AppBaseException("Assigned interviewer must have INTERVIEWER role", "INVALID_INTERVIEWER_ROLE", 400)

    async def _build_search_query(self, search: str | None) -> dict:
        """Build the MongoDB query for interview search."""
        search_term = normalize_search_term(search)
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

    async def _refresh_completed_status(self, interview_id: str, interview: dict) -> dict:
        """Mark a scheduled interview completed once its IST time has passed."""
        if not interview:
            return interview
        if interview.get("status") != CandidateStatus.INTERVIEW_SCHEDULED.value:
            return interview

        interview_date = interview.get("interview_date")
        interview_time = interview.get("interview_time")
        if not interview_date or not interview_time:
            return interview

        current_ist = datetime.now(self.ist_timezone)
        scheduled_at = self._combine_interview_datetime(interview_date, interview_time)
        if not scheduled_at:
            return interview

        is_due = scheduled_at <= current_ist

        if not is_due:
            return interview

        updated_interview = await self.interview_repo.update_interview(interview_id, {"status": CandidateStatus.INTERVIEW_COMPLETED.value})
        if updated_interview:
            await self.candidate_service.update_candidate_status(updated_interview["candidate_id"], CandidateStatus.INTERVIEW_COMPLETED, force_transition=True)
        return updated_interview or interview

    def _combine_interview_datetime(self, interview_date, interview_time: str) -> datetime | None:
        """Build an IST-aware datetime from the stored interview date and time."""
        try:
            if isinstance(interview_date, datetime):
                interview_day = interview_date.astimezone(self.ist_timezone).date()
            elif isinstance(interview_date, date):
                interview_day = interview_date
            elif isinstance(interview_date, str):
                interview_day = datetime.fromisoformat(interview_date.replace("Z", "+00:00")).astimezone(self.ist_timezone).date()
            else:
                return None

            interview_clock = datetime.strptime(interview_time, "%H:%M").time()
            return datetime.combine(interview_day, interview_clock, tzinfo=self.ist_timezone)
        except Exception:
            logger.exception("Failed to combine interview date and time for automatic completion")
            return None

    def _now_ist(self) -> datetime:
        """Return the current IST datetime."""
        return datetime.now(self.ist_timezone)

    async def _sync_overdue_interviews(self) -> None:
        """Mark overdue interviews as completed before serving read requests."""
        completed_interviews = await self.interview_repo.complete_overdue_interviews(self._now_ist())
        for interview in completed_interviews:
            await self.candidate_service.update_candidate_status(interview["candidate_id"], CandidateStatus.INTERVIEW_COMPLETED.value, force_transition=True)
