"""Repository tests for candidate persistence and resume storage."""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.repositories.candidate_repository import CandidateRepository


@pytest.fixture
def candidate_repository():
    db = MagicMock()
    db.__getitem__.side_effect = lambda key: {
        "candidates": MagicMock(),
        "jobs": MagicMock(),
        "candidate_resumes": MagicMock(),
        "candidate_status_history": MagicMock(),
    }[key]
    with patch("src.repositories.candidate_repository.get_database", return_value=db):
        repo = CandidateRepository()
        repo.collection.insert_one = AsyncMock()
        repo.collection.find_one = AsyncMock()
        repo.collection.update_one = AsyncMock()
        repo.collection.count_documents = AsyncMock()
        repo.collection.find.return_value.sort.return_value.skip.return_value.limit.return_value = MagicMock()
        repo.job_collection.find_one = AsyncMock()
        repo.job_collection.find.return_value = MagicMock()
        repo.resume_collection.find_one = AsyncMock()
        repo.resume_collection.update_one = AsyncMock()
        repo.resume_collection.insert_one = AsyncMock()
        repo.resume_collection.create_index = AsyncMock()
        repo.status_history_collection.insert_one = AsyncMock()
        repo.status_history_collection.find.return_value.sort.return_value = MagicMock()
        yield repo


@pytest.mark.asyncio
class TestCandidateRepository:
    async def test_serialize_helpers_and_indexes(self, candidate_repository):
        assert candidate_repository._serialize_doc(None) is None
        assert candidate_repository._serialize_resume_document(None) is None
        assert candidate_repository._serialize_status_history(None) is None
        candidate_repository.collection.create_index = AsyncMock()
        candidate_repository.resume_collection.create_index = AsyncMock()
        candidate_repository.status_history_collection.create_index = AsyncMock()
        candidate_repository.job_collection.create_index = AsyncMock()
        await candidate_repository.ensure_indexes()
        assert candidate_repository.collection.create_index.await_count == 5

    async def test_create_and_get_candidate(self, candidate_repository):
        candidate_repository.collection.insert_one.return_value = MagicMock(inserted_id="cand1")
        candidate_repository.job_collection.find_one.return_value = None
        created = await candidate_repository.create_candidate({"first_name": "Ashutosh", "applied_job_id": "job1"})
        assert created["_id"] == "cand1"

        candidate_repository.collection.find_one.return_value = {"_id": MagicMock(), "first_name": "Ashutosh"}
        found = await candidate_repository.get_candidate_by_id("507f1f77bcf86cd799439011")
        assert found["first_name"] == "Ashutosh"

    async def test_list_update_and_search(self, candidate_repository):
        candidate_repository.collection.count_documents.return_value = 1
        candidate_repository.collection.find.return_value.sort.return_value.skip.return_value.limit.return_value = MagicMock()
        candidate_repository.collection.find.return_value.sort.return_value.skip.return_value.limit.return_value.__aiter__.return_value = []
        candidates, total = await candidate_repository.get_all_candidates()
        assert total == 1
        assert candidates == []

        candidate_repository.collection.update_one.return_value = MagicMock(matched_count=1)
        candidate_repository.collection.find_one.return_value = {"_id": MagicMock(), "first_name": "Updated"}
        updated = await candidate_repository.update_candidate("507f1f77bcf86cd799439011", {"first_name": "Updated"})
        assert updated["first_name"] == "Updated"

        candidate_repository.collection.find_one.return_value = {"_id": MagicMock(), "email": "a@nucleusteq.com"}
        assert (await candidate_repository.get_candidate_by_email("a@nucleusteq.com"))["email"] == "a@nucleusteq.com"
        assert (await candidate_repository.get_candidate_by_mobile("9999999999")) is not None

    async def test_job_resume_and_status_history(self, candidate_repository):
        candidate_repository.job_collection.find_one.return_value = {"_id": MagicMock(), "jobTitle": "Backend"}
        assert (await candidate_repository.get_job_by_id("507f1f77bcf86cd799439011"))["jobTitle"] == "Backend"
        candidate_repository.job_collection.find.return_value.__aiter__.return_value = []
        assert await candidate_repository.get_jobs_by_title("backend") == []

        candidate_repository.resume_collection.find_one.return_value = {"_id": MagicMock(), "candidate_id": MagicMock(), "file_data": b"abc", "uploaded_by": MagicMock()}
        assert (await candidate_repository.get_resume_metadata("507f1f77bcf86cd799439011"))["candidate_id"]

        candidate_repository.resume_collection.insert_one.return_value = MagicMock(inserted_id="res1")
        candidate_repository.resume_collection.find_one.return_value = {"_id": MagicMock(), "candidate_id": MagicMock(), "file_data": b"abc"}
        assert (await candidate_repository.upsert_resume("507f1f77bcf86cd799439011", "resume.pdf", "application/pdf", b"abc"))["candidate_id"]

        candidate_repository.status_history_collection.insert_one.return_value = MagicMock(inserted_id="hist1")
        candidate_repository.status_history_collection.find.return_value.sort.return_value = MagicMock()
        candidate_repository.status_history_collection.find.return_value.sort.return_value.__aiter__.return_value = []
        assert await candidate_repository.add_status_history("507f1f77bcf86cd799439011", "A", "B") is not None
        assert await candidate_repository.get_status_history("507f1f77bcf86cd799439011") == []

    async def test_invalid_inputs(self, candidate_repository):
        assert await candidate_repository.get_candidate_by_id("bad") is None
        assert await candidate_repository.get_job_by_id("bad") is None
        assert await candidate_repository.get_resume_metadata("bad") is None
        assert await candidate_repository.update_candidate("bad", {}) is None
        assert await candidate_repository.get_resume_file("bad") is None
        assert await candidate_repository.add_status_history("bad", "A", "B") is None
        assert await candidate_repository.get_status_history("bad") == []

    async def test_update_candidate_miss_and_resume_upsert_update_branch(self, candidate_repository):
        candidate_repository.collection.update_one.return_value = MagicMock(matched_count=0)
        assert await candidate_repository.update_candidate("507f1f77bcf86cd799439011", {"first_name": "X"}) is None

        candidate_repository.resume_collection.find_one.return_value = {"_id": MagicMock(), "candidate_id": MagicMock(), "file_data": b"abc"}
        candidate_repository.resume_collection.update_one.return_value = MagicMock()
        candidate_repository.resume_collection.insert_one.return_value = MagicMock()
        candidate_repository.resume_collection.find_one.return_value = {"_id": MagicMock(), "candidate_id": MagicMock(), "file_data": b"abc"}
        result = await candidate_repository.upsert_resume("507f1f77bcf86cd799439011", "resume.pdf", "application/pdf", b"abc", uploaded_by="507f1f77bcf86cd799439012")
        assert result["candidate_id"]

    async def test_hydrate_applied_job_with_invalid_and_valid_ids(self, candidate_repository):
        assert await candidate_repository._hydrate_applied_job({}) == {}
        doc = {"applied_job_id": "bad"}
        assert await candidate_repository._hydrate_applied_job(doc) == doc
        candidate_repository.job_collection.find_one.return_value = {"_id": MagicMock(), "jobTitle": "Backend"}
        doc = {"applied_job_id": "507f1f77bcf86cd799439011"}
        hydrated = await candidate_repository._hydrate_applied_job(doc)
        assert hydrated["applied_job"]["jobTitle"] == "Backend"
