from fastapi import FastAPI

from app.api.health import router as health_router
from app.core.config import get_settings
from app.core.exceptions import (
    AppException,app_exception_handler
    
)
from app.core.loging import configure_logging
from app.modules.customers.router import (
    router as customer_router,
)


settings = get_settings()

configure_logging()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "AI-powered banking platform "
        "for agricultural customers."
    ),
)


app.add_exception_handler(
    AppException,
    app_exception_handler,
)


app.include_router(
    health_router,
    prefix=settings.api_prefix,
)


app.include_router(
    customer_router,
    prefix=settings.api_prefix,
)


@app.get(
    "/",
    tags=["System"],
)
async def root() -> dict[str, str]:
    """
    Return basic application information.
    """

    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }