from pydantic import BaseModel

from src.app.waste.types import Waste


class CreateFacilityIn(BaseModel):
    name: str
    description: str
    wastes: list[Waste]
