import asyncio
import logging
from src.core.config import settings
from src.core.database import connect_to_mongo, close_mongo_connection, get_database
from src.utils.security import encode_password
from src.enums.app_enums import UserRole

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_seed():
    await connect_to_mongo()
    db = get_database()
    collection = db["users"]

    admin_email = "admin@nucleusteq.com"
    existing_admin = await collection.find_one({"email": admin_email})

    if existing_admin:
        logger.info(f"Admin user {admin_email} already exists. Skipping seed.")
    else:
        # Securely fetch the password from the environment context
        secure_password = settings.DEFAULT_ADMIN_PASSWORD
        
        admin_user = {
            "email": admin_email,
            "password_base64": encode_password(secure_password),
            "role": UserRole.ADMIN.value,
            "is_active": True,
            "requires_password_reset": True 
        }
        await collection.insert_one(admin_user)
        # Log the action, but NEVER log the actual password string
        logger.info(f"Successfully seeded Admin user: {admin_email} from environment configuration.")

    await close_mongo_connection()

if __name__ == "__main__":
    asyncio.run(run_seed())