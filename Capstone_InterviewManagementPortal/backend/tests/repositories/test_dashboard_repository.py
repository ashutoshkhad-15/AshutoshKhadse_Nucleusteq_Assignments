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
        assert result["total_jobs"] == 1
