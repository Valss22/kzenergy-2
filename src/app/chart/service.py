from src.app.chart.static import LIMIT
from src.app.summary_report.model import SummaryReport
from src.app.ticket.model import Ticket
from src.app.ticket.types import MeasureSystem
from src.app.waste.model import Waste

QUANTITY_BY_MEASURE = {
    MeasureSystem.TON.value: 0,
    MeasureSystem.M3.value: 0,
    MeasureSystem.ITEM.value: 0,
}


class ChartService:

    async def get_lineplot(self):
        repsonse = {}
        for sum_report in await SummaryReport.all():
            for waste in await Waste.all():
                info: list[dict] = []
                qnt_by_measure = {**QUANTITY_BY_MEASURE}
                for ticket in await Ticket.filter(wasteName=waste.name):
                    qnt_by_measure.update({
                        qnt_by_measure[ticket.measureSystem.value]
                        : qnt_by_measure[ticket.measureSystem.value] + ticket.quantity
                    })
                info.append({**qnt_by_measure, "date": sum_report.date})
                repsonse.update({waste.name: info, "limit": LIMIT[waste.name]})
        return repsonse