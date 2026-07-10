"""Repository layer for interview scheduling and feedback persistence."""

import logging
from datetime import date, datetime, time, timezone

from bson.objectid import ObjectId

from src.constants.interview_constants import InterviewConstants
from src.core.database import get_database

logger = logging.getLogger(__name__)


class InterviewRepository:
    """Provide MongoDB data access operations for interviews."""

    def __init__(self):
        """Initialize the repository with active MongoDB collections."""
        self.db = get_database()
        self.collection = self.db[InterviewConstants.INTERVIEW_COLLECTION]
        self.candidates = self.db["candidates"]
        self.jobs = self.db["jobs"]
        self.users = self.db["users"]

    @staticmethod
    def _normalize_interview_date(value):
        """Convert date values into a BSON-safe UTC datetime."""
        if isinstance(value, date) and not isinstance(value, datetime):
            return datetime.combine(value, time.min, tzinfo=timezone.utc)
        return value

    @staticmethod
    def _normalize_object_id(value):
        """Convert valid string identifiers into ObjectId values."""
        if isinstance(value, str) and ObjectId.is_valid(value):
            return ObjectId(value)
        return value

    @staticmethod
    def _serialize(document: dict | None) -> dict | None:
        """Return a JSON-friendly interview document."""
        if not document:
            return document
        serialized = dict(document)
        serialized["_id"] = str(serialized["_id"])
        if isinstance(serialized.get("interview_date"), datetime):
            serialized["interview_date"] = serialized["interview_date"].date().isoformat()
        elif isinstance(serialized.get("interview_date"), date):
            serialized["interview_date"] = serialized["interview_date"].isoformat()
        for field in ("created_at", "updated_at", "feedback_submitted_at"):
            if isinstance(serialized.get(field), datetime):
                serialized[field] = serialized[field].isoformat()
        for field in ("candidate_id", "job_id", "interviewer_id", "feedback_by"):
            if serialized.get(field) is not None:
                serialized[field] = str(serialized[field])
        return serialized

    async def create_interview(self, interview_data: dict) -> dict:
        """Insert a new interview document."""
        try:
            interview_data = dict(interview_data)
            for field in ("candidate_id", "job_id", "interviewer_id"):
                interview_data[field] = self._normalize_object_id(interview_data.get(field))
            interview_data["interview_date"] = self._normalize_interview_date(interview_data.get("interview_date"))
            interview_data["created_at"] = datetime.now(timezone.utc)
            interview_data["updated_at"] = datetime.now(timezone.utc)
            result = await self.collection.insert_one(interview_data)
            interview_data["_id"] = result.inserted_id
            logger.info("Interview created successfully")
            return self._serialize(interview_data)
        except Exception:
            logger.exception("Repository failure while creating interview")
            raise

    async def update_interview(self, interview_id: str, update_data: dict) -> dict | None:
        """Apply a partial interview update."""
        if not ObjectId.is_valid(interview_id):
            logger.warning("Invalid interview ID provided for update: %s", interview_id)
            return None
        try:
            update_data = dict(update_data)
            for field in ("candidate_id", "job_id", "interviewer_id"):
                if field in update_data:
                    update_data[field] = self._normalize_object_id(update_data.get(field))
            if "interview_date" in update_data:
                update_data["interview_date"] = self._normalize_interview_date(update_data.get("interview_date"))
            update_data["updated_at"] = datetime.now(timezone.utc)
            result = await self.collection.update_one({"_id": ObjectId(interview_id)}, {"$set": update_data})
            if result.matched_count == 0:
                logger.warning("Interview not found for update: %s", interview_id)
                return None
            logger.info("Interview updated successfully: %s", interview_id)
            return await self.get_interview_by_id(interview_id)
        except Exception:
            logger.exception("Repository failure while updating interview: %s", interview_id)
            raise

    async def get_interview_by_id(self, interview_id: str) -> dict | None:
        """Fetch an interview by identifier."""
        if not ObjectId.is_valid(interview_id):
            logger.warning("Invalid interview ID provided: %s", interview_id)
            return None
        try:
            document = await self.collection.find_one({"_id": ObjectId(interview_id)})
            if not document:
                logger.warning("Interview not found for ID: %s", interview_id)
            return self._serialize(document)
        except Exception:
            logger.exception("Repository failure while fetching interview by ID: %s", interview_id)
            raise

    async def get_interview_by_id_and_interviewer(self, interview_id: str, interviewer_id: str) -> dict | None:
        """Fetch an interview by identifier only when assigned to the interviewer."""
        if not ObjectId.is_valid(interview_id):
            logger.warning("Invalid interview ID provided for interviewer lookup: %s", interview_id)
            return None
        try:
            interviewer_filter = [interviewer_id]
            normalized_interviewer_id = self._normalize_object_id(interviewer_id)
            if normalized_interviewer_id is not None:
                interviewer_filter.append(normalized_interviewer_id)
            document = await self.collection.find_one({
                "_id": ObjectId(interview_id),
                "interviewer_id": {"$in": interviewer_filter},
            })
            if not document:
                logger.warning("Interview not found for interviewer lookup: %s", interview_id)
            return self._serialize(document)
        except Exception:
            logger.exception("Repository failure while fetching interview for interviewer: %s", interview_id)
            raise

    async def get_all_interviews(self, query: dict | None = None, page: int = 1, limit: int = 10) -> tuple[list[dict], int]:
        """Return interview documents ordered newest-first."""
        try:
            normalized_query = query or {}
            total_items = await self.collection.count_documents(normalized_query)
            cursor = self.collection.find(normalized_query).sort("created_at", -1).skip((page - 1) * limit).limit(limit)
            interviews: list[dict] = []
            async for document in cursor:
                interviews.append(self._serialize(document))
            logger.info("Interview list retrieved successfully")
            return interviews, total_items
        except Exception:
            logger.exception("Repository failure while fetching interview list")
            raise

    async def complete_overdue_interviews(self, current_time: datetime) -> list[dict]:
        """Mark overdue scheduled interviews as completed."""
        try:
            cursor = self.collection.find({"status": "INTERVIEW_SCHEDULED"})
            updates: list[dict] = []
            async for document in cursor:
                interview_date = document.get("interview_date")
                interview_time = document.get("interview_time")
                scheduled_at = self._combine_interview_datetime(interview_date, interview_time, current_time.tzinfo)
                if not scheduled_at or scheduled_at > current_time:
                    continue
                result = await self.collection.update_one(
                    {"_id": document["_id"]},
                    {"$set": {"status": "INTERVIEW_COMPLETED", "updated_at": datetime.now(timezone.utc)}},
                )
                if result.modified_count:
                    updates.append(self._serialize(await self.collection.find_one({"_id": document["_id"]})))
            return updates
        except Exception:
            logger.exception("Repository failure while completing overdue interviews")
            raise

    def _combine_interview_datetime(self, interview_date, interview_time: str, tzinfo=timezone.utc) -> datetime | None:
        """Build a timezone-aware datetime from the stored interview date and time."""
        try:
            if isinstance(interview_date, datetime):
                interview_day = interview_date.date()
            elif isinstance(interview_date, date):
                interview_day = interview_date
            elif isinstance(interview_date, str):
                interview_day = datetime.fromisoformat(interview_date.replace("Z", "+00:00")).date()
            else:
                return None
            interview_clock = datetime.strptime(interview_time, "%H:%M").time()
            return datetime.combine(interview_day, interview_clock, tzinfo=tzinfo)
        except Exception:
            logger.exception("Failed to combine interview date and time in repository")
            return None

    async def find_overlapping_interview(self, candidate_id: str, interview_date, interview_time: str, exclude_id: str | None = None) -> dict | None:
        """Find an interview scheduled for the same candidate slot."""
        try:
            query = {
                "candidate_id": self._normalize_object_id(candidate_id),
                "interview_date": self._normalize_interview_date(interview_date),
                "interview_time": interview_time,
            }
            if exclude_id:
                query["_id"] = {"$ne": ObjectId(exclude_id)} if ObjectId.is_valid(exclude_id) else {"$ne": exclude_id}
            return self._serialize(await self.collection.find_one(query))
        except Exception:
            logger.exception("Repository failure while checking overlapping interview for candidate: %s", candidate_id)
            raise

    async def has_active_scheduled_interview(self, candidate_id: str, exclude_id: str | None = None) -> bool:
        """Return whether the candidate already has a scheduled interview."""
        try:
            candidate_filter = [candidate_id]
            normalized_candidate_id = self._normalize_object_id(candidate_id)
            if normalized_candidate_id is not None:
                candidate_filter.append(normalized_candidate_id)
            query = {"candidate_id": {"$in": candidate_filter}, "status": "INTERVIEW_SCHEDULED"}
            if exclude_id:
                query["_id"] = {"$ne": ObjectId(exclude_id)} if ObjectId.is_valid(exclude_id) else {"$ne": exclude_id}
            return await self.collection.count_documents(query) > 0
        except Exception:
            logger.exception("Repository failure while checking active interview for candidate: %s", candidate_id)
            raise

    async def has_scheduled_interviews_for_interviewer(self, interviewer_id: str) -> bool:
        """Return whether the interviewer has any currently scheduled interviews."""
        try:
            interviewer_filter = [interviewer_id]
            normalized_interviewer_id = self._normalize_object_id(interviewer_id)
            if normalized_interviewer_id is not None:
                interviewer_filter.append(normalized_interviewer_id)
            return await self.collection.count_documents({
                "interviewer_id": {"$in": interviewer_filter},
                "status": "INTERVIEW_SCHEDULED",
            }) > 0
        except Exception:
            logger.exception("Repository failure while checking scheduled interviews for interviewer: %s", interviewer_id)
            raise

    async def find_interviewer_conflict(self, interviewer_id: str, interview_date, interview_time: str, exclude_id: str | None = None) -> dict | None:
        """Find a scheduled interview already assigned to the interviewer at the same slot."""
        try:
            query = {
                "interviewer_id": self._normalize_object_id(interviewer_id),
                "status": "INTERVIEW_SCHEDULED",
                "interview_date": self._normalize_interview_date(interview_date),
                "interview_time": interview_time,
            }
            if exclude_id:
                query["_id"] = {"$ne": ObjectId(exclude_id)} if ObjectId.is_valid(exclude_id) else {"$ne": exclude_id}
            return self._serialize(await self.collection.find_one(query))
        except Exception:
            logger.exception("Repository failure while checking overlapping interview for interviewer: %s", interviewer_id)
            raise

    async def get_interview_by_candidate(self, candidate_id: str) -> dict | None:
        """Fetch the latest interview for a candidate."""
        try:
            document = await self.collection.find_one({"candidate_id": self._normalize_object_id(candidate_id)}, sort=[("created_at", -1)])
            return self._serialize(document)
        except Exception:
            logger.exception("Repository failure while fetching interview by candidate: %s", candidate_id)
            raise

    async def get_candidate_by_id(self, candidate_id: str) -> dict | None:
        """Fetch a candidate for validation and dashboard lookups."""
        try:
            object_id = self._normalize_object_id(candidate_id)
            if not object_id:
                return None
            candidate = await self.candidates.find_one({"_id": object_id})
            if candidate:
                candidate["_id"] = str(candidate["_id"])
            return candidate
        except Exception:
            logger.exception("Repository failure while fetching candidate by ID: %s", candidate_id)
            raise

    async def get_job_by_id(self, job_id: str) -> dict | None:
        """Fetch a job for validation and dashboard lookups."""
        try:
            object_id = self._normalize_object_id(job_id)
            if not object_id:
                return None
            job = await self.jobs.find_one({"_id": object_id})
            if job:
                job["_id"] = str(job["_id"])
            return job
        except Exception:
            logger.exception("Repository failure while fetching job by ID: %s", job_id)
            raise

    async def get_user_by_id(self, user_id: str) -> dict | None:
        """Fetch a user for interviewer validation and dashboard lookups."""
        try:
            object_id = self._normalize_object_id(user_id)
            if not object_id:
                return None
            user = await self.users.find_one({"_id": object_id})
            if user:
                user["_id"] = str(user["_id"])
            return user
        except Exception:
            logger.exception("Repository failure while fetching user by ID: %s", user_id)
            raise

    async def submit_feedback(self, interview_id: str, feedback_data: dict) -> dict | None:
        """Store feedback on an existing interview."""
        if not ObjectId.is_valid(interview_id):
            logger.warning("Invalid interview ID provided for feedback submission: %s", interview_id)
            return None
        try:
            feedback_data = dict(feedback_data)
            feedback_data["feedback_submitted_at"] = datetime.now(timezone.utc)
            result = await self.collection.update_one({"_id": ObjectId(interview_id)}, {"$set": feedback_data})
            if result.matched_count == 0:
                logger.warning("Interview not found for feedback submission: %s", interview_id)
                return None
            logger.info("Feedback stored successfully for interview: %s", interview_id)
            return await self.get_interview_by_id(interview_id)
        except Exception:
            logger.exception("Repository failure while storing feedback for interview: %s", interview_id)
            raise

    async def get_feedback_by_interview_id(self, interview_id: str) -> dict | None:
        """Fetch stored feedback for a given interview."""
        return await self.get_interview_by_id(interview_id)

    async def get_hr_dashboard_stats(self) -> dict:
        """Aggregate the HR dashboard statistics."""
        total_jobs = await self.jobs.count_documents({})
        total_candidates = await self.candidates.count_documents({})
        scheduled_interviews = await self.collection.count_documents({})
        selected_candidates = await self.candidates.count_documents({"status": "SELECTED"})
        rejected_candidates = await self.candidates.count_documents({"status": "REJECTED"})
        return {
            "total_jobs": total_jobs,
            "total_candidates": total_candidates,
            "scheduled_interviews": scheduled_interviews,
            "selected_candidates": selected_candidates,
            "rejected_candidates": rejected_candidates,
        }

    async def get_interviewer_dashboard_stats(self, interviewer_id: str) -> dict:
        """Aggregate interviewer dashboard statistics."""
        interviewer_object_id = self._normalize_object_id(interviewer_id)
        assigned_filter = {"$in": [interviewer_object_id, str(interviewer_id)]}
        assigned_interviews = await self.collection.count_documents({"interviewer_id": assigned_filter})
        pending_feedback = await self.collection.count_documents({"interviewer_id": assigned_filter, "feedback": {"$exists": False}})
        completed_feedback = await self.collection.count_documents({"interviewer_id": assigned_filter, "feedback": {"$exists": True}})
        return {
            "assigned_interviews": assigned_interviews,
            "pending_feedback": pending_feedback,
            "completed_feedback": completed_feedback,
        }
