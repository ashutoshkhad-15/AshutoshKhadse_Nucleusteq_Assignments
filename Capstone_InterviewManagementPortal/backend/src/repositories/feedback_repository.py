"""Repository layer for interview feedback persistence."""

import logging

from bson.objectid import ObjectId

from src.constants.interview_constants import InterviewConstants
from src.core.database import get_database

logger = logging.getLogger(__name__)


class FeedbackRepository:
    """Provide MongoDB data access operations for feedback."""

    def __init__(self):
        """Initialize the repository with active MongoDB collections."""
        self.db = get_database()
        self.collection = self.db[InterviewConstants.INTERVIEW_COLLECTION]

    @staticmethod
    def _serialize(document: dict | None) -> dict | None:
        """Return a JSON-friendly feedback document."""
        if not document:
            return document
        serialized = dict(document)
        serialized["_id"] = str(serialized["_id"])
        for field in ("candidate_id", "job_id", "interviewer_id", "feedback_by"):
            if serialized.get(field) is not None:
                serialized[field] = str(serialized[field])
        return serialized

    async def get_feedback_by_interview_id(self, interview_id: str) -> dict | None:
        """Fetch feedback for an interview."""
        if not ObjectId.is_valid(interview_id):
            logger.warning("Invalid interview ID provided for feedback lookup: %s", interview_id)
            return None
        try:
            document = await self.collection.find_one(
                {"_id": ObjectId(interview_id)},
                {"feedback": 1, "feedback_by": 1, "feedback_submitted_at": 1},
            )
            return self._serialize(document)
        except Exception:
            logger.exception("Repository failure while fetching feedback for interview: %s", interview_id)
            raise

    async def feedback_exists(self, interview_id: str) -> bool:
        """Return whether feedback already exists for an interview."""
        feedback = await self.get_feedback_by_interview_id(interview_id)
        exists = bool(feedback and feedback.get("feedback"))
        logger.info("Feedback existence checked for interview: %s", interview_id)
        return exists

    async def submit_feedback(self, interview_id: str, feedback_data: dict) -> dict | None:
        """Store feedback for an interview."""
        if not ObjectId.is_valid(interview_id):
            logger.warning("Invalid interview ID provided for feedback submission: %s", interview_id)
            return None
        try:
            result = await self.collection.update_one({"_id": ObjectId(interview_id)}, {"$set": feedback_data})
            if result.matched_count == 0:
                logger.warning("Feedback submission target not found for interview: %s", interview_id)
                return None
            logger.info("Feedback stored successfully for interview: %s", interview_id)
            return await self.get_feedback_by_interview_id(interview_id)
        except Exception:
            logger.exception("Repository failure while submitting feedback for interview: %s", interview_id)
            raise
