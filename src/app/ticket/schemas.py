from typing import Optional
from uuid import UUID
from datetime import date

from pydantic import Field
from pydantic.main import BaseModel
from src.app.ticket.types import WasteDestinationType, AggregateState, MeasureSystem, TicketStatus


class TicketOut(BaseModel):
    id: UUID
    date: date
    wasteDestinationType: WasteDestinationType
    aggregateState: AggregateState
    measureSystem: MeasureSystem
    quantity: float
    status: TicketStatus
    excelUrl: Optional[str] = Field(alias="excel")
    message: Optional[str]
