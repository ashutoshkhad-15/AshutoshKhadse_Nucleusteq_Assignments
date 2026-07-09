"""Repository layer for dashboard statistics and aggregation queries."""

import logging

from src.constants.interview_constants import InterviewConstants
from src.core.database import get_database

logger = logging.getLogger(__name__)


class DashboardRepository:
    """Provide aggregation queries for dashboard statistics."""

    def __init__(self):
        """Initialize the repository with active MongoDB collections."""
        self.db = get_database()
        self.jobs = self.db["jobs"]
        self.candidates = self.db["candidates"]
        self.interviews = self.db[InterviewConstants.INTERVIEW_COLLECTION]

    async def get_hr_dashboard_stats(self) -> dict:
        """Aggregate the HR dashboard statistics."""
        try:
            stats = {
                "total_jobs": await self.jobs.count_documents({}),
                "total_candidates": await self.candidates.count_documents({}),
                "scheduled_interviews": await self.interviews.count_documents({"status": "SCHEDULED"}),
                "selected_candidates": await self.candidates.count_documents({"status": "SELECTED"}),
                "rejected_candidates": await self.candidates.count_documents({"status": "REJECTED"}),
            }
            logger.info("HR dashboard statistics retrieved successfully")
            return stats
        except Exception:
            logger.exception("Repository failure while fetching HR dashboard statistics")
            raise

    async def get_interviewer_dashboard_stats(self, interviewer_id: str) -> dict:
        """Aggregate interviewer dashboard statistics."""
        try:
            stats = {
                "assigned_interviews": await self.interviews.count_documents({"interviewer_id": interviewer_id}),
                "pending_feedback": await self.interviews.count_documents({"interviewer_id": interviewer_id, "feedback": {"$exists": False}}),
                "completed_feedback": await self.interviews.count_documents({"interviewer_id": interviewer_id, "feedback": {"$exists": True}}),
            }
            logger.info("Interviewer dashboard statistics retrieved successfully for interviewer: %s", interviewer_id)
            return stats
        except Exception:
            logger.exception("Repository failure while fetching interviewer dashboard statistics for interviewer: %s", interviewer_id)
            raise
