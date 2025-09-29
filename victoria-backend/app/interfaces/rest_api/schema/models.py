from pydantic import BaseModel, ConfigDict, Field

class ModelResponse(BaseModel):
    id: int = Field(..., alias="id")
    name: str = Field(..., alias="name")
    connection_id: int = Field(..., alias="connectionId")
    enabled: bool = Field(..., alias="enabled")

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=False,
        validate_by_name=True,
    )

