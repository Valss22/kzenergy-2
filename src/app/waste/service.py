from src.app.chart.static import LIMIT
from src.app.summary_report.service import QUANTITY_BY_MEASURE
from src.app.ticket.model import Ticket
from src.app.ticket.types import TicketStatus
from src.app.waste.model import Waste
from src.app.waste.schemas import UpdateWaste
from typing import List


class WasteService:

    async def get_wastes_quantity(self):
        wastes: List[dict] = []
        for waste in await Waste.all():
            quantity = {**QUANTITY_BY_MEASURE}
            for ticket in await Ticket.filter(
                wasteName=waste.name, archived=False,
                status=TicketStatus.ACCEPTED.value
            ):
                quantity.update({ticket.measureSystem: quantity[ticket.measureSystem] + ticket.quantity})
            wastes.append({
                "id": waste.id, "name": waste.name,
                "limit": LIMIT[waste.name], "quantity": quantity
            })
        return wastes

    def update_waste_limit(self, waste: UpdateWaste):
        LIMIT.update({waste.dict()["wasteName"]: waste.dict()["quantity"]})
