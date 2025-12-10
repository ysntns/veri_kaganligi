"""
Uygulama konfigurasyonu
"""
import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Uygulama ayarlari"""

    # API Ayarlari
    APP_NAME: str = "Veri Kaganligi - Turkce NLP API"
    APP_VERSION: str = "2.0.0"
    DEBUG: bool = False

    # Server Ayarlari
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # CORS Ayarlari
    CORS_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # Model Ayarlari
    MAX_TEXT_LENGTH: int = 512
    SUMMARIZATION_MAX_LENGTH: int = 150
    SUMMARIZATION_MIN_LENGTH: int = 50

    # HuggingFace
    HUGGINGFACE_TOKEN: str | None = None

    class Config:
        env_file = ".env"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
