from src.app.report.model import Report
from src.app.summary_report.model import SummaryReport
from src.app.ticket.model import Ticket
from src.app.ticket.types import TicketStatus
from src.app.user.service import get_current_user


class SummaryReportService:
    async def get_facilities_with_reports(self) -> dict[str, list]:
        pass

    async def create_sum_report(self, auth_header: str):
        user = await get_current_user(auth_header)
        summary_report = await SummaryReport.create(user=user)
        await Report.filter(archived=False).update(summaryReport=summary_report)
        await Report.filter(summaryReport=summary_report).update(archived=True)
        await Ticket.filter(
            archived=False, status=TicketStatus.ACCEPTED.value
        ).update(archived=True)

    async def get_sum_report(self):
        response = []
        sum_reports = await SummaryReport.all()
        for sum_report in sum_reports:
            tickets = await Ticket.filter(report__summaryReport_id=sum_report.id)
            for ticket in tickets:
                destination_type = ticket.wasteDestinationType.value
                measure_system = ticket.measureSystem.value
                quantity_by_measure_system = {measure_system: ticket.quantity}
