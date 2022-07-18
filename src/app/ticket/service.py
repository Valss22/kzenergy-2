from src.app.facility.model import Facility
from src.app.ticket.excel.service import write_ticket_to_excel
from src.app.ticket.model import Ticket
from src.app.ticket.schemas import TicketIn
from src.app.ticket.types import TicketStatus
from src.app.user.service import get_current_user
import cloudinary.uploader as cloud


class TicketService:
    async def create_ticket(self, ticket: TicketIn, auth_header: str):
        ticket_dict = ticket.dict()
        facility = await Facility.get(id=ticket_dict["facilityId"])
        user = await get_current_user(auth_header)
        del ticket_dict["facilityId"]
        await Ticket.create(**ticket_dict, user=user, facility=facility)

    async def update_ticket(self, ticket_id: str, ticket_body):
        await Ticket.filter(id=ticket_id).update(**ticket_body)
        ticket = await Ticket.get(id=ticket_id)
        try:
            if ticket_body["status"] == TicketStatus.ACCEPTED.value:
                await write_ticket_to_excel(ticket)
                excel_url = cloud.upload("ticket.xlsx", resourse_type="auto")
                excel_url = excel_url["secure_url"]
                await Ticket.filter(id=ticket_id).update(excelUrl=excel_url)
        except KeyError:
            pass
