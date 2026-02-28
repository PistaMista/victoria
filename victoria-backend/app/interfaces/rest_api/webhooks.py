from fastapi import APIRouter, status, HTTPException, Depends, Request
from dependency_injector.wiring import inject, Provide
from app.services.trigger import TriggerService, InvalidWebhookEndpointError
from app.containers import Container
from typing import Annotated

router = APIRouter()


@router.post("/{endpoint:path}")
@inject
async def receive_webhook_payload(
    endpoint: str,
    request: Request,
    trigger_service: Annotated[TriggerService, Depends(Provide[Container.trigger])],
):
    try:
        body = await request.body()
        content = body.decode("utf-8")
        trigger_service.receive_webhook_payload(endpoint=endpoint, content=content)
    except InvalidWebhookEndpointError as err:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(err))
