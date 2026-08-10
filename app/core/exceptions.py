from fastapi import Request
from fastapi.responses import JSONResponse

class AppException(Exception):
    """
    Base exception for application-specific errors.
    """

    def __init__(self, message: str,status_code: int = 400,)-> None:
        self.message = message,
        self.status_code = status_code,
        super().__init__(message)

    async def app_exception_handler( request: Request,
                                     exc: AppException, ) -> JSONResponse:
        """
        Convert application exceptions into a consistent JSON response.
        """

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "message": exc.message,
                    },
                    },
        )