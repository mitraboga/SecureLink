from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SecureLink"
    database_url: str = "sqlite:///./securelink.db"
    jwt_secret: str = "change-this-development-secret"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 60
    key_encryption_secret: str = "change-this-key-encryption-secret"
    replay_window_seconds: int = 300
    rate_limit_requests: int = 120
    rate_limit_window_seconds: int = 60
    environment: str = "development"
    redis_url: str | None = None
    login_failure_threshold: int = 5
    login_failure_window_seconds: int = 300

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
