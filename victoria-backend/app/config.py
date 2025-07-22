from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="VICTORIA_")
    
    DATABASE_URL: Optional[str] = None
    FRONTEND_PATH: Optional[str] = None
    PORT: Optional[int] = None
    ADDRESS: Optional[str] = None