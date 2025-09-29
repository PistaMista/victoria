from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.services.llm import OllamaConnectionDiff

class ConnectionListItemResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=False,
        validate_by_name=True,
    )

class ConnectionResponse(BaseModel):
    id: int
    name: str
    url: str

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=False,
        validate_by_name=True,
    )

class ConnectionCreate(BaseModel):
    id: Optional[int] = None
    name: str
    url: str

class ConnectionUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None

    def to_diff(self) -> OllamaConnectionDiff:
        return OllamaConnectionDiff(
            name=self.name,
            url=self.url
        )
