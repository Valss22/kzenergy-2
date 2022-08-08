from fastapi import APIRouter, Depends
from src.app.chart.service import ChartService

chart_router = APIRouter(
    prefix="/stat"
)


@chart_router.get("/lineplot/")
async def get_lineplot(chart_service: ChartService = Depends()):
    return await chart_service.get_lineplot()


@chart_router.get("/barplot/")
async def get_barplot(chart_service: ChartService = Depends()):
    return await chart_service.get_barplot()