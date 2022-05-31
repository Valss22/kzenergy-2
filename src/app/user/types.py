from enum import Enum, unique


@unique
class Roles(Enum):
    ROLE_1 = "Ecologist"
    ROLE_2 = "Facility worker 1"
    ROLE_3 = "Facility worker 2"
    ROLE_4 = "Facility worker 3"
    ROLE_5 = "Admin"
