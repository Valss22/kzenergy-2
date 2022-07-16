from typing import Final

from src.app.report.model import Report
from src.app.summary_report.model import SummaryReport
from src.app.summary_report.schemas import SummaryReportOut
from src.app.ticket.model import Ticket
from src.app.ticket.types import TicketStatus, MeasureSystem, WasteDestinationType
from src.app.user.service import get_current_user

QUANTITY_BY_MEASURE: Final[dict] = {
    MeasureSystem.ITEM: 0,
    MeasureSystem.TON: 0,
    MeasureSystem.M3: 0,
}

QUANTITY_BY_DESTINATION: Final[dict] = {
    WasteDestinationType.A: 0,
    WasteDestinationType.B: 0,
    WasteDestinationType.C: 0,
    WasteDestinationType.D: 0,
    WasteDestinationType.E: 0,
}


class SummaryReportService:

    async def create_sum_report(self, auth_header: str):
        user = await get_current_user(auth_header)
        summary_report = await SummaryReport.create(user=user)
        await Report.filter(archived=False).update(summaryReport=summary_report)
        await Report.filter(summaryReport=summary_report).update(archived=True)
        await Ticket.filter(
            archived=False, status=TicketStatus.ACCEPTED.value
        ).update(archived=True)

    async def get_sum_reports(self) -> list[SummaryReportOut]:
        response: list[SummaryReportOut] = []
        sum_reports = await SummaryReport.all().prefetch_related("user")
        print(sum_reports)
        sum_reports = list(reversed(sum_reports))
        tickets_response: list[dict] = []

        for sum_report in sum_reports:
            total_in_sum_report = {**QUANTITY_BY_MEASURE, **QUANTITY_BY_DESTINATION}
            tickets = await Ticket.filter(
                report__summaryReport_id=sum_report.id
            ).prefetch_related("facility")

            for ticket in tickets:
                quantity = ticket.quantity
                ticket_response = {}
                measure_system = ticket.measureSystem
                destination_type = ticket.wasteDestinationType
                quantity_by_measure_system = {**QUANTITY_BY_MEASURE, measure_system: quantity}
                quantity_by_destionation_type = {**QUANTITY_BY_DESTINATION, destination_type: quantity}
                ticket_response.update({
                    **ticket.__dict__,
                    "quantityByMeasureSystem": quantity_by_measure_system,
                    "quantityByDestinationType": quantity_by_destionation_type,
                    "facilityName": ticket.facility.name
                })
                tickets_response.append(ticket_response)
                total_in_sum_report[measure_system] += quantity
                total_in_sum_report[destination_type] += quantity

            response.append(SummaryReportOut(
                **sum_report.__dict__,
                user=sum_report.user,
                total=total_in_sum_report,
                tickets=tickets_response,
            ))
        return response
