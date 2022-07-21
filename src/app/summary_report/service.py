from datetime import date
from typing import Final
import cloudinary.uploader as cloud
from src.app.facility.model import Facility
from src.app.report.model import Report
from src.app.summary_report.excel.service import write_excel_sum_report
from src.app.summary_report.excel.types import Excel
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
    WasteDestinationType.BURIED: 0,
    WasteDestinationType.UTILIZIED: 0,
    WasteDestinationType.RECYCLED: 0,
    WasteDestinationType.TRANSMITTED: 0,
    WasteDestinationType.REUSED: 0,
}

TOTAL_FIELD: Final[dict] = {
    MeasureSystem.TON.name: 0,
    MeasureSystem.M3.name: 0,
    MeasureSystem.ITEM.name: 0,
    WasteDestinationType.BURIED.name: 0,
    WasteDestinationType.UTILIZIED.name: 0,
    WasteDestinationType.RECYCLED.name: 0,
    WasteDestinationType.TRANSMITTED.name: 0,
    WasteDestinationType.REUSED.name: 0,
}


class SummaryReportService:

    async def prepare_excel_data(self, reports: list[Report]) -> list[Excel]:
        excel_data = []
        wastes = []
        for fac in await Facility.all():
            fac_name = fac.name
            for report in reports:
                for ticket in await report.tickets.all():
                    wastes.append({
                        "name": ticket.wasteName,
                        "aggregate_state": ticket.aggregateState.value,
                        **TOTAL_FIELD,
                        ticket.measureSystem.name: ticket.quantity,
                        ticket.wasteDestinationType.name: ticket.quantity,
                        "comment": ticket.message,
                        "date": str(ticket.date)
                    })
            excel_data.append({"facility": {"name": fac_name, "wastes": wastes}})
        return excel_data

    async def create_sum_report(self, auth_header: str):
        user = await get_current_user(auth_header)

        reports = await Report.filter(archived=False)

        excel_data = await self.prepare_excel_data(reports)
        await write_excel_sum_report(excel_data, date.today(), user.fullname)
        excel_url = cloud.upload("sum_report.xlsx", resource_type="auto")["secure_url"]
        summary_report = await SummaryReport.create(user=user, excel=excel_url)

        await Report.filter(archived=False).update(summaryReport=summary_report)
        await Report.filter(summaryReport=summary_report).update(archived=True)
        await Ticket.filter(
            archived=False, status=TicketStatus.ACCEPTED.value
        ).update(archived=True)

    async def get_sum_reports(self) -> list[SummaryReportOut]:
        response: list[SummaryReportOut] = []
        sum_reports = await SummaryReport.all().prefetch_related("user")
        sum_reports = list(reversed(sum_reports))

        for sum_report in sum_reports:
            total_in_sum_report = {**QUANTITY_BY_MEASURE, **QUANTITY_BY_DESTINATION}
            tickets_response: list[dict] = []

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
                excel=sum_report.excel
            ))
        return response
