from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="VICTORIA_")

    DATABASE_URL: Optional[str] = None
    FRONTEND_PATH: Optional[str] = None
    PORT: Optional[int] = None
    ADDRESS: Optional[str] = None
    # TODO: Create a setting in the nixos module for a jwt_secret_file
    JWT_SECRET: str = os.urandom(32).hex()
    WS_HEARTBEAT_INTERVAL: float = 30.0
    WS_HEARTBEAT_TIMEOUT: float = 60.0


settings = Settings()
