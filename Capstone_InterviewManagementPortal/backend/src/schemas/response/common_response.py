from pydantic import BaseModel
from typing import Generic, TypeVar, Optional, Any

T = TypeVar("T")

class SuccessResponse(BaseModel, Generic[T]):
    success: bool = True
    message: str
    data: Optional[T] = None
    meta: Optional[dict[str, Any]] = None

class ErrorResponse(BaseModel):
    success: bool = False
    error_code: str
    message: str
    details: Optional[Any] = None