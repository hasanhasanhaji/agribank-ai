from fastapi import FastAPI
from app.api.health import router as health_router
from app.core.config import get_settings
from app.core.exceptions import AppException
                                
from app.core.loging import configure_logging

settings = get_settings()          # settings object
configure_logging()                # setup logging

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "AI-powered banking platform "
          "for agricultural customers."
          ), ) # create FastAPI app instance


app.add_exception_handler( AppException, AppException.app_exception_handler, ) # exception handler for AppException
app.include_router(health_router,
                   prefix=settings.api_prefix,) # include health check router

# define root endpoint
@app.get( "/", tags=["System"], ) 
async def root() -> dict[str, str]: 
    """
    Root endpoint for the application.
    Returns a simple message indicating that the application is running.
    """
    return {"application": settings.app_name,
             "version": settings.app_version,
               "environment": settings.environment,}