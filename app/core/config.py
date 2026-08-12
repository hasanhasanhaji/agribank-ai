from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """ Application configuration. 
    Values are loaded from environment variables and the local 
    .env file during development. 
    """

    app_name: str = Field(
        default= "AgriBank AI",
        description="Application name",
    )

    app_version: str = Field(
        default="0.1.0", 
        description="Application version", )

    environment: str = Field(
        default="development",
        description="Current application environment", )

    debug: bool = Field(
        default=False,
        description="Enable debug mode", )

    api_prefix: str = Field(
        default="/api/v1",
        description="Base API prefix",)

    database_url: str = Field( default=( "postgresql+asyncpg://" "postgres:0173276" 
                                        "@localhost:5432/" "agribank" ), 
                                        description="PostgreSQL database URL", )


    model_config = SettingsConfigDict(
        env_file= ".env",
        env_file_encoding="utf-8",
        case_sensitive= False,
        extra="ignore"
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached Settings instance.
    The configuration object is created only once
    and reused throughout the application lifecycle.
    """
    return Settings()