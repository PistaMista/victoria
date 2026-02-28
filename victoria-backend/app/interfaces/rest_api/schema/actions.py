from pydantic import BaseModel, ConfigDict, Field, computed_field


class ActionResponse(BaseModel):
    id: int
    repository_id: int = Field(alias="repoId")
    function_name: str = Field(alias="name")

    model_config = ConfigDict(
        from_attributes=True,
        validate_by_alias=False,
        validate_by_name=True,
    )

    @computed_field
    @property
    def displayName(self) -> str:
        return self.function_name.replace("_", " ").capitalize()
