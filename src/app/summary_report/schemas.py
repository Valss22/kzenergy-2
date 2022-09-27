from typing import Optional, Union, Any
from uuid import UUID
from typing import List, Dict
from pydantic.main import BaseModel
from datetime import date

from src.app.report.schemas import User
from src.app.ticket.types import WasteDestination, AggregateState, MeasureSystem


class SummaryReportTicket(BaseModel):
    id: UUID
    facilityName: str
    wasteName: str
    aggregateState: AggregateState
    quantityByMeasureSystem: Dict[MeasureSystem, float]
    quantityByDestinationType: Dict[WasteDestination, Union[float, str]]
    message: Optional[str]
    date: date


class SummaryReportOut(BaseModel):
    id: UUID
    date: date
    user: User
    excel: Optional[str]
    total: Dict[Union[MeasureSystem, WasteDestination], Any]
    tickets: List[SummaryReportTicket]
