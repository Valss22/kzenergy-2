from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from src.app.report.schemas import ReportOut
from src.app.settings import to_camel
from src.app.ticket.schemas import TicketOut
from src.app.waste.schemas import WasteOut
from typing import List, Dict

class FacilityIn(BaseModel):
    name: str
    wastes: List[str]


class FacilityOut(BaseModel):
    id: UUID
    name: str
    wastes: List[WasteOut]


class FacilityTicketsOut(BaseModel):
    report: Optional[ReportOut]
    tickets: List[TicketOut]


class Report(ReportOut):
    facilityName: str


class FacilityTotalOut(BaseModel):
    reports: List[Report]
    tickets: Dict[str, List[TicketOut]]
    facility_number: int

    class Config:
        alias_generator = to_camel
