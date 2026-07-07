"""Repository tests for interview feedback persistence."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.repositories.feedback_repository import FeedbackRepository


@pytest.fixture
def feedback_repository():
    db = MagicMock()
    db.__getitem__.side_effect = lambda key: {"interviews": MagicMock()}[key]
    with patch("src.repositories.feedback_repository.get_database", return_value=db):
        repo = FeedbackRepository()
        repo.collection.find_one = AsyncMock()
        repo.collection.update_one = AsyncMock()
        yield repo


@pytest.mark.asyncio
class TestFeedbackRepository:
    async def test_feedback_exists_false(self, feedback_repository):
        feedback_repository.collection.find_one.return_value = None
        assert await feedback_repository.feedback_exists("int1") is False

