from typing import Optional
from uuid import UUID
import datetime
from pydantic.main import BaseModel
from pydantic.utils import to_camel

from src.app.ticket.types import WasteDestinationType, AggregateState, MeasureSystem, TicketStatus


class TicketOut(BaseModel):
    id: UUID
    date: datetime
    waste_destination_type: WasteDestinationType
    aggregate_state: AggregateState
    measure_system: MeasureSystem
    quantity: float
    status: TicketStatus
    excel_url: Optional[str]
    message: Optional[str]

    class Config:
        alias_generator = to_camel
