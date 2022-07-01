from enum import Enum
from typing import TypedDict


class AggregateState(Enum):
    SOLID = "Твёрдое"
    LIQUID = "Жидкое"


class Waste(TypedDict):
    name: str
    type: AggregateState
    density: float
