from pydantic import BaseModel
from app.interfaces.rest_api.schema.exchanges import ExchangeResponse
from typing import Literal, List


class InitialExchangesEvent(BaseModel):
    type: Literal["initial"] = "initial"
    exchanges: List[ExchangeResponse]


class NewExchangeEvent(BaseModel):
    type: Literal["new"] = "new"
    exchange: ExchangeResponse
