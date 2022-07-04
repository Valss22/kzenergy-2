from uuid import UUID
from pydantic import BaseModel

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
    permission_to_report: bool
    tickets: list[TicketOut]

    class Config:
        alias_generator = to_camel
