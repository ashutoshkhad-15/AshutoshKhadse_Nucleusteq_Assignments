"""FastAPI application bootstrap for the Interview Management Portal API."""

from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter

from src.core.config import settings
from src.core.database import connect_to_mongo, close_mongo_connection
from src.core.logger import setup_logger
from src.exceptions.exception_handlers import add_exception_handlers
from src.schemas.response.common_response import SuccessResponse

logger = setup_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown resources.

    The lifespan hook establishes the MongoDB connection before the API starts
    accepting requests and closes the connection during application shutdown.

    Args:
        app: FastAPI application instance managed by the ASGI server.

    Yields:
        None: Control is yielded to FastAPI while the application is running.

    Raises:
        Exception: Propagates database connection failures during startup.
    """
    logger.info("Starting up application...")
    await connect_to_mongo()
    yield
    logger.info("Shutting down application...")
    await close_mongo_connection()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Backend API for managing candidate interviews.",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# Register shared exception handlers before routing so every endpoint returns a
# consistent error contract.
add_exception_handlers(app)

api_router = APIRouter(prefix=settings.API_V1_STR)


@api_router.get("/health", response_model=SuccessResponse[dict])
async def health_check():
    """Return application health metadata.

    This public endpoint expects no request body or authorization headers. It
    returns a standardized success response containing the active environment
    so deployment checks can verify that the API process is reachable.

    Returns:
        SuccessResponse[dict]: Health response with environment metadata.
    """
    return SuccessResponse(
        message="System is healthy",
        data={"environment": settings.ENVIRONMENT}
    )


app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
