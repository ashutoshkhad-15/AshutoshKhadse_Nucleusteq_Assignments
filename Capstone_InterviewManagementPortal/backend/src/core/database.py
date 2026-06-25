"""MongoDB connection management utilities."""

import logging

from motor.motor_asyncio import AsyncIOMotorClient

from src.core.config import settings

logger = logging.getLogger(__name__)


class DatabaseConfig:
    """Mutable holder for the application MongoDB client and database.

    The FastAPI lifespan hook initializes this object once at startup. Keeping
    the client in a shared holder allows dependencies and repositories to
    access the active database without recreating connection pools.
    """

    client: AsyncIOMotorClient = None
    db = None


db_config = DatabaseConfig()


async def connect_to_mongo():
    """Open the MongoDB client and select the configured database.

    Returns:
        None: The active client and database are stored on ``db_config``.

    Raises:
        Exception: Propagates connection or configuration errors raised by
            Motor while creating the client or selecting the database.
    """
    try:
        logger.info("Connecting to MongoDB...")
        db_config.client = AsyncIOMotorClient(settings.MONGODB_URL)
        db_config.db = db_config.client[settings.DATABASE_NAME]
        logger.info(f"Connected to MongoDB database: {settings.DATABASE_NAME}")
    except Exception as e:
        logger.error(f"Could not connect to MongoDB: {e}")
        raise e


async def close_mongo_connection():
    """Close the MongoDB client if one has been initialized.

    Returns:
        None: The underlying Motor client is closed in place.
    """
    logger.info("Closing MongoDB connection...")
    if db_config.client:
        db_config.client.close()
        logger.info("MongoDB connection closed.")


def get_database():
    """Return the active MongoDB database instance.

    FastAPI dependencies and repository constructors use this function to
    retrieve the database selected during application startup.

    Returns:
        Any: Motor database instance, or ``None`` if startup has not completed.
    """
    return db_config.db
