from tortoise.exceptions import IntegrityError

from src.app.facility.model import Facility
from src.app.facility.schemas import FacilityIn
from src.app.waste.model import Waste


class FacilityService:
    async def create_facility(self, facility: FacilityIn) -> None:
        facility_dict = facility.dict()
        wastes = facility_dict["wastes"]
        del facility_dict["wastes"]
        facility_obj: Facility = await Facility.create(**facility_dict)
        for waste in wastes:
            try:
                waste_obj = await Waste.create(name=waste)
            except IntegrityError:
                waste_obj = await Waste.get(name=waste)
            await facility_obj.wastes.add(waste_obj)
