from typing import TypedDict

from src.app.ticket.types import AggregateState


class Waste(TypedDict):
    name: str
    type: AggregateState
    density: float
