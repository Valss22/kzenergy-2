from pydantic import BaseModel


class FacilityIn(BaseModel):
    name: str
    wastes: list[str]
