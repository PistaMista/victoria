from fastapi import APIRouter, status, HTTPException, Depends
from dependency_injector.wiring import inject, Provide
from app.services.llm import LLMService, NonexistentModelError
from app.containers import Container
from app.model.user import User
from .schema.models import ModelResponse
from .dependencies.auth import get_non_admin_user, get_admin_user
from typing import List, Annotated

router = APIRouter()


@router.get("/enabled", response_model=List[ModelResponse])
@inject
async def get_enabled_models(
    _: Annotated[User, Depends(get_non_admin_user)],
    llm_service: Annotated[LLMService, Depends(Provide[Container.llm])],
) -> List[ModelResponse]:
    models = llm_service.get_enabled_models()
    return [ModelResponse.model_validate(x) for x in models]


@router.get("/all", response_model=List[ModelResponse])
@inject
async def get_all_models(
    _: Annotated[User, Depends(get_non_admin_user)],
    llm_service: Annotated[LLMService, Depends(Provide[Container.llm])],
) -> List[ModelResponse]:
    models = llm_service.get_all_models()
    return [ModelResponse.model_validate(x) for x in models]


@router.post("/{id}/enable")
@inject
async def enable_model(
    id: int,
    _: Annotated[User, Depends(get_admin_user)],
    llm_service: Annotated[LLMService, Depends(Provide[Container.llm])],
):
    try:
        llm_service.set_model_enabled_by_id(model_id=id, enabled=True)
    except NonexistentModelError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.post("/{id}/disable")
@inject
async def disable_model(
    id: int,
    _: Annotated[User, Depends(get_admin_user)],
    llm_service: Annotated[LLMService, Depends(Provide[Container.llm])],
):
    try:
        llm_service.set_model_enabled_by_id(model_id=id, enabled=False)
    except NonexistentModelError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
