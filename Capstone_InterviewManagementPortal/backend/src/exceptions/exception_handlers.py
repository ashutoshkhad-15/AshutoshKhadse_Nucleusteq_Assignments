from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from src.exceptions.custom_exceptions import AppBaseException
from src.schemas.response.common_response import ErrorResponse
import logging

logger = logging.getLogger(__name__)

def add_exception_handlers(app: FastAPI):
    
    @app.exception_handler(AppBaseException)
    async def app_exception_handler(request: Request, exc: AppBaseException):
        logger.warning(f"AppException: {exc.error_code} - {exc.message}")
        response = ErrorResponse(
            error_code=exc.error_code,
            message=exc.message
        )
        return JSONResponse(status_code=exc.status_code, content=response.model_dump())

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.error(f"Validation Error: {exc.errors()}")
        response = ErrorResponse(
            error_code="VALIDATION_ERROR",
            message="Invalid request parameters",
            details=exc.errors()
        )
        return JSONResponse(status_code=422, content=response.model_dump())

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.critical(f"Unhandled Exception: {str(exc)}", exc_info=True)
        response = ErrorResponse(
            error_code="INTERNAL_SERVER_ERROR",
            message="An unexpected error occurred."
        )
        return JSONResponse(status_code=500, content=response.model_dump())