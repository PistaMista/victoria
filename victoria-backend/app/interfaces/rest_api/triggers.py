from fastapi import status, APIRouter, HTTPException, Depends
from app.services.trigger import TriggerService, NonexistentTriggerError, TriggerDiff, TimerTriggerDiff, PollTriggerDiff, ChatTriggerDiff, WebhookTriggerDiff
from app.model.user import User
from app.model.trigger import TimerTrigger, PollTrigger, ChatTrigger, WebhookTrigger
from dependency_injector.wiring import inject, Provide
from app.containers import Container
from .dependencies.auth import get_non_admin_user, get_admin_user
from .schema.triggers import TriggerListItemResponse, TriggerResponse, TriggerCreate, TimerSettings, PollSettings, ChatSettings, WebhookSettings, to_trigger_response, TriggerUpdate, TimerSettingsUpdate, PollSettingsUpdate, ChatSettingsUpdate, WebhookSettingsUpdate
from typing import Annotated, List

router = APIRouter()

@router.get("/", response_model=List[TriggerListItemResponse])
@inject
async def get_allowed_triggers(
    user: Annotated[User, Depends(get_non_admin_user)],
    trigger_service: Annotated[TriggerService, Depends(Provide[Container.trigger])]
) -> List[TriggerListItemResponse]:
    allowed = trigger_service.get_user_allowed_triggers(
        user_id=user.id
    )
    return [TriggerListItemResponse.model_validate(x) for x in allowed]

@router.get("/all", response_model=List[TriggerListItemResponse])
@inject
async def get_all_triggers(
    _: Annotated[User, Depends(get_admin_user)],
    trigger_service: Annotated[TriggerService, Depends(Provide[Container.trigger])]
) -> List[TriggerListItemResponse]:
    triggers = trigger_service.get_all_triggers()
    return [TriggerListItemResponse.model_validate(x) for x in triggers]

@router.post("/", response_model=TriggerListItemResponse)
@inject
async def create_trigger(
    _: Annotated[User, Depends(get_admin_user)],
    trigger_service: Annotated[TriggerService, Depends(Provide[Container.trigger])],
    body: TriggerCreate
) -> TriggerListItemResponse:
    created_trigger_id = -1
    match body.settings:
        case TimerSettings():
            created_trigger_id = trigger_service.add_timer_trigger(
                name=body.name,
                template=body.template,
                interval=body.settings.interval
            )
        case PollSettings():
            created_trigger_id = trigger_service.add_poll_trigger(
                name=body.name,
                template=body.template,
                interval=body.settings.interval,
                url=body.settings.url
            )
        case ChatSettings():
            created_trigger_id = trigger_service.add_chat_trigger(
                name=body.name,
                template=body.template,
                receiver=body.settings.receiver
            )
        case WebhookSettings():
            created_trigger_id = trigger_service.add_webhook_trigger(
                name=body.name,
                template=body.template,
                endpoint=body.settings.url
            )

    created_trigger = trigger_service.get_trigger_by_id(id=created_trigger_id)
    return TriggerListItemResponse.model_validate(created_trigger)

@router.get("/{id}", response_model=TriggerResponse)
@inject
async def get_trigger(
    id: int,
    _: Annotated[User, Depends(get_admin_user)],
    trigger_service: Annotated[TriggerService, Depends(Provide[Container.trigger])]
) -> TriggerResponse:
    try:
        trigger = trigger_service.get_trigger_by_id(id=id)
        return to_trigger_response(trigger)
    except NonexistentTriggerError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )

@router.put("/{id}")
@inject
async def update_trigger(
    id: int,
    body: TriggerUpdate,
    _: Annotated[User, Depends(get_admin_user)],
    trigger_service: Annotated[TriggerService, Depends(Provide[Container.trigger])]
):
    try:
        existing = trigger_service.get_trigger_by_id(id)
        diff = None

        match (body.settings, existing):
            case (None, _):
                diff = TriggerDiff(
                    name=body.name,
                    template=body.template
                )
            case (TimerSettingsUpdate(type="timer"), _) | (TimerSettingsUpdate(), TimerTrigger()):
                diff = TimerTriggerDiff(
                    name=body.name,
                    template=body.template,
                    interval=body.settings.interval
                )
            case (PollSettingsUpdate(type="poll"), _) | (PollSettingsUpdate(), PollTrigger()):
                diff = PollTriggerDiff(
                    name=body.name,
                    template=body.template,
                    interval=body.settings.interval,
                    url=body.settings.url
                )
            case (ChatSettingsUpdate(type="chat"), _) | (ChatSettingsUpdate(), ChatTrigger()):
                diff = ChatTriggerDiff(
                    name=body.name,
                    template=body.template,
                    receiver=body.settings.receiver
                )
            case (WebhookSettingsUpdate(type="webhook"), _) | (WebhookSettingsUpdate(), WebhookTrigger()):
                diff = WebhookTriggerDiff(
                    name=body.name,
                    template=body.template,
                    endpoint=body.settings.url
                )
            # TODO: Handle the discrimination between update requests better...
            case (TimerSettingsUpdate(), PollTrigger()):
                diff = PollTriggerDiff(
                    name=body.name,
                    template=body.template,
                    interval=body.settings.interval
                )
            case (PollSettingsUpdate(), WebhookTrigger()):
                diff = WebhookTriggerDiff(
                    name=body.name,
                    template=body.template,
                    endpoint=body.settings.url
                )
        
        if diff is not None:
            trigger_service.update_trigger(
                trigger_id=id,
                changes=diff
            )
    except NonexistentTriggerError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )

@router.delete("/{id}")
@inject
async def delete_trigger(
    id: int,
    _: Annotated[User, Depends(get_admin_user)],
    trigger_service: Annotated[TriggerService, Depends(Provide[Container.trigger])]
):
    try:
        trigger_service.remove_trigger(
            id=id
        )
    except NonexistentTriggerError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(err)
        )
