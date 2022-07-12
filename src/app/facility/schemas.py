from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from src.app.report.schemas import ReportOut
from src.app.settings import to_camel
from src.app.ticket.schemas import TicketOut
from src.app.waste.schemas import WasteOut


class FacilityIn(BaseModel):
    name: str
    wastes: list[str]


class FacilityOut(BaseModel):
    id: UUID
    name: str
    wastes: list[WasteOut]


class FacilityTicketsOut(BaseModel):
    report: Optional[ReportOut]
    tickets: list[TicketOut]


class Report(ReportOut):
    facilityName: str


class FacilityTotalOut(BaseModel):
    reports: list[Optional[Report]]
    tickets: dict[str, list[TicketOut]]
    facility_number: int

    class Config:
        alias_generator = to_camel
