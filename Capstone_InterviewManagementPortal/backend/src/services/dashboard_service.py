"""Service layer for dashboard aggregation workflows."""

import logging

from src.repositories.dashboard_repository import DashboardRepository

logger = logging.getLogger(__name__)


class DashboardService:
    """Coordinate dashboard statistics and response formatting."""

    def __init__(self):
        """Initialize the service with the dashboard repository dependency."""
        self.dashboard_repo = DashboardRepository()

    async def get_hr_dashboard(self) -> dict:
        """Return HR dashboard statistics."""
        logger.info("Retrieving HR dashboard statistics")
        return await self.dashboard_repo.get_hr_dashboard_stats()

    async def get_admin_dashboard(self) -> dict:
        """Return admin dashboard statistics."""
        return await self.get_hr_dashboard()

    async def get_interviewer_dashboard(self, interviewer_id: str) -> dict:
        """Return interviewer dashboard statistics."""
        logger.info("Retrieving interviewer dashboard statistics")
        return await self.dashboard_repo.get_interviewer_dashboard_stats(interviewer_id)
