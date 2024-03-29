from tortoise.exceptions import IntegrityError
from src.app.facility.model import Facility
from src.app.facility.schemas import FacilityIn, FacilityTicketsOut, FacilityTotalOut
from src.app.report.model import Report
from src.app.ticket.model import Ticket
from src.app.waste.model import Waste
from typing import List, Dict


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

    async def get_facility_tickets(self, facility_id: str):
        tickets = await Ticket.filter(
            facility__id=facility_id,
            archived=False
        )
        for ticket in tickets:
            ticket.usedInReport = bool(ticket.report)  # type: ignore
            await ticket.save(update_fields=["usedInReport"])
        try:
            report = await Report.filter(  # type: ignore
                tickets__facility_id=facility_id,
                archived=False
            ).prefetch_related("user").first()
            report_tickets = await Ticket.filter(report_id=report.id)  # type: ignore
            report = {  # type: ignore
                **report.__dict__,
                "user": report.user,  # type: ignore
                "tickets": report_tickets
            }
        except:
            report = None

        return FacilityTicketsOut(
            report=report,
            tickets=tickets
        )

    async def get_facility_total(self):
        reports_objs = await Report.filter(  # type: ignore
            archived=False
        ).prefetch_related("user").order_by("-date")
        try:
            reports = []
            for report in reports_objs:
                report_tickets = await report.tickets.all().first()
                report_facility = await report_tickets.facility
                facility_name = report_facility.name

                report_tickets = await Ticket.filter(report_id=report.id).order_by("id")

                reports.append({
                    **report.__dict__, "user": report.user,
                    "tickets": report_tickets,
                    "facilityName": facility_name})

        except AttributeError:
            reports = []

        tickets_objs = await Ticket.filter(
            archived=False
        ).prefetch_related("facility").order_by("id")

        for ticket_obj in tickets_objs:
            ticket_obj.usedInReport = bool(ticket_obj.report)
            await ticket_obj.save(update_fields=["usedInReport"])

        tickets: Dict[str, List[Ticket]] = {}

        for ticket in tickets_objs:
            facility_name = ticket.facility.name
            facility_tickets = await Ticket.filter(
                facility__name=facility_name,
                archived=False
            ).prefetch_related("facility").order_by("id")

            tickets[facility_name] = facility_tickets

        facility_number = await Facility.all().count()

        return FacilityTotalOut(
            reports=reports,
            tickets=tickets,
            facilityNumber=facility_number
        )

    async def delete_facility(self, facility_id: str):
        await Facility.filter(id=facility_id).delete()
