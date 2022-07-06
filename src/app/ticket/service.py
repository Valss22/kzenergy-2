from src.app.facility.model import Facility
from src.app.ticket.model import Ticket
from src.app.ticket.schemas import TicketIn
from src.app.user.service import get_current_user
from src.app.waste.model import Waste


class TicketService:
    async def create_ticket(self, ticket: TicketIn, auth_header: str):
        ticket_dict = ticket.dict()
        facility = await Facility.get(id=ticket_dict["facilityId"])
        waste = await Waste.get(name=ticket_dict["wasteName"])
        user = await get_current_user(auth_header)
        del ticket_dict["facilityId"]
        del ticket_dict["wasteName"]
        await Ticket.create(
            **ticket_dict, user=user,
            facility=facility, wasteName=waste.name
        )
