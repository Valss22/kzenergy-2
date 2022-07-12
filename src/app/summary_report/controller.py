from fastapi import APIRouter, Header, Depends

from src.app.summary_report.service import SummaryReportService

summary_report_router = APIRouter()
SUMMARY_REPORT_ENDPOINT = "/facility/summary/"


@summary_report_router.post(SUMMARY_REPORT_ENDPOINT)
async def create_sum_report(
    Authorization: str = Header(),
    summary_report_service: SummaryReportService = Depends()
):
    return await summary_report_service.create_sum_report(Authorization)
