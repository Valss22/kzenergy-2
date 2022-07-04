from enum import Enum


class AggregateState(Enum):
    SOLID = "Твёрдое"
    LIQUID = "Жидкое"


class MeasureSystem(Enum):
    TON = "тонна"
    M3 = "м3"
    ITEM = "штука"


class WasteDestinationType(Enum):
    A = "Захоронение"
    B = "Утилизация"
    C = "Переработка"
    D = "Передача подрядческой организации"
    E = "Повторное использование"


class TicketStatus(Enum):
    ACCEPTED = "Принят"
    REJECTED = "Отклонён"
    PENDING = "В ожидании"
