"""Repository tests for job persistence workflows."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.repositories.job_repository import JobRepository


@pytest.fixture
def job_repository():
    db = MagicMock()
    db.__getitem__.side_effect = lambda key: {"jobs": MagicMock()}[key]
    with patch("src.repositories.job_repository.get_database", return_value=db):
        repo = JobRepository()
        repo.collection.insert_one = AsyncMock()
        repo.collection.update_one = AsyncMock()
        repo.collection.find_one = AsyncMock()
        repo.collection.count_documents = AsyncMock()
        repo.collection.find.return_value.sort.return_value.skip.return_value.limit.return_value = MagicMock()
        yield repo


@pytest.mark.asyncio
class TestJobRepository:
    async def test_normalize_helpers(self, job_repository):
        normalized = job_repository._normalize_job({"_id": 1, "experienceRequired": 2, "requiredSkills": ["Python"]})
        assert normalized["_id"] == "1"
        assert job_repository._build_job_query(None) == {}

    async def test_create_get_update_and_list(self, job_repository):
        job_repository.collection.insert_one.return_value = MagicMock(inserted_id="job1")
        created = await job_repository.create_job({"jobTitle": "Backend"})
        assert created["_id"] == "job1"

        job_repository.collection.find_one.return_value = {"_id": MagicMock(), "jobTitle": "Backend", "experienceRequired": 2}
        found = await job_repository.get_job_by_id("507f1f77bcf86cd799439011")
        assert found["jobTitle"] == "Backend"

        job_repository.collection.count_documents.return_value = 1
        job_repository.collection.find.return_value.sort.return_value.skip.return_value.limit.return_value.__aiter__.return_value = [
            {"_id": MagicMock(), "jobTitle": "Backend", "experienceRequired": 2}
        ]
        jobs, total = await job_repository.get_all_jobs()
        assert total == 1 and jobs[0]["jobTitle"] == "Backend"

        job_repository.collection.update_one.return_value = MagicMock()
        job_repository.collection.find_one.return_value = {"_id": MagicMock(), "jobTitle": "Updated"}
        updated = await job_repository.update_job("507f1f77bcf86cd799439011", {"jobTitle": "Updated"})
        assert updated["jobTitle"] == "Updated"

    async def test_invalid_job_id_and_error_path(self, job_repository):
        assert await job_repository.get_job_by_id("bad") is None
        assert await job_repository.update_job("bad", {}) is None
        job_repository.collection.find_one.return_value = None
        assert await job_repository.get_job_by_id("507f1f77bcf86cd799439011") is None
        job_repository.collection.update_one.return_value = MagicMock()
        job_repository.collection.find_one.return_value = {"_id": MagicMock(), "jobTitle": "Updated"}
        updated = await job_repository.update_job("507f1f77bcf86cd799439011", {"jobTitle": "Updated"})
        assert updated["jobTitle"] == "Updated"
        job_repository.collection.find_one.side_effect = Exception("boom")
        with pytest.raises(Exception):
            await job_repository.get_job_by_id("507f1f77bcf86cd799439011")
