"""User repository for MongoDB-backed account persistence."""

import logging

from bson import ObjectId

from src.constants.app_constants import AppConstants
from src.constants.interview_constants import InterviewConstants
from src.core.database import get_database
from src.exceptions.custom_exceptions import AppBaseException

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
        self.interviews = self.db[InterviewConstants.INTERVIEW_COLLECTION]

    @staticmethod
    def _stringify_ids(users: list[dict]) -> list[dict]:
        """Convert MongoDB ObjectId values into strings for API responses."""
        for user in users:
            user["_id"] = str(user["_id"])
        return users

    @staticmethod
    def _raise_repository_error(operation: str, exc: Exception) -> None:
        """Raise a stable application error for repository failures."""
        logger.exception("Repository failure while %s", operation)
        raise AppBaseException("An unexpected database error occurred.", "USER_REPOSITORY_ERROR", 500) from exc

    async def get_user_by_email(self, email: str) -> dict:
        """Fetch a user document by email address.

        Args:
            email: Unique user email address used as the lookup key.

        Returns:
            dict: Matching user document, or ``None`` when no user exists.
        """
        try:
            return await self.collection.find_one({"email": email})
        except Exception as exc:
            self._raise_repository_error(f"fetching user by email: {email}", exc)

    async def create_user(self, user_data: dict) -> dict:
        """Insert a new user document into the users collection.

        Args:
            user_data: User document fields to persist.

        Returns:
            dict: Persisted user data including the generated ``_id`` value.
        """
        try:
            result = await self.collection.insert_one(user_data)
        except Exception as exc:
            self._raise_repository_error(f"creating user: {user_data.get('email')}", exc)

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
        except Exception as exc:
            self._raise_repository_error(f"updating user: {email}", exc)

    async def get_all_users(self, page: int = 1, limit: int = 10) -> tuple[list, int]:
        """Return all user documents without sensitive password material."""
        query = {}
        try:
            total_items = await self.collection.count_documents(query)
            cursor = (
                self.collection.find(query, {"password_base64": 0})
                .sort([("created_at", -1), ("_id", -1)])
                .skip((page - 1) * limit)
                .limit(limit)
            )
            users = await cursor.to_list(length=1000)
        except Exception as exc:
            self._raise_repository_error("fetching all users", exc)
        return self._stringify_ids(users), total_items

    async def search_users(self, search: str, page: int = 1, limit: int = 10) -> tuple[list, int]:
        """Search user documents across common text fields using a case-insensitive regex."""
        query = {
            "$or": [
                {"name": {"$regex": search, "$options": "i"}},
                {"email": {"$regex": search, "$options": "i"}},
                {"role": {"$regex": search, "$options": "i"}},
            ]
        }
        try:
            total_items = await self.collection.count_documents(query)
            cursor = (
                self.collection.find(query, {"password_base64": 0})
                .sort([("created_at", -1), ("_id", -1)])
                .skip((page - 1) * limit)
                .limit(limit)
            )
            users = await cursor.to_list(length=limit)
        except Exception as exc:
            self._raise_repository_error(f"searching users with term: {search}", exc)
        return self._stringify_ids(users), total_items

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
            return self._stringify_ids([user])[0] if user else None
        except Exception as exc:
            if "not a valid ObjectId" in str(exc):
                return None
            self._raise_repository_error(f"fetching user by ID: {user_id}", exc)

    async def update_user_by_id(self, user_id: str, update_data: dict):
        """Apply a partial update to a user document identified by ObjectId.

        Args:
            user_id: MongoDB ObjectId string for the target user.
            update_data: Field/value pairs to persist using ``$set``.
        """
        try:
            await self.collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
        except Exception as exc:
            self._raise_repository_error(f"updating user by ID: {user_id}", exc)

    async def get_default_admin(self) -> dict | None:
        """Return the seeded default admin account, if it exists."""
        try:
            user = await self.collection.find_one({"email": AppConstants.DEFAULT_ADMIN_EMAIL}, {"password_base64": 0})
            return self._stringify_ids([user])[0] if user else None
        except Exception as exc:
            self._raise_repository_error("fetching default admin account", exc)

