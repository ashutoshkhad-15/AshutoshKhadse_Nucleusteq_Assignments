"""Repository layer for Job Descriptions.

This module encapsulates direct database interactions for job documents.
It intentionally keeps transformation logic minimal; higher-level business
rules are applied by the service layer.
"""

from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
import os
from datetime import datetime, timezone


class JobRepository:
    """Data access operations for job descriptions collection."""

    def __init__(self):
        # Using the standard MongoDB connection setup; environment variables
        # allow the test environment to override the connection string.
        client = AsyncIOMotorClient(os.getenv("MONGODB_URL", "mongodb://localhost:27017"))
        self.db = client[os.getenv("DATABASE_NAME", "interview_portal_db")]
        self.collection = self.db.jobs

    async def create_job(self, job_data: dict) -> dict:
        """Insert a new job description into the database.

        Adds created/updated timestamps and returns the stored document with
        the Mongo `_id` converted to a string for JSON compatibility.
        """
        job_data["created_at"] = datetime.now(timezone.utc)
        job_data["updated_at"] = datetime.now(timezone.utc)

        result = await self.collection.insert_one(job_data)

        # Convert ObjectId to string to prevent FastAPI/Pydantic crashes
        job_data["_id"] = str(result.inserted_id)
        return job_data

    async def get_all_jobs(self, query: dict | None = None) -> list:
        """Retrieve all job descriptions ordered newest-first.

        The cursor is iterated asynchronously to avoid loading the entire
        collection into memory at once in large deployments.
        """
        jobs = []
        cursor = self.collection.find(query or {}).sort("created_at", -1)  # Newest first
        async for document in cursor:
            document["_id"] = str(document["_id"])
            jobs.append(document)
        return jobs

    async def get_job_by_id(self, job_id: str) -> dict:
        """Retrieve a specific job description by its ID.

        Returns None when the provided id is not a valid ObjectId or if the
        document cannot be found; callers are expected to translate that into
        an application-level error if necessary.
        """
        if not ObjectId.is_valid(job_id):
            return None

        job = await self.collection.find_one({"_id": ObjectId(job_id)})
        if job:
            job["_id"] = str(job["_id"])
        return job

    async def update_job(self, job_id: str, update_data: dict) -> dict:
        """Update specific fields of an existing job description.

        Appends an `updated_at` timestamp and performs a Mongo `$set` update.
        Returns the updated document (or None when the id is invalid).
        """
        if not ObjectId.is_valid(job_id):
            return None

        update_data["updated_at"] = datetime.now(timezone.utc)

        await self.collection.update_one(
            {"_id": ObjectId(job_id)},
            {"$set": update_data},
        )
        return await self.get_job_by_id(job_id)
