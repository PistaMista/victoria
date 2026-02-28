from app.services.action import ActionRepositoryDiff
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class ActionRepository(BaseModel):
    id: int
    name: str = Field(alias="name")
    url: str = Field(alias="url")

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=True,
        validate_by_name=False,
        serialize_by_alias=False,
    )


class ActionRepositoryCreate(BaseModel):
    id: Optional[int] = None
    name: str
    url: str


class ActionRepositoryUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None

    def to_diff(self) -> ActionRepositoryDiff:
        return ActionRepositoryDiff(name=self.name, url=self.url)
