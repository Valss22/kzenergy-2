from tortoise.exceptions import IntegrityError

from src.app.facility.model import Facility
from src.app.facility.schemas import FacilityIn, FacilityOut
from src.app.report.model import Report
from src.app.ticket.model import Ticket
from src.app.waste.model import Waste


class FacilityService:
    async def create_facility(self, facility: FacilityIn):
        facility_dict = facility.dict()
        wastes = facility_dict["wastes"]
        del facility_dict["wastes"]

        facility_obj = await Facility.create(**facility_dict)

        for waste in wastes:
            try:
                waste_obj = await Waste.create(name=waste)
            except IntegrityError:
                waste_obj = await Waste.get(name=waste)
            await facility_obj.wastes.add(waste_obj)

    async def get_facilities(self):
        facilities = await Facility.all().prefetch_related("wastes")
        response = []

        for facility in facilities:
            wastes = []
            for waste in facility.wastes.related_objects:
                wastes.append(waste)
            response.append({**facility.__dict__, "wastes": wastes})

        return response

    async def get_facility_info(self, facility_id: str):
        tickets = await Ticket.filter(
            facility__id=facility_id,
            archived=False
        )
        try:
            permission_to_report = bool(await Report.tickets.filter(
                archived=False,
                facility__id=facility_id
            ))
        except AttributeError:
            permission_to_report = True

        return {
            "permissionToReport": permission_to_report,
            "tickets": tickets
        }

    async def delete_facility(self, facility_id: str):
        await Facility.filter(id=facility_id).delete()
