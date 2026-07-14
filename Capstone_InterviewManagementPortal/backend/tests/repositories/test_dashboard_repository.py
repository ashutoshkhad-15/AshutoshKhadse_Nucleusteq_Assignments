"""Repository tests for dashboard aggregation queries."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.repositories.dashboard_repository import DashboardRepository


@pytest.fixture
def dashboard_repository():
    db = MagicMock()
    db.__getitem__.side_effect = lambda key: {
        "jobs": MagicMock(),
        "candidates": MagicMock(),
        "interviews": MagicMock(),
    }[key]
    with patch("src.repositories.dashboard_repository.get_database", return_value=db):
        repo = DashboardRepository()
        repo.jobs.count_documents = AsyncMock(return_value=1)
        repo.candidates.count_documents = AsyncMock(return_value=2)
        repo.interviews.count_documents = AsyncMock(return_value=3)
        yield repo


@pytest.mark.asyncio
class TestDashboardRepository:
    async def test_hr_dashboard_stats(self, dashboard_repository):
        result = await dashboard_repository.get_hr_dashboard_stats()
        assert result == {
            "total_jobs": 1,
            "total_candidates": 2,
            "scheduled_interviews": 3,
            "selected_candidates": 2,
            "rejected_candidates": 2,
        }

    async def test_interviewer_dashboard_stats_with_object_id(self, dashboard_repository):
        dashboard_repository.interviews.count_documents = AsyncMock(side_effect=[4, 1, 3])
        result = await dashboard_repository.get_interviewer_dashboard_stats("507f1f77bcf86cd799439011")
        assert result == {
            "assigned_interviews": 4,
            "pending_feedback": 1,
            "completed_feedback": 3,
        }

    async def test_hr_dashboard_stats_error_propagates(self, dashboard_repository):
        dashboard_repository.jobs.count_documents = AsyncMock(side_effect=Exception("boom"))
        with pytest.raises(Exception):
            await dashboard_repository.get_hr_dashboard_stats()
