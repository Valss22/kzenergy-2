from src.app.chart.static import LIMIT
from src.app.summary_report.model import SummaryReport
from src.app.ticket.model import Ticket
from src.app.ticket.types import MeasureSystem
from src.app.waste.model import Waste

QUANTITY_BY_MEASURE = {
    MeasureSystem.TON: 0,
    MeasureSystem.M3: 0,
    MeasureSystem.ITEM: 0,
}


class ChartService:

    async def get_lineplot(self):
        repsonse = {}

        for waste in await Waste.all():
            info: list[dict] = []
            for sum_report in await SummaryReport.all():
                qnt_by_measure = {**QUANTITY_BY_MEASURE}
                for ticket in await Ticket.filter(
                    wasteName=waste.name,
                    report__summaryReport_id=sum_report.id
                ):
                    qnt_by_measure.update({
                        ticket.measureSystem: qnt_by_measure[ticket.measureSystem] + ticket.quantity
                    })
                info.append({**qnt_by_measure, "date": sum_report.date})
            repsonse.update({waste.name: {"limit": LIMIT[waste.name], "info": info}})
        return repsonse
