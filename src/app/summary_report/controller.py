from fastapi import APIRouter

summary_report = APIRouter()
SUMMARY_REPORT_ENDPOINT = "/summary/"


@summary_report.post(SUMMARY_REPORT_ENDPOINT)
async def create_sum_report():
    pass
