from uuid import UUID

from pydantic import BaseModel

from src.app.waste.schemas import WasteSchema


class FacilityIn(BaseModel):
    name: str
    wastes: list[str]


class FacilityOut(FacilityIn):
    id: UUID
    wastes: list[WasteSchema]
