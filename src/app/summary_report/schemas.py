from typing import Optional, Union, Any
from uuid import UUID

from pydantic.main import BaseModel
from datetime import date

from src.app.report.schemas import User
from src.app.ticket.types import WasteDestination, AggregateState, MeasureSystem


class SummaryReportTicket(BaseModel):
    id: UUID
    facilityName: str
    wasteName: str
    aggregateState: AggregateState
    quantityByMeasureSystem: dict[MeasureSystem, float]
    quantityByDestinationType: dict[WasteDestination, Union[float, str]]
    message: Optional[str]
    date: date


class SummaryReportOut(BaseModel):
    id: UUID
    date: date
    user: User
    excel: Optional[str]
    total: dict[Union[MeasureSystem, WasteDestination], Any]
    tickets: list[SummaryReportTicket]
