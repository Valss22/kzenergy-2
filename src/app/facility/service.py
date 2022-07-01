from src.app.facility.model import Facility
from src.app.facility.schemas import FacilityIn


class FacilityService:
    async def create_facility(self, facility: FacilityIn):
        pass
        #await Facility.create()
