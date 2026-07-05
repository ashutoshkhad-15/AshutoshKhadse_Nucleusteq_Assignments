"""Repository layer for candidate persistence and search operations."""

import logging
from datetime import datetime, timezone

from bson.objectid import ObjectId

from src.core.database import get_database

logger = logging.getLogger(__name__)


class CandidateRepository:
    """Provide MongoDB data access operations for candidate records."""

    def __init__(self):
        """Initialize the repository with active MongoDB collections."""
        self.db = get_database()
        self.collection = self.db["candidates"]
        self.job_collection = self.db["jobs"]

    async def ensure_indexes(self) -> None:
        """Create the indexes used by search and uniqueness checks."""
        try:
            await self.collection.create_index("email", unique=True, background=True)
            await self.collection.create_index("mobile", unique=True, background=True)
            await self.collection.create_index([("first_name", 1), ("last_name", 1)], background=True)
            await self.collection.create_index("current_company", background=True)
            await self.collection.create_index("applied_job_id", background=True)
            await self.job_collection.create_index("jobTitle", background=True)
        except Exception:
            logger.exception("Failed to ensure candidate indexes")

    @staticmethod
    def _serialize_doc(document: dict | None) -> dict | None:
        """Return a JSON-friendly copy of a Mongo document."""
        if not document:
            return document
        serialized = dict(document)
        if "_id" in serialized:
            serialized["_id"] = str(serialized["_id"])
        if "applied_job" in serialized and serialized["applied_job"]:
            applied_job = dict(serialized["applied_job"])
            if "_id" in applied_job:
                applied_job["_id"] = str(applied_job["_id"])
            serialized["applied_job"] = applied_job
        return serialized

    async def _hydrate_applied_job(self, candidate: dict) -> dict:
        """Attach a compact applied-job summary when the job exists."""
        if not candidate:
            return candidate

        applied_job_id = candidate.get("applied_job_id")
        if not applied_job_id or not ObjectId.is_valid(str(applied_job_id)):
            return candidate

        job = await self.job_collection.find_one({"_id": ObjectId(applied_job_id)})
        if job:
            candidate["applied_job"] = {"_id": str(job["_id"]), "jobTitle": job.get("jobTitle", "")}
        return candidate

    async def create_candidate(self, candidate_data: dict) -> dict:
        """Insert a new candidate document."""
        candidate_data = dict(candidate_data)
        candidate_data["created_at"] = datetime.now(timezone.utc)
        candidate_data["updated_at"] = datetime.now(timezone.utc)
        result = await self.collection.insert_one(candidate_data)
        candidate_data["_id"] = result.inserted_id
        candidate_data = await self._hydrate_applied_job(candidate_data)
        return self._serialize_doc(candidate_data)

    async def get_all_candidates(self, query: dict | None = None, page: int = 1, limit: int = 10) -> tuple[list[dict], int]:
        """Return matching candidates ordered newest-first."""
        normalized_query = query or {}
        skip = (page - 1) * limit
        total_items = await self.collection.count_documents(normalized_query)
        cursor = self.collection.find(normalized_query).sort("created_at", -1).skip(skip).limit(limit)
        candidates: list[dict] = []
        async for document in cursor:
            document = await self._hydrate_applied_job(document)
            candidates.append(self._serialize_doc(document))
        return candidates, total_items

    async def get_candidate_by_id(self, candidate_id: str) -> dict | None:
        """Fetch a candidate by MongoDB identifier."""
        if not ObjectId.is_valid(candidate_id):
            return None
        candidate = await self.collection.find_one({"_id": ObjectId(candidate_id)})
        if not candidate:
            return None
        candidate = await self._hydrate_applied_job(candidate)
        return self._serialize_doc(candidate)

    async def update_candidate(self, candidate_id: str, update_data: dict) -> dict | None:
        """Apply a partial update to a candidate document."""
        if not ObjectId.is_valid(candidate_id):
            return None

        update_data = dict(update_data)
        update_data["updated_at"] = datetime.now(timezone.utc)
        result = await self.collection.update_one({"_id": ObjectId(candidate_id)}, {"$set": update_data})
        if result.matched_count == 0:
            return None
        return await self.get_candidate_by_id(candidate_id)

    async def get_candidate_by_email(self, email: str) -> dict | None:
        """Fetch a candidate by unique email address."""
        candidate = await self.collection.find_one({"email": email})
        return self._serialize_doc(candidate)

    async def get_candidate_by_mobile(self, mobile: str) -> dict | None:
        """Fetch a candidate by unique mobile number."""
        candidate = await self.collection.find_one({"mobile": mobile})
        return self._serialize_doc(candidate)

    async def get_job_by_id(self, job_id: str) -> dict | None:
        """Fetch an applied job record for candidate validation."""
        if not ObjectId.is_valid(job_id):
            return None
        job = await self.job_collection.find_one({"_id": ObjectId(job_id)})
        if not job:
            return None
        job = dict(job)
        job["_id"] = str(job["_id"])
        return job

    async def get_jobs_by_title(self, search: str) -> list[dict]:
        """Fetch job IDs matching a title search term."""
        query = {"jobTitle": {"$regex": search, "$options": "i"}} if search else {}
        jobs: list[dict] = []
        cursor = self.job_collection.find(query, {"jobTitle": 1})
        async for job in cursor:
            jobs.append({"_id": str(job["_id"]), "jobTitle": job.get("jobTitle", "")})
        return jobs
