from datetime import date, datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.repositories.interview_repository import InterviewRepository


class FakeCursor:
    def __init__(self, docs):
        self.docs = docs

    def sort(self, *args, **kwargs):
        return self

    def skip(self, *args, **kwargs):
        return self

    def limit(self, *args, **kwargs):
        return self

    def __aiter__(self):
        async def gen():
            for doc in self.docs:
                yield doc
        return gen()


@pytest.fixture
def repo():
    fake_db = MagicMock()
    fake_collection = MagicMock()
    fake_candidates = MagicMock()
    fake_jobs = MagicMock()
    fake_users = MagicMock()
    fake_db.__getitem__.side_effect = lambda key: {
        "interviews": fake_collection,
        "candidates": fake_candidates,
        "jobs": fake_jobs,
        "users": fake_users,
    }[key]

    with patch("src.repositories.interview_repository.get_database", return_value=fake_db):
        repository = InterviewRepository()
        repository.collection = fake_collection
        repository.candidates = fake_candidates
        repository.jobs = fake_jobs
        repository.users = fake_users
        yield repository


@pytest.mark.asyncio
async def test_create_update_get_and_lists(repo):
    repo.collection.insert_one = AsyncMock(return_value=SimpleNamespace(inserted_id="507f1f77bcf86cd799439011"))
    repo.collection.update_one = AsyncMock(return_value=SimpleNamespace(matched_count=1, modified_count=1))
    repo.collection.find_one = AsyncMock(return_value={"_id": "507f1f77bcf86cd799439011", "interview_date": date(2026, 1, 1)})
    repo.collection.count_documents = AsyncMock(return_value=1)
    repo.collection.find.return_value = FakeCursor([{"_id": "507f1f77bcf86cd799439011"}])

    created = await repo.create_interview({"candidate_id": "507f1f77bcf86cd799439012", "job_id": "507f1f77bcf86cd799439013", "interviewer_id": "507f1f77bcf86cd799439014", "interview_date": date(2026, 1, 1)})
    assert created["_id"] == "507f1f77bcf86cd799439011"

    updated = await repo.update_interview("507f1f77bcf86cd799439011", {"interview_time": "10:30"})
    assert updated["_id"] == "507f1f77bcf86cd799439011"

    assert await repo.get_interview_by_id("507f1f77bcf86cd799439011")
    interviews, total = await repo.get_all_interviews({}, page=1, limit=10)
    assert total == 1 and interviews


@pytest.mark.asyncio
async def test_invalid_ids_and_none_paths(repo):
    repo.collection.find_one = AsyncMock(return_value=None)
    repo.collection.count_documents = AsyncMock(return_value=0)
    repo.candidates.find_one = AsyncMock(return_value=None)
    repo.jobs.find_one = AsyncMock(return_value=None)
    repo.users.find_one = AsyncMock(return_value=None)
    assert repo._normalize_interview_date(datetime(2026, 1, 1, tzinfo=timezone.utc)).date() == date(2026, 1, 1)
    assert repo._normalize_object_id("bad") == "bad"
    assert repo._serialize(None) is None
    assert await repo.update_interview("bad", {}) is None
    assert await repo.get_interview_by_id("bad") is None
    assert await repo.get_interview_by_id_and_interviewer("bad", "usr1") is None
    assert await repo.find_overlapping_interview("bad", date(2026, 1, 1), "10:00") is None
    assert await repo.has_active_scheduled_interview("bad") is False
    assert await repo.has_scheduled_interviews_for_interviewer("bad") is False
    assert await repo.find_interviewer_conflict("bad", date(2026, 1, 1), "10:00") is None
    assert await repo.get_interview_by_candidate("bad") is None
    assert await repo.get_candidate_by_id("bad") is None
    assert await repo.get_job_by_id("bad") is None
    assert await repo.get_user_by_id("bad") is None
    assert await repo.submit_feedback("bad", {}) is None
    assert await repo.get_feedback_by_interview_id("bad") is None
    assert repo._combine_interview_datetime("bad", "10:00") is None


@pytest.mark.asyncio
async def test_repository_helpers_and_conflicts(repo):
    repo.collection.find_one = AsyncMock(return_value={"_id": "507f1f77bcf86cd799439011"})
    repo.collection.count_documents = AsyncMock(return_value=1)
    repo.collection.update_one = AsyncMock(return_value=SimpleNamespace(matched_count=1, modified_count=1))
    repo.jobs.count_documents = AsyncMock(return_value=1)
    repo.candidates.count_documents = AsyncMock(return_value=1)
    repo.collection.find.return_value = FakeCursor([{"_id": "507f1f77bcf86cd799439011", "candidate_id": "cand1", "interview_date": date(2026, 1, 1), "interview_time": "10:00", "status": "INTERVIEW_SCHEDULED"}])
    repo.candidates.find_one = AsyncMock(return_value={"_id": "cand1"})
    repo.jobs.find_one = AsyncMock(return_value={"_id": "job1"})
    repo.users.find_one = AsyncMock(return_value={"_id": "usr1"})
    repo.users.count_documents = AsyncMock(return_value=1)

    assert repo._combine_interview_datetime("2026-01-01", "10:00", timezone.utc)
    assert await repo.find_overlapping_interview("cand1", date(2026, 1, 1), "10:00")
    assert await repo.has_active_scheduled_interview("cand1") is True
    assert await repo.has_scheduled_interviews_for_interviewer("usr1") is True
    assert await repo.find_interviewer_conflict("usr1", date(2026, 1, 1), "10:00")
    assert await repo.get_interview_by_candidate("cand1")
    assert await repo.get_candidate_by_id("cand1")
    assert await repo.get_job_by_id("job1")
    assert await repo.get_user_by_id("usr1")
    assert await repo.submit_feedback("507f1f77bcf86cd799439011", {"feedback": True})
    assert await repo.get_feedback_by_interview_id("507f1f77bcf86cd799439011")
    assert await repo.get_hr_dashboard_stats()
    assert await repo.get_interviewer_dashboard_stats("usr1")


@pytest.mark.asyncio
async def test_complete_overdue_interviews(repo):
    repo.collection.find.return_value = FakeCursor([
        {"_id": "i1", "candidate_id": "cand1", "interview_date": date(2020, 1, 1), "interview_time": "10:00", "status": "INTERVIEW_SCHEDULED"},
        {"_id": "i2", "candidate_id": "cand2", "interview_date": date(2099, 1, 1), "interview_time": "10:00", "status": "INTERVIEW_SCHEDULED"},
    ])
    repo.collection.update_one = AsyncMock(return_value=SimpleNamespace(modified_count=1))
    repo.collection.find_one = AsyncMock(return_value={"_id": "i1", "candidate_id": "cand1", "status": "INTERVIEW_COMPLETED"})
    completed = await repo.complete_overdue_interviews(datetime.now(timezone.utc))
    assert completed
