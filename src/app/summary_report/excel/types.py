from typing import TypedDict


class TotalField(TypedDict):
    TON: float
    M3: float
    ITEM: int
    BURIED: float
    UTILIZIED: float
    RECYCLED: float
    TRANSMITTED: float
    REUSED: float


class Waste(TotalField):
    name: str
    aggregate_state: str
    comment: str
    date: str


class Facility(TypedDict):
    name: str
    wastes: list[Waste]


class Excel(Facility):
    facility: Facility
    total: TotalField
