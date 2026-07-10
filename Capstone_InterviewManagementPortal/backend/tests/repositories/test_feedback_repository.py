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
    async def test_get_feedback_by_interview_id_invalid(self, feedback_repository):
        assert await feedback_repository.get_feedback_by_interview_id("bad-id") is None

    async def test_get_feedback_by_interview_id_success(self, feedback_repository):
        feedback_repository.collection.find_one.return_value = {
            "_id": MagicMock(),
            "feedback": {"comments": "good"},
            "feedback_by": MagicMock(),
        }
        result = await feedback_repository.get_feedback_by_interview_id("507f1f77bcf86cd799439011")
        assert result["feedback"] == {"comments": "good"}

    async def test_feedback_exists_true_and_false(self, feedback_repository):
        feedback_repository.collection.find_one.return_value = {
            "_id": MagicMock(),
            "feedback": {"comments": "good"},
        }
        assert await feedback_repository.feedback_exists("507f1f77bcf86cd799439011") is True
        feedback_repository.collection.find_one.return_value = {
            "_id": MagicMock(),
            "feedback": None,
        }
        assert await feedback_repository.feedback_exists("507f1f77bcf86cd799439011") is False

    async def test_submit_feedback_invalid_and_missing_and_success(self, feedback_repository):
        assert await feedback_repository.submit_feedback("bad-id", {}) is None

        feedback_repository.collection.update_one.return_value = MagicMock(matched_count=0)
        assert await feedback_repository.submit_feedback("507f1f77bcf86cd799439011", {"feedback": {"comments": "ok"}}) is None

        feedback_repository.collection.update_one.return_value = MagicMock(matched_count=1)
        feedback_repository.collection.find_one.return_value = {"_id": MagicMock(), "feedback": {"comments": "ok"}}
        result = await feedback_repository.submit_feedback("507f1f77bcf86cd799439011", {"feedback": {"comments": "ok"}})
        assert result["feedback"]["comments"] == "ok"
