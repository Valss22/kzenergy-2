from fastapi import APIRouter, Depends, Header

from src.app.report.service import ReportService

report_router = APIRouter()
REPORT_ENDPOINT = "/facility/{facility_id}/report/"


@report_router.post(REPORT_ENDPOINT)
async def create_report(
    facility_id: str,
    Authorization: str = Header(...),
    report_service: ReportService = Depends()
):
    return await report_service.create_report(facility_id, Authorization)
