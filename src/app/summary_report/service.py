from typing import Final
import cloudinary.uploader as cloud
from src.app.report.model import Report
from src.app.summary_report.excel.service import write_excel_sum_report
from src.app.summary_report.model import SummaryReport
from src.app.summary_report.schemas import SummaryReportOut
from src.app.ticket.model import Ticket
from src.app.ticket.types import TicketStatus, MeasureSystem, WasteDestinationType
from src.app.user.service import get_current_user

QUANTITY_BY_MEASURE: Final[dict] = {
    MeasureSystem.TON: 0,
    MeasureSystem.M3: 0,
    MeasureSystem.ITEM: 0,
}

QUANTITY_BY_DESTINATION: Final[dict] = {
    WasteDestinationType.BURIED: 0,
    WasteDestinationType.UTILIZIED: 0,
    WasteDestinationType.RECYCLED: 0,
    WasteDestinationType.TRANSMITTED: 0,
    WasteDestinationType.REUSED: 0,
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
        sum_reports: list[SummaryReportOut] = await self.get_sum_reports()
        await write_excel_sum_report(sum_reports[-1])
        excel_url = cloud.upload("sum_report.xlsx", resource_type="auto")["secure_url"]
        await SummaryReport.filter(user=user).update(excel=excel_url)

    async def get_sum_reports(self) -> list[SummaryReportOut]:
        response: list[SummaryReportOut] = []
        sum_reports = await SummaryReport.all().prefetch_related("user")
        sum_reports = list(reversed(sum_reports))

        for sum_report in sum_reports:
            total_in_sum_report = {**QUANTITY_BY_MEASURE, **QUANTITY_BY_DESTINATION}
            tickets_response: list[dict] = []

            tickets = await Ticket.filter(
                report__summaryReport_id=sum_report.id
            ).prefetch_related("facility").order_by("facility_id")

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
