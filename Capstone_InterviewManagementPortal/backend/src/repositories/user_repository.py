"""User repository for MongoDB-backed account persistence."""

from src.core.database import get_database


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

    async def get_user_by_email(self, email: str) -> dict:
        """Fetch a user document by email address.

        Args:
            email: Unique user email address used as the lookup key.

        Returns:
            dict: Matching user document, or ``None`` when no user exists.
        """
        return await self.collection.find_one({"email": email})

    async def create_user(self, user_data: dict) -> dict:
        """Insert a new user document into the users collection.

        Args:
            user_data: User document fields to persist.

        Returns:
            dict: Persisted user data including the generated ``_id`` value.
        """
        result = await self.collection.insert_one(user_data)
        user_data["_id"] = result.inserted_id
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
        await self.collection.update_one({"email": email}, {"$set": update_data})
