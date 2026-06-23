from fastapi import FastAPI, APIRouter
from contextlib import asynccontextmanager
from src.core.config import settings
from src.core.database import connect_to_mongo, close_mongo_connection
from src.core.logger import setup_logger
from src.exceptions.exception_handlers import add_exception_handlers
from src.schemas.response.common_response import SuccessResponse

# Initialize logger
logger = setup_logger()

# Manage Application Lifespan (Startup/Shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup tasks
    logger.info("Starting up application...")
    await connect_to_mongo()
    yield
    # Shutdown tasks
    logger.info("Shutting down application...")
    await close_mongo_connection()

# Initialize FastAPI app with Swagger configs
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Backend API for managing candidate interviews.",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Register Exception Handlers
add_exception_handlers(app)

# Setup Base Router
api_router = APIRouter(prefix=settings.API_V1_STR)

@api_router.get("/health", response_model=SuccessResponse[dict])
async def health_check():
    """Health check endpoint to verify API and DB connectivity."""
    return SuccessResponse(
        message="System is healthy",
        data={"environment": settings.ENVIRONMENT}
    )

# Include Routers
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)