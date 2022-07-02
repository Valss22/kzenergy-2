from enum import Enum, unique


@unique
class UserRole(Enum):
    ADMIN = "Админ"
    ECOLOGIS = "Эколог"
    FACILITY_WORKER = "Работник объекта"
