"""Service tests for dashboard aggregation workflows."""

from unittest.mock import AsyncMock, patch

import pytest

from src.services.dashboard_service import DashboardService


@pytest.fixture
def dashboard_service():
    with patch("src.services.dashboard_service.DashboardRepository") as mock_repo_class, \
         patch("src.services.dashboard_service.InterviewService") as mock_interview_class:
        repo = mock_repo_class.return_value
        repo.get_hr_dashboard_stats = AsyncMock()
        repo.get_interviewer_dashboard_stats = AsyncMock()
        interview_service = mock_interview_class.return_value
        interview_service.get_interview_by_id = AsyncMock()
        service = DashboardService()
        service.dashboard_repo = repo
        service.interview_service = interview_service
        yield service


@pytest.mark.asyncio
class TestDashboardService:
    async def test_hr_dashboard(self, dashboard_service):
        dashboard_service.dashboard_repo.get_hr_dashboard_stats.return_value = {"total_jobs": 1}
        result = await dashboard_service.get_hr_dashboard()
        assert result["total_jobs"] == 1

    async def test_admin_dashboard(self, dashboard_service):
        dashboard_service.dashboard_repo.get_hr_dashboard_stats.return_value = {"total_jobs": 1}
        result = await dashboard_service.get_admin_dashboard()
        assert result["total_jobs"] == 1

    async def test_interviewer_dashboard(self, dashboard_service):
        dashboard_service.dashboard_repo.get_interviewer_dashboard_stats.return_value = {"assigned_interviews": 2}
        result = await dashboard_service.get_interviewer_dashboard("usr1")
        assert result["assigned_interviews"] == 2
