from enum import Enum, unique


@unique
class Roles(Enum):
    ECOLOGIS = "Ecologist"
    FACILITY_WORKER_1 = "Facility worker 1"
    FACILITY_WORKER_2 = "Facility worker 2"
    FACILITY_WORKER_3 = "Facility worker 3"
    ADMIN = "Admin"


