from enum import Enum, unique


@unique
class Role(Enum):
    ADMIN = "Админ"
    ECOLOGIS = "Эколог"
    FACILITY_WORKER = "Работник объекта"
