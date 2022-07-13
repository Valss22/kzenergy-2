from typing import Optional, Union
from uuid import UUID

from pydantic.main import BaseModel
from datetime import date

from src.app.report.schemas import User
from src.app.ticket.types import WasteDestinationType, AggregateState, MeasureSystem


class SummaryReportTicket(BaseModel):
    id: UUID
    date: date
    facilityName: str
    wasteName: str
    aggregateState: AggregateState
    message: Optional[str]
    quantityByMeasureSystem: dict[MeasureSystem, float]
    quantityByDestinationType: dict[WasteDestinationType, float]


class SummaryReportOut(BaseModel):
    id: UUID
    date: date
    user: User
    total: dict[Union[MeasureSystem, WasteDestinationType], float]
    tickets: list[SummaryReportTicket]
