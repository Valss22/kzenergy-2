from typing import Optional, Union
from uuid import UUID

from pydantic.main import BaseModel
from datetime import date

from src.app.report.schemas import User
from src.app.ticket.types import WasteDestinationType, AggregateState, MeasureSystem


class SummaryReportTicket(BaseModel):
    id: UUID
    facilityName: str
    wasteName: str
    aggregateState: AggregateState
    quantityByMeasureSystem: dict[MeasureSystem, float]
    quantityByDestinationType: dict[WasteDestinationType, float]
    message: Optional[str]
    date: date


class SummaryReportOut(BaseModel):
    id: UUID
    date: date
    user: User
    excel: Optional[str]
    total: dict[Union[MeasureSystem, WasteDestinationType], float]
    tickets: list[SummaryReportTicket]
