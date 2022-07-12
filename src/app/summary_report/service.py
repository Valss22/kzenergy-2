from src.app.report.model import Report
from src.app.summary_report.model import SummaryReport
from src.app.user.service import get_current_user


class SummaryReportService:
    async def get_facilities_with_reports(self) -> dict[str, list]:
        pass

    async def create_sum_report(self, auth_header: str):
        user = await get_current_user(auth_header)
        summary_report = await SummaryReport.create(user=user)
        await Report.filter(archived=False).update(summaryReport=summary_report)
