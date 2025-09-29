from fastapi import status, HTTPException, APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from app.services.trigger import TriggerService, NonexistentEventError
from app.model.user import User
from .schema.events import EventResponse
from .dependencies.auth import get_non_admin_user
from typing import Annotated
from app.containers import Container

router = APIRouter()

@router.get("/{id}", response_model=EventResponse)
@inject
async def get_event(
    id: int,
    user: Annotated[User, Depends(get_non_admin_user)],
    trigger_service: Annotated[TriggerService, Depends(Provide[Container.trigger])]
) -> EventResponse:
    try:
        event = trigger_service.get_user_event(
            user_id=user.id,
            event_id=id
        )
        return EventResponse(
            triggerId=event.trigger_id,
            content=event.content
        )
    except NonexistentEventError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )



