from enum import Enum
from typing import TypedDict


class TypesOfWaste(Enum):
    SOLID = "solid"
    LIQUID = "liquid"


class Waste(TypedDict):
    name: str
    type: TypesOfWaste
    density: float
