from src.app.facility.model import Facility
from src.app.ticket.model import Ticket
from src.app.ticket.schemas import TicketIn, TicketPatchIn
from src.app.user.service import get_current_user


class TicketService:
    async def create_ticket(self, ticket: TicketIn, auth_header: str):
        ticket_dict = ticket.dict()
        facility = await Facility.get(id=ticket_dict["facilityId"])
        user = await get_current_user(auth_header)
        del ticket_dict["facilityId"]
        await Ticket.create(**ticket_dict, user=user, facility=facility)

    async def update_ticket(self, ticket_id: str, ticket: TicketPatchIn):
        await Ticket.filter(id=ticket_id).update(**ticket.dict())
