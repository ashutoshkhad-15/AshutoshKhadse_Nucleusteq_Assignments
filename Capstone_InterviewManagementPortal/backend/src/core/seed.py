"""Database seed script for initial administrator provisioning."""

import asyncio
import logging

from src.core.database import connect_to_mongo, close_mongo_connection, get_database
from src.utils.security import encode_password
from src.enums.app_enums import UserRole

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def run_seed():
    """Create the default administrator account when it does not exist.

    The seed operation connects to MongoDB, checks for the configured default
    administrator email, and inserts the account only when it is missing. The
    seeded account is marked for password reset so the initial shared password
    is replaced during the first authenticated session.

    Returns:
        None: The user collection is updated in place when seeding is required.

    Raises:
        Exception: Propagates MongoDB connection, query, or insert failures.
    """
    await connect_to_mongo()
    db = get_database()
    collection = db["users"]

    admin_email = "admin@nucleusteq.com"
    existing_admin = await collection.find_one({"email": admin_email})

    if existing_admin:
        logger.info(f"Admin user {admin_email} already exists. Skipping seed.")
    else:
        admin_user = {
            "email": admin_email,
            "password_base64": encode_password("Admin@123"),
            "role": UserRole.ADMIN.value,
            "is_active": True,
            # Enforce credential rotation after the seeded account is used.
            "requires_password_reset": True
        }
        await collection.insert_one(admin_user)
        logger.info(f"Successfully seeded Admin user: {admin_email} with password: Admin@123")

    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(run_seed())
