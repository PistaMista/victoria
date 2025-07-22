from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="VICTORIA_")
    
    database_url: Optional[str]
    frontend_path: Optional[str]
    port: Optional[int]
    address: Optional[str]