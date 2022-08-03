from fastapi import APIRouter, Depends

from src.app.chart.service import ChartService
from src.app.chart.shemas import Lineplot

chart_router = APIRouter(
    prefix="/stat"
)


@chart_router.get("/lineplot/", response_model=Lineplot)
async def get_lineplot(chart_service: ChartService = Depends()):
    return await chart_service.get_lineplot()