from pydantic import BaseModel

from src.app.waste.types import Waste


class FacilityIn(BaseModel):
    name: str
    wastes: list[Waste]
