"""
config module for the base app.
"""

from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Base settings for the application.
    """
    database_url : str = ""
    redis_url : str = ""
    celery_url : str = ""
    celery_broker_url : str = ""
    celery_result_backend : str = ""

    model_config = SettingsConfigDict(env_file=".env")


@lru_cache()
def get_settings():
    """
    Get the settings for the application.
    """
    return Settings()
