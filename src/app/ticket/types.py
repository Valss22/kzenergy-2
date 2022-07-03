from enum import Enum


class AggregateState(Enum):
    SOLID = "Твёрдое"
    LIQUID = "Жидкое"


class MeasureSystem(Enum):
    TON = "тонна"
    M3 = "м3"
    ITEM = "штука"


class WasteDestination(Enum):
    ...
