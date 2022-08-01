from enum import Enum


class AggregateState(Enum):
    SOLID = "Твёрдое"
    LIQUID = "Жидкое"


class MeasureSystem(Enum):
    TON = "тонна"
    M3 = "м3"
    ITEM = "штука"


class WasteDestination(Enum):
    BURIED = "Захоронение"
    UTILIZIED = "Утилизация"
    RECYCLED = "Переработка"
    TRANSMITTED = "Передача подрядческой организации"
    REUSED = "Повторное использование"


class TicketStatus(Enum):
    ACCEPTED = "Принят"
    REJECTED = "Отклонён"
    PENDING = "В ожидании"
