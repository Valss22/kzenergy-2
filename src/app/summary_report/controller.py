from fastapi import APIRouter, Header, Depends
from typing import List
from src.app.summary_report.schemas import SummaryReportOut
from src.app.summary_report.service import SummaryReportService

summary_report_router = APIRouter()
SUMMARY_REPORT_ENDPOINT = "/facility/summary/"


@summary_report_router.post(SUMMARY_REPORT_ENDPOINT)
async def create_sum_report(
    Authorization: str = Header(...),
    summary_report_service: SummaryReportService = Depends()
):
    return await summary_report_service.create_sum_report(Authorization)


@summary_report_router.get("/archive/summary/", response_model=List[SummaryReportOut])
async def get_sum_report(
    summary_report_service: SummaryReportService = Depends()
):
    return await summary_report_service.get_sum_reports()
