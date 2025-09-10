from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """API 공통 응답 형식"""

    success: bool = True
    message: str = "성공"
    data: Optional[T] = None


class ErrorResponse(BaseModel):
    """에러 응답 형식"""

    success: bool = False
    message: str
    error_code: Optional[str] = None
