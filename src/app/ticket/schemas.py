from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import Field
from pydantic.main import BaseModel

from src.app.settings import to_camel
from src.app.ticket.types import WasteDestinationType, AggregateState, MeasureSystem, TicketStatus


class TicketOut(BaseModel):
    id: UUID
    date: datetime
    waste_destination_type: WasteDestinationType
    aggregate_state: AggregateState
    measure_system: MeasureSystem
    quantity: float
    status: TicketStatus
    excel_url: Optional[str] = Field(alias="excel")
    message: Optional[str]

    class Config:
        alias_generator = to_camel
