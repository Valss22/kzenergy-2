from fastapi import APIRouter, Depends, Header

from src.app.ticket.schemas import TicketIn
from src.app.ticket.service import TicketService

ticket_router = APIRouter()
TICKET_ENDPOINT = "/facility/ticket/"


@ticket_router.post(TICKET_ENDPOINT, )
async def create_ticket(
    ticket: TicketIn,
    Authorization: str = Header(...),
    ticket_service: TicketService = Depends()
):
    return await ticket_service.create_ticket(ticket, Authorization)
