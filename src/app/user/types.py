from enum import Enum, unique


@unique
class Roles(Enum):
    ADMIN = "Admin"
    ECOLOGIS = "Ecologist"
    FACILITY_WORKER = "Facility worker"
