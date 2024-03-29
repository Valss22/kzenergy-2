from typing import Optional
from uuid import UUID
from datetime import date
from pydantic.main import BaseModel
from src.app.ticket.types import WasteDestination, AggregateState, MeasureSystem, TicketStatus


# FIXME: не дублировать поля в схемах
class TicketIn(BaseModel):
    facilityId: str
    wasteName: str
    wasteDestinationType: WasteDestination
    aggregateState: AggregateState
    measureSystem: MeasureSystem
    quantity: float


class TicketPatchIn(BaseModel):
    status: TicketStatus
    message: Optional[str]
    wasteName: Optional[str]
    wasteDestinationType: Optional[WasteDestination]
    aggregateState: Optional[AggregateState]
    measureSystem: Optional[MeasureSystem]
    quantity: Optional[float]


class TicketOut(BaseModel):
    id: UUID
    date: date
    wasteName: str
    wasteDestinationType: WasteDestination
    aggregateState: AggregateState
    measureSystem: MeasureSystem
    quantity: float
    status: TicketStatus
    excelUrl: Optional[str]
    message: Optional[str]
    usedInReport: bool
