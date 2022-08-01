from typing import Final, Union
import cloudinary.uploader as cloud
from src.app.report.model import Report
from src.app.summary_report.excel.service import write_excel_sum_report
from src.app.summary_report.model import SummaryReport
from src.app.summary_report.schemas import SummaryReportOut
from src.app.ticket.model import Ticket
from src.app.ticket.types import TicketStatus, MeasureSystem, WasteDestination
from src.app.user.service import get_current_user

QUANTITY_BY_MEASURE: Final[dict] = {
    MeasureSystem.TON: 0,
    MeasureSystem.M3: 0,
    MeasureSystem.ITEM: 0,
}
QNT_BY_DEST: dict[WasteDestination, float] = {
    WasteDestination.BURIED: 0,
    WasteDestination.UTILIZIED: 0,
    WasteDestination.RECYCLED: 0,
    WasteDestination.TRANSMITTED: 0,
    WasteDestination.REUSED: 0,
}

qnt_by_dest: dict[WasteDestination, Union[list, str]] = {
    WasteDestination.BURIED: [0, 0, 0],
    WasteDestination.UTILIZIED: [0, 0, 0],
    WasteDestination.RECYCLED: [0, 0, 0],
    WasteDestination.TRANSMITTED: [0, 0, 0],
    WasteDestination.REUSED: [0, 0, 0],
}

qnt_str_by_dest: dict[WasteDestination, Union[list, str]] = {
    WasteDestination.BURIED: "0 т. + 0 м3 + 0 шт.",
    WasteDestination.UTILIZIED: "0 т. + 0 м3 + 0 шт.",
    WasteDestination.RECYCLED: "0 т. + 0 м3 + 0 шт.",
    WasteDestination.TRANSMITTED: "0 т. + 0 м3 + 0 шт.",
    WasteDestination.REUSED: "0 т. + 0 м3 + 0 шт.",
}


def calc_each_measure_values(dest_type: WasteDestination, measure_system: MeasureSystem, quantity: float):
    if measure_system == MeasureSystem.TON:
        qnt_by_dest.update({dest_type: [qnt_by_dest[dest_type][0] + quantity, 0, 0]})
        waste_dest_values: list = qnt_by_dest[dest_type]
        qnt_str_by_dest.update({
            dest_type: f"{waste_dest_values[0]} т."
                       f" + {waste_dest_values[1]} м3 +"
                       f" {waste_dest_values[2]} шт."
        })
    elif measure_system == MeasureSystem.M3:
        qnt_by_dest.update({dest_type: [0, qnt_by_dest[dest_type][1] + quantity, 0]})
        waste_dest_values: list = qnt_by_dest[dest_type]
        qnt_str_by_dest.update({
            dest_type: f"{waste_dest_values[0]} т."
                       f" + {waste_dest_values[1]} м3 +"
                       f" {waste_dest_values[2]} шт."
        })
    else:
        qnt_by_dest.update({dest_type: [0, 0, qnt_by_dest[dest_type][2] + quantity]})
        waste_dest_values: list = qnt_by_dest[dest_type]
        qnt_str_by_dest.update({
            dest_type: f"{waste_dest_values[0]} т."
                       f" + {waste_dest_values[1]} м3 +"
                       f" {waste_dest_values[2]} шт."
        })


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
            total_in_sum_report = {**QUANTITY_BY_MEASURE}
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
                calc_each_measure_values(destination_type, measure_system, quantity)
                ticket_response.update({
                    **ticket.__dict__,
                    "quantityByMeasureSystem": quantity_by_measure_system,
                    "quantityByDestinationType": {**QNT_BY_DEST, destination_type: quantity},
                    "facilityName": ticket.facility.name
                })
                tickets_response.append(ticket_response)
                total_in_sum_report[measure_system] += quantity

            total_in_sum_report.update({**qnt_str_by_dest})
            response.append(SummaryReportOut(
                **sum_report.__dict__,
                user=sum_report.user,
                total=total_in_sum_report,
                tickets=tickets_response,
            ))
        return response
