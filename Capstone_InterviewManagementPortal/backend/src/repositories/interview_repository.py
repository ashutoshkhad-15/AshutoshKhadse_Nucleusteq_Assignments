"""Repository layer for interview scheduling and feedback persistence."""

import logging
from datetime import date, datetime, timezone

from bson.objectid import ObjectId

from src.core.database import get_database

logger = logging.getLogger(__name__)


class InterviewRepository:
    """Provide MongoDB data access operations for interviews."""

    def __init__(self):
        """Initialize the repository with active MongoDB collections."""
        self.db = get_database()
        self.collection = self.db["interviews"]
        self.candidates = self.db["candidates"]
        self.jobs = self.db["jobs"]
        self.users = self.db["users"]

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
            document = await self.collection.find_one({
                "_id": ObjectId(interview_id),
                "interviewer_id": interviewer_id,
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
            query = {
                "status": "SCHEDULED",
                "interview_date": {"$lte": current_time},
            }
            cursor = self.collection.find(query)
            updates: list[dict] = []
            async for document in cursor:
                result = await self.collection.update_one(
                    {"_id": document["_id"]},
                    {"$set": {"status": "COMPLETED", "updated_at": datetime.now(timezone.utc)}},
                )
                if result.modified_count:
                    updates.append(self._serialize(await self.collection.find_one({"_id": document["_id"]})))
            return updates
        except Exception:
            logger.exception("Repository failure while completing overdue interviews")
            raise

    async def find_overlapping_interview(self, candidate_id: str, interview_date, interview_time: str, exclude_id: str | None = None) -> dict | None:
        """Find an interview scheduled for the same candidate slot."""
        try:
            query = {
                "candidate_id": candidate_id,
                "interview_date": interview_date,
                "interview_time": interview_time,
            }
            if exclude_id:
                query["_id"] = {"$ne": ObjectId(exclude_id)} if ObjectId.is_valid(exclude_id) else {"$ne": exclude_id}
            return self._serialize(await self.collection.find_one(query))
        except Exception:
            logger.exception("Repository failure while checking overlapping interview for candidate: %s", candidate_id)
            raise

    async def get_interview_by_candidate(self, candidate_id: str) -> dict | None:
        """Fetch the latest interview for a candidate."""
        try:
            document = await self.collection.find_one({"candidate_id": candidate_id}, sort=[("created_at", -1)])
            return self._serialize(document)
        except Exception:
            logger.exception("Repository failure while fetching interview by candidate: %s", candidate_id)
            raise

    async def get_candidate_by_id(self, candidate_id: str) -> dict | None:
        """Fetch a candidate for validation and dashboard lookups."""
        try:
            candidate = await self.candidates.find_one({"_id": candidate_id})
            if candidate:
                candidate["_id"] = str(candidate["_id"])
            return candidate
        except Exception:
            logger.exception("Repository failure while fetching candidate by ID: %s", candidate_id)
            raise

    async def get_job_by_id(self, job_id: str) -> dict | None:
        """Fetch a job for validation and dashboard lookups."""
        try:
            job = await self.jobs.find_one({"_id": job_id})
            if job:
                job["_id"] = str(job["_id"])
            return job
        except Exception:
            logger.exception("Repository failure while fetching job by ID: %s", job_id)
            raise

    async def get_user_by_id(self, user_id: str) -> dict | None:
        """Fetch a user for interviewer validation and dashboard lookups."""
        try:
            user = await self.users.find_one({"_id": user_id})
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
        assigned_interviews = await self.collection.count_documents({"interviewer_id": interviewer_id})
        pending_feedback = await self.collection.count_documents({"interviewer_id": interviewer_id, "feedback": {"$exists": False}})
        completed_feedback = await self.collection.count_documents({"interviewer_id": interviewer_id, "feedback": {"$exists": True}})
        return {
            "assigned_interviews": assigned_interviews,
            "pending_feedback": pending_feedback,
            "completed_feedback": completed_feedback,
        }
