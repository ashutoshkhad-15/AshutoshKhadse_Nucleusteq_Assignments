"""Repository layer for candidate persistence and search operations."""

import logging
from datetime import datetime, timezone

from bson import ObjectId

from src.core.database import get_database

logger = logging.getLogger(__name__)


class CandidateRepository:
    """Provide MongoDB data access operations for candidate records."""

    def __init__(self):
        """Initialize the candidate repository with the active collection."""
        self.db = get_database()
        self.collection = self.db["candidates"]

    def _serialize_doc(self, document: dict | None) -> dict | None:
        """Convert MongoDB ObjectId values to strings for API responses.

        Args:
            document: MongoDB candidate document.

        Returns:
            dict | None: Serialized candidate document or ``None``.
        """
        if document and "_id" in document:
            document["_id"] = str(document["_id"])
        return document

    async def create_candidate(self, candidate_data: dict) -> dict:
        """Insert a new candidate document.

        Args:
            candidate_data: Candidate fields ready for persistence.

        Returns:
            dict: Persisted candidate document.
        """
        candidate_data["created_at"] = datetime.now(timezone.utc)
        candidate_data["updated_at"] = datetime.now(timezone.utc)
        result = await self.collection.insert_one(candidate_data)
        candidate_data["_id"] = str(result.inserted_id)
        return candidate_data

    async def get_all_candidates(self, search: str | None = None) -> list[dict]:
        """Return all candidates with optional case-insensitive search.

        Args:
            search: Optional search term applied to name, email, and mobile.

        Returns:
            list[dict]: Matching candidate documents sorted newest-first.
        """
        query: dict = {}
        if search:
            query["$or"] = [
                {"name": {"$regex": search, "$options": "i"}},
                {"email": {"$regex": search, "$options": "i"}},
                {"mobile": {"$regex": search, "$options": "i"}},
            ]

        cursor = self.collection.find(query).sort("created_at", -1)
        candidates = await cursor.to_list(length=1000)
        return [self._serialize_doc(candidate) for candidate in candidates]

    async def get_candidate_by_id(self, candidate_id: str) -> dict | None:
        """Fetch a candidate by MongoDB identifier.

        Args:
            candidate_id: Candidate ObjectId string.

        Returns:
            dict | None: Matching candidate document when found.
        """
        if not ObjectId.is_valid(candidate_id):
            return None
        candidate = await self.collection.find_one({"_id": ObjectId(candidate_id)})
        return self._serialize_doc(candidate)

    async def update_candidate(self, candidate_id: str, update_data: dict) -> dict | None:
        """Apply a partial update to a candidate document.

        Args:
            candidate_id: Candidate ObjectId string.
            update_data: Field/value pairs to persist.

        Returns:
            dict | None: Updated candidate document when the id is valid.
        """
        if not ObjectId.is_valid(candidate_id):
            return None

        update_data["updated_at"] = datetime.now(timezone.utc)
        await self.collection.update_one(
            {"_id": ObjectId(candidate_id)},
            {"$set": update_data},
        )
        return await self.get_candidate_by_id(candidate_id)

    async def get_candidate_by_email(self, email: str) -> dict | None:
        """Fetch a candidate by unique email address.

        Args:
            email: Candidate email address.

        Returns:
            dict | None: Matching candidate document when found.
        """
        candidate = await self.collection.find_one({"email": email})
        return self._serialize_doc(candidate)

    async def get_candidate_by_mobile(self, mobile: str) -> dict | None:
        """Fetch a candidate by unique mobile number.

        Args:
            mobile: Candidate mobile number.

        Returns:
            dict | None: Matching candidate document when found.
        """
        candidate = await self.collection.find_one({"mobile": mobile})
        return self._serialize_doc(candidate)
