from src.app.report.model import Report
from src.app.ticket.model import Ticket
from src.app.user.service import get_current_user


class ReportService:

    async def create_report(self, facility_id: str, auth_header: str):
        user = await get_current_user(auth_header)
        report = await Report.create(user=user)
        await Ticket.filter(
            facility_id=facility_id,
            archived=False
        ).update(report=report)
