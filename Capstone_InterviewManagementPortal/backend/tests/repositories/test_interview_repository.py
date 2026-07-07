"""Repository tests for interview persistence workflows."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.repositories.interview_repository import InterviewRepository


@pytest.fixture
def interview_repository():
    db = MagicMock()
    db.__getitem__.side_effect = lambda key: {
        "interviews": MagicMock(),
        "candidates": MagicMock(),
        "jobs": MagicMock(),
        "users": MagicMock(),
    }[key]
    with patch("src.repositories.interview_repository.get_database", return_value=db):
        repo = InterviewRepository()
        repo.collection.insert_one = AsyncMock()
        repo.collection.update_one = AsyncMock()
        repo.collection.find_one = AsyncMock()
        repo.collection.count_documents = AsyncMock()
        repo.collection.find.return_value.sort.return_value.skip.return_value.limit.return_value = MagicMock()
        yield repo


@pytest.mark.asyncio
class TestInterviewRepository:
    async def test_create_interview(self, interview_repository):
        interview_repository.collection.insert_one.return_value = MagicMock(inserted_id="int1")
        result = await interview_repository.create_interview({"candidate_id": "cand1"})
        assert result["_id"] == "int1"

