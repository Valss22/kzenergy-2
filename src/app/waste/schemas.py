from uuid import UUID
from typing import Dict
from pydantic import BaseModel

from src.app.ticket.types import MeasureSystem


class WasteOut(BaseModel):
    id: UUID
    name: str


class UpdateWaste(BaseModel):
    wasteName: str
    quantity: float


class WasteQuantity(BaseModel):
    id: UUID
    name: str
    limit: float
    quantity: Dict[MeasureSystem, float]
