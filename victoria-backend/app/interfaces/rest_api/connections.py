from fastapi import APIRouter, status, HTTPException, Depends
from app.services.llm import (
    LLMService,
    NonexistentConnectionError,
    OllamaCommunicationError,
)
from app.model.user import User
from app.containers import Container
from dependency_injector.wiring import inject, Provide
from .schema.connections import (
    ConnectionListItemResponse,
    ConnectionResponse,
    ConnectionCreate,
    ConnectionUpdate,
)
from .dependencies.auth import get_admin_user
from typing import List, Annotated

router = APIRouter()


@router.get("/", response_model=List[ConnectionListItemResponse])
@inject
async def list_all_connections(
    _: Annotated[User, Depends(get_admin_user)],
    llm_service: Annotated[LLMService, Depends(Provide[Container.llm])],
) -> List[ConnectionListItemResponse]:
    connections = llm_service.get_all_connections()
    return [ConnectionListItemResponse.model_validate(x) for x in connections]


@router.post("/", response_model=ConnectionListItemResponse)
@inject
async def create_connection(
    _: Annotated[User, Depends(get_admin_user)],
    llm_service: Annotated[LLMService, Depends(Provide[Container.llm])],
    body: ConnectionCreate,
) -> ConnectionListItemResponse:
    try:
        new_id = llm_service.add_ollama_connection(name=body.name, url=body.url)
        new_connection = llm_service.get_connection_by_id(new_id)
        return ConnectionListItemResponse.model_validate(new_connection)
    except OllamaCommunicationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to contact provided Ollama server, please check the URL",
        )


@router.get("/{id}", response_model=ConnectionResponse)
@inject
async def get_connection(
    id: int,
    _: Annotated[User, Depends(get_admin_user)],
    llm_service: Annotated[LLMService, Depends(Provide[Container.llm])],
) -> ConnectionResponse:
    try:
        connection = llm_service.get_connection_by_id(id)
        return ConnectionResponse.model_validate(connection)
    except NonexistentConnectionError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))


@router.put("/{id}")
@inject
async def update_connection(
    id: int,
    _: Annotated[User, Depends(get_admin_user)],
    llm_service: Annotated[LLMService, Depends(Provide[Container.llm])],
    body: ConnectionUpdate,
):
    try:
        llm_service.update_ollama_connection(id=id, changes=body.to_diff())
    except NonexistentConnectionError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
    except OllamaCommunicationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to contact provided Ollama server, please check the URL",
        )


@router.delete("/{id}")
@inject
async def delete_connection(
    id: int,
    _: Annotated[User, Depends(get_admin_user)],
    llm_service: Annotated[LLMService, Depends(Provide[Container.llm])],
):
    try:
        llm_service.remove_connection(id=id)
    except NonexistentConnectionError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
