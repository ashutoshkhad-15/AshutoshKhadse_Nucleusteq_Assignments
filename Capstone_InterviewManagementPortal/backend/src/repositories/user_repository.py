"""User repository for MongoDB-backed account persistence."""

import logging

from bson import ObjectId
from src.core.database import get_database

logger = logging.getLogger(__name__)


class UserRepository:
    """Provide database operations for user account records."""

    def __init__(self):
        """Initialize the repository with the active MongoDB users collection.

        Raises:
            TypeError: If the database connection has not been initialized and
                collection access is attempted on ``None``.
        """
        self.db = get_database()
        self.collection = self.db["users"]
    
    def _serialize_doc(self, doc: dict) -> dict:
        """Safely convert MongoDB ObjectId to a string for FastAPI/Pydantic."""
        if doc and "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc

    async def get_user_by_email(self, email: str) -> dict:
        """Fetch a user document by email address.

        Args:
            email: Unique user email address used as the lookup key.

        Returns:
            dict: Matching user document, or ``None`` when no user exists.
        """
        try:
            return await self.collection.find_one({"email": email})
        except Exception:
            logger.exception("Repository failure while fetching user by email: %s", email)
            raise

    async def create_user(self, user_data: dict) -> dict:
        """Insert a new user document into the users collection.

        Args:
            user_data: User document fields to persist.

        Returns:
            dict: Persisted user data including the generated ``_id`` value.
        """
        try:
            result = await self.collection.insert_one(user_data)
        except Exception:
            logger.exception("Repository failure while creating user: %s", user_data.get("email"))
            raise

        user_data["_id"] = str(result.inserted_id)
        return user_data

    async def update_user(self, email: str, update_data: dict):
        """Update mutable fields for a user identified by email address.

        Args:
            email: Email address of the user document to update.
            update_data: Field/value pairs applied through MongoDB ``$set``.

        Returns:
            None: The update is executed against MongoDB without returning the
            modified document.
        """
        try:
            await self.collection.update_one({"email": email}, {"$set": update_data})
        except Exception:
            logger.exception("Repository failure while updating user: %s", email)
            raise

    async def get_all_users(self) -> list:
        """Return all user documents without sensitive password material."""
        cursor = self.collection.find({}, {"password_base64": 0})
        try:
            users = await cursor.to_list(length=1000)
        except Exception:
            logger.exception("Repository failure while fetching all users")
            raise
        for user in users:
            user["_id"] = str(user["_id"])
        return users

    async def search_users(self, search: str) -> list:
        """Search user documents across common text fields using a case-insensitive regex."""
        query = {
            "$or": [
                {"email": {"$regex": search, "$options": "i"}},
                {"employee_id": {"$regex": search, "$options": "i"}},
                {"role": {"$regex": search, "$options": "i"}},
            ]
        }
        try:
            cursor = self.collection.find(query, {"password_base64": 0})
            users = await cursor.to_list(length=1000)
        except Exception:
            logger.exception("Repository failure while searching users")
            raise
        for user in users:
            user["_id"] = str(user["_id"])
        return users

    async def get_user_by_id(self, user_id: str) -> dict:
        """Fetch a user document by MongoDB identifier.

        Args:
            user_id: MongoDB ObjectId string for the target user.

        Returns:
            dict: Matching user document with sensitive fields excluded, or
            ``None`` when the record cannot be found or parsed.
        """
        try:
            user = await self.collection.find_one({"_id": ObjectId(user_id)}, {"password_base64": 0})
            if user:
                user["_id"] = str(user["_id"])
            return user
        except Exception as exc:
            if "not a valid ObjectId" in str(exc):
                return None
            logger.exception("Repository failure while fetching user by ID: %s", user_id)
            raise

    async def update_user_by_id(self, user_id: str, update_data: dict):
        """Apply a partial update to a user document identified by ObjectId.

        Args:
            user_id: MongoDB ObjectId string for the target user.
            update_data: Field/value pairs to persist using ``$set``.
        """
        try:
            await self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
        except Exception:
            logger.exception("Repository failure while updating user by ID: %s", user_id)
            raise
