"""Repository layer for Job Descriptions.

This module encapsulates direct database interactions for job documents.
It intentionally keeps transformation logic minimal; higher-level business
rules are applied by the service layer.
"""

import logging
from datetime import datetime, timezone

from bson.objectid import ObjectId

from src.core.database import get_database

logger = logging.getLogger(__name__)


class JobRepository:
    """Data access operations for job descriptions collection."""

    def __init__(self):
        """Initialize the repository with the active MongoDB jobs collection."""
        logger.info("Initializing JobRepository")
        self.db = get_database()
        self.collection = self.db["jobs"]

    def _normalize_job(self, job_data: dict) -> dict:
        """Return a response-ready job document with stringified identifiers."""
        if not job_data:
            return job_data
        normalized = dict(job_data)
        normalized["_id"] = str(normalized["_id"])
        normalized["experienceRequired"] = str(normalized.get("experienceRequired", ""))
        normalized["requiredSkills"] = normalized.get("requiredSkills", [])
        return normalized

    @staticmethod
    def _build_job_query(query: dict | None = None) -> dict:
        """Normalize an incoming query payload for MongoDB lookups."""
        return query or {}

    async def create_job(self, job_data: dict) -> dict:
        """Insert a new job description into the database.

        Adds created/updated timestamps and returns the stored document with
        the Mongo `_id` converted to a string for JSON compatibility.
        """
        try:
            job_data["created_at"] = datetime.now(timezone.utc)
            job_data["updated_at"] = datetime.now(timezone.utc)
            result = await self.collection.insert_one(job_data)
            job_data["_id"] = result.inserted_id
            job_data = self._normalize_job(job_data)
            logger.info("Job created successfully: %s", job_data.get("_id"))
            return job_data
        except Exception:
            logger.exception("Repository failure while creating job")
            raise

    async def get_all_jobs(self, query: dict | None = None, page: int = 1, limit: int = 10) -> tuple[list, int]:
        """Retrieve all job descriptions ordered newest-first.

        The cursor is iterated asynchronously to avoid loading the entire
        collection into memory at once in large deployments.
        """
        try:
            normalized_query = self._build_job_query(query)
            total_items = await self.collection.count_documents(normalized_query)
            jobs = []
            cursor = (
                self.collection.find(normalized_query)
                .sort([("created_at", -1), ("_id", -1)])
                .skip((page - 1) * limit)
                .limit(limit)
            )
            async for document in cursor:
                document["_id"] = str(document["_id"])
                document = self._normalize_job(document)
                jobs.append(document)
            logger.info("Job list retrieved successfully")
            return jobs, total_items
        except Exception:
            logger.exception("Repository failure while fetching all jobs")
            raise

    async def get_job_by_id(self, job_id: str) -> dict:
        """Retrieve a specific job description by its ID.

        Returns None when the provided id is not a valid ObjectId or if the
        document cannot be found; callers are expected to translate that into
        an application-level error if necessary.
        """
        if not ObjectId.is_valid(job_id):
            logger.warning("Invalid job ID provided: %s", job_id)
            return None

        try:
            job = await self.collection.find_one({"_id": ObjectId(job_id)})
            if job:
                job = self._normalize_job(job)
            else:
                logger.warning("Job not found for ID: %s", job_id)
            return job
        except Exception:
            logger.exception("Repository failure while fetching job by ID: %s", job_id)
            raise
        
    async def update_job(self, job_id: str, update_data: dict) -> dict:
        """Update specific fields of an existing job description.

        Appends an `updated_at` timestamp and performs a Mongo `$set` update.
        Returns the updated document (or None when the id is invalid).
        """
        if not ObjectId.is_valid(job_id):
            logger.warning("Invalid job ID provided for update: %s", job_id)
            return None

        try:
            update_data["updated_at"] = datetime.now(timezone.utc)
            await self.collection.update_one(
                {"_id": ObjectId(job_id)},
                {"$set": update_data},
            )
            logger.info("Job updated successfully: %s", job_id)
            return await self.get_job_by_id(job_id)
        except Exception:
            logger.exception("Repository failure while updating job: %s", job_id)
            raise
