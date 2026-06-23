from motor.motor_asyncio import AsyncIOMotorClient
from src.core.config import settings
import logging

logger = logging.getLogger(__name__)

class DatabaseConfig:
    client: AsyncIOMotorClient = None
    db = None

db_config = DatabaseConfig()

async def connect_to_mongo():
    try:
        logger.info("Connecting to MongoDB...")
        db_config.client = AsyncIOMotorClient(settings.MONGODB_URL)
        db_config.db = db_config.client[settings.DATABASE_NAME]
        logger.info(f"Connected to MongoDB database: {settings.DATABASE_NAME}")
    except Exception as e:
        logger.error(f"Could not connect to MongoDB: {e}")
        raise e

async def close_mongo_connection():
    logger.info("Closing MongoDB connection...")
    if db_config.client:
        db_config.client.close()
        logger.info("MongoDB connection closed.")

def get_database():
    """Dependency to get the database instance."""
    return db_config.db