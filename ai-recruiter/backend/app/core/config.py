"""
Application configuration.

All values are loaded from environment variables (see .env.example).
Nothing sensitive is ever hard-coded here.
"""
from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- App ---
    APP_NAME: str = "AI Recruiter"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # --- Database ---
    DATABASE_URL: str = "postgresql+psycopg2://postgres:postgres234@localhost:5432/ai_recruiter"


    # --- JWT / Auth ---
    JWT_SECRET: str = "CHANGE_ME_IN_ENV"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # --- Google OAuth ---
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""


    # --- LLM ---
    LLM_API_KEY: str = ""
    LLM_MODEL: str = "gemini-3-pro-preview"
    LLM_PROVIDER: str = "gemini"

    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-3.6-flash"
    GEMINI_BASE_URL: str = "https://generativelanguage.googleapis.com/v1beta"

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"

    HF_API_KEY: str = ""
    HF_MODEL: str = "meta-llama/Llama-3.2-3B-Instruct"

    # --- Uploads ---
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE_MB: int = 10

    # --- CORS ---
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000,http://localhost:5501,http://127.0.0.1:5501"

    # --- Rate limiting ---
    RATE_LIMIT_REGISTER_PER_MINUTE: int = 200  # per-IP; generous default, tighten in production
    LOGIN_LOCKOUT_MAX_ATTEMPTS: int = 5
    LOGIN_LOCKOUT_WINDOW_SECONDS: int = 900  # 15 minutes

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance so we only parse the environment once."""
    return Settings()


settings = get_settings()
