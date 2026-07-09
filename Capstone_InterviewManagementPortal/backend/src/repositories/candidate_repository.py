"""Repository layer for candidate persistence, resume storage, and status history."""

import base64
import logging
from datetime import datetime, timezone

from bson.binary import Binary
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
        self.resume_collection = self.db["candidate_resumes"]
        self.status_history_collection = self.db["candidate_status_history"]

    async def ensure_indexes(self) -> None:
        """Create the indexes used by search, uniqueness, and audit queries."""
        try:
            await self.collection.create_index("email", unique=True, background=True)
            await self.collection.create_index("mobile", unique=True, background=True)
            await self.collection.create_index([("first_name", 1), ("last_name", 1)], background=True)
            await self.collection.create_index("current_company", background=True)
            await self.collection.create_index("applied_job_id", background=True)
            await self.resume_collection.create_index("candidate_id", unique=True, background=True)
            await self.status_history_collection.create_index([("candidate_id", 1), ("timestamp", -1)], background=True)
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

    @staticmethod
    def _serialize_resume_document(document: dict | None) -> dict | None:
        """Return a JSON-safe copy of a stored resume metadata document."""
        if not document:
            return document
        serialized = dict(document)
        serialized["_id"] = str(serialized["_id"])
        serialized["candidate_id"] = str(serialized["candidate_id"])
        if "file_data" in serialized and serialized["file_data"] is not None:
            serialized["resume_content_base64"] = base64.b64encode(bytes(serialized.pop("file_data"))).decode("ascii")
        if "uploaded_by" in serialized and serialized["uploaded_by"] is not None:
            serialized["uploaded_by"] = str(serialized["uploaded_by"])
        return serialized

    @staticmethod
    def _serialize_status_history(document: dict | None) -> dict | None:
        """Return a JSON-safe status history row."""
        if not document:
            return document
        serialized = dict(document)
        serialized["_id"] = str(serialized["_id"])
        serialized["candidate_id"] = str(serialized["candidate_id"])
        if "updated_by" in serialized and serialized["updated_by"] is not None:
            serialized["updated_by"] = str(serialized["updated_by"])
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

    @staticmethod
    def _get_object_id(value: str) -> ObjectId | None:
        """Return a Mongo ObjectId when the input is valid."""
        if not ObjectId.is_valid(value):
            return None
        return ObjectId(value)

    async def create_candidate(self, candidate_data: dict) -> dict:
        """Insert a new candidate document."""
        candidate_data = dict(candidate_data)
        candidate_data["status"] = candidate_data.get("status", "PROFILE_CREATED")
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
        cursor = (
            self.collection.find(normalized_query)
            .sort([("created_at", -1), ("_id", -1)])
            .skip(skip)
            .limit(limit)
        )
        candidates: list[dict] = []
        async for document in cursor:
            document = await self._hydrate_applied_job(document)
            candidates.append(self._serialize_doc(document))
        return candidates, total_items

    async def get_candidate_by_id(self, candidate_id: str) -> dict | None:
        """Fetch a candidate by MongoDB identifier."""
        object_id = self._get_object_id(candidate_id)
        if not object_id:
            return None
        candidate = await self.collection.find_one({"_id": object_id})
        if not candidate:
            return None
        candidate = await self._hydrate_applied_job(candidate)
        return self._serialize_doc(candidate)

    async def update_candidate(self, candidate_id: str, update_data: dict) -> dict | None:
        """Apply a partial update to a candidate document."""
        object_id = self._get_object_id(candidate_id)
        if not object_id:
            return None

        update_data = dict(update_data)
        update_data["updated_at"] = datetime.now(timezone.utc)
        result = await self.collection.update_one({"_id": object_id}, {"$set": update_data})
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
        object_id = self._get_object_id(job_id)
        if not object_id:
            return None
        job = await self.job_collection.find_one({"_id": object_id})
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

    async def get_resume_metadata(self, candidate_id: str) -> dict | None:
        """Return stored resume metadata for a candidate."""
        object_id = self._get_object_id(candidate_id)
        if not object_id:
            return None
        document = await self.resume_collection.find_one({"candidate_id": object_id})
        return self._serialize_resume_document(document)

    async def upsert_resume(self, candidate_id: str, file_name: str, content_type: str, file_bytes: bytes, uploaded_by: str | None = None) -> dict | None:
        """Store resume bytes and metadata for a candidate."""
        object_id = self._get_object_id(candidate_id)
        if not object_id:
            return None
        payload = {
            "candidate_id": object_id,
            "original_filename": file_name,
            "stored_filename": f"{candidate_id}_{file_name}",
            "content_type": content_type,
            "file_data": Binary(file_bytes),
            "uploaded_at": datetime.now(timezone.utc),
            "uploaded_by": ObjectId(uploaded_by) if uploaded_by and ObjectId.is_valid(uploaded_by) else uploaded_by,
        }
        existing = await self.get_resume_metadata(candidate_id)
        if existing:
            await self.resume_collection.update_one({"candidate_id": object_id}, {"$set": payload})
        else:
            await self.resume_collection.insert_one(payload)
        return await self.get_resume_metadata(candidate_id)

    async def get_resume_file(self, candidate_id: str) -> dict | None:
        """Return stored resume bytes and metadata for a candidate."""
        object_id = self._get_object_id(candidate_id)
        if not object_id:
            return None
        document = await self.resume_collection.find_one({"candidate_id": object_id})
        return self._serialize_resume_document(document)

    async def add_status_history(self, candidate_id: str, previous_status: str | None, new_status: str, updated_by: str | None = None) -> dict | None:
        """Append an immutable candidate status history row."""
        object_id = self._get_object_id(candidate_id)
        if not object_id:
            return None
        payload = {
            "candidate_id": object_id,
            "previous_status": previous_status,
            "new_status": new_status,
            "timestamp": datetime.now(timezone.utc),
            "updated_by": ObjectId(updated_by) if updated_by and ObjectId.is_valid(updated_by) else updated_by,
        }
        result = await self.status_history_collection.insert_one(payload)
        payload["_id"] = result.inserted_id
        return self._serialize_status_history(payload)

    async def get_status_history(self, candidate_id: str) -> list[dict]:
        """Return the full status history for a candidate."""
        object_id = self._get_object_id(candidate_id)
        if not object_id:
            return []
        history: list[dict] = []
        cursor = self.status_history_collection.find({"candidate_id": object_id}).sort("timestamp", 1)
        async for document in cursor:
            history.append(self._serialize_status_history(document))
        return history
