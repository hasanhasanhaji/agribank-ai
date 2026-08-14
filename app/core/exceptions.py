from typing import Any

from fastapi import Request
from fastapi.responses import JSONResponse


class AppException(Exception):
    """
    Base exception for application-level errors.
    """

    status_code: int = 500
    error_code: str = "APP_ERROR"

    def __init__(
        self,
        message: str,
        details: Any | None = None,
    ) -> None:
        self.message = message
        self.details = details

        super().__init__(message)


class NotFoundException(AppException):
    """
    Raised when a requested resource does not exist.
    """

    status_code = 404
    error_code = "RESOURCE_NOT_FOUND"


class ConflictException(AppException):
    """
    Raised when a business conflict occurs.
    """

    status_code = 409
    error_code = "RESOURCE_CONFLICT"


class BadRequestException(AppException):
    """
    Raised when the request violates business rules.
    """

    status_code = 400
    error_code = "BAD_REQUEST"


async def app_exception_handler(
    request: Request,
    exc: AppException,
) -> JSONResponse:
    """
    Convert application exceptions into a
    standardized HTTP response.
    """

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "code": exc.error_code,
                "message": exc.message,
                "details": exc.details,
            },
        },
    )