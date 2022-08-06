from uuid import UUID

from pydantic import BaseModel

from src.app.ticket.types import MeasureSystem


class WasteOut(BaseModel):
    id: UUID
    name: str


class WasteQuantity(BaseModel):
    id: UUID
    name: str
    limit: float
    quantity: dict[MeasureSystem, float]

