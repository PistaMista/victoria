from fastapi import status, APIRouter, Depends, HTTPException
from app.services.agent import AgentService, NonexistentAgentError, InvalidAgentSettingError
from app.containers import Container
from app.model.user import User
from app.model.chat import Chat
from app.model.agent import Agent
from typing import List, Annotated
from .schema.agents import AgentListItemResponse, AgentCreate, AgentResponse, AgentUpdate
from .schema.monologues import MonologueListItemResponse, to_monologue_list_item_response
from .dependencies.auth import get_non_admin_user
from dependency_injector.wiring import inject, Provide

router = APIRouter()


@router.get("/", response_model=List[AgentListItemResponse])
@inject
async def list_agents(
    user: Annotated[User, Depends(get_non_admin_user)],
    agent_service: Annotated[AgentService, Depends(Provide[Container.agent])]
) -> List[AgentListItemResponse]:
    agents = agent_service.get_user_agents(user.id)
    return [
            AgentListItemResponse(
                id=x.id,
                name=x.name,
                status="BUSY" if agent_service.is_agent_running_monologues(x.id) else "IDLE"
            )
            for x in agents
    ]


@router.post("/")
@inject
async def create_agent(
    user: Annotated[User, Depends(get_non_admin_user)],
    body: AgentCreate,
    agent_service: Annotated[AgentService, Depends(Provide[Container.agent])]
) -> None:
    try:
        agent_service.add_user_agent(
            user_id=user.id,
            name=body.name,
            model_id=body.baseModelId,
            system_prompt=body.systemPrompt,
            model_parameters=body.modelParameters,
            enabled_trigger_ids=body.enabledTriggers,
            enabled_action_ids=body.enabledActions
        )
    except InvalidAgentSettingError as err:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(err)
            )

@router.get("/{id}", response_model=AgentResponse)
@inject
async def get_agent(
    id: int,
    user: Annotated[User, Depends(get_non_admin_user)],
    agent_service: Annotated[AgentService, Depends(Provide[Container.agent])]
) -> AgentResponse:
    try:
        agent: Agent = agent_service.get_user_agent_by_id(
            user_id=user.id,
            agent_id=id
        )
        return AgentResponse(
            id=agent.id,
            name=agent.name,
            status="BUSY" if agent_service.is_agent_running_monologues(agent.id) else "IDLE",
            baseModelId=agent.model_id,
            systemPrompt=agent.prompt,
            modelParameters=agent.model_params,
            enabledTriggers=[x.id for x in agent.allowed_triggers],
            enabledActions=[x.id for x in agent.allowed_actions]
        )
    except NonexistentAgentError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )

@router.put("/{id}")
@inject
async def update_agent(
    id: int,
    body: AgentUpdate,
    user: Annotated[User, Depends(get_non_admin_user)],
    agent_service: Annotated[AgentService, Depends(Provide[Container.agent])]
) -> None:
    try:
        agent_service.update_user_agent(
            user_id=user.id,
            agent_id=id,
            diff=body.to_diff()
        )
    except InvalidAgentSettingError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err)
        )
    except NonexistentAgentError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )

@router.delete("/{id}")
@inject
async def delete_agent(
    id: int,
    user: Annotated[User, Depends(get_non_admin_user)],
    agent_service: Annotated[AgentService, Depends(Provide[Container.agent])]
) -> None:
    try:
        agent_service.remove_user_agent(
            user_id=user.id,
            agent_id=id
        )
    except NonexistentAgentError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )

@router.get("/{id}/monologues", response_model=List[MonologueListItemResponse])
@inject
async def list_agent_monologues(
    id: int,
    user: Annotated[User, Depends(get_non_admin_user)],
    agent_service: Annotated[AgentService, Depends(Provide[Container.agent])]
) -> List[MonologueListItemResponse]:
    try:
        monologues = agent_service.get_user_agent_monologues(
            user_id=user.id,
            agent_id=id
        )
        return [
            to_monologue_list_item_response(x)
            for x in monologues
        ]
    except NonexistentAgentError as err:
        raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(err)
            )

