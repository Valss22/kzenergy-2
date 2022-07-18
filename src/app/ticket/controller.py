from fastapi import APIRouter, Depends, Header, Body

from src.app.ticket.schemas import TicketIn
from src.app.ticket.service import TicketService

ticket_router = APIRouter()
TICKET_ENDPOINT = "/facility/ticket/"


@ticket_router.post(TICKET_ENDPOINT)
async def create_ticket(
    ticket: TicketIn,
    Authorization: str = Header(...),
    ticket_service: TicketService = Depends()
):
    return await ticket_service.create_ticket(ticket, Authorization)


@ticket_router.patch(TICKET_ENDPOINT + "{ticket_id}")
async def update_ticket(
    ticket_id: str,
    ticket_body=Body(...),
    ticket_service: TicketService = Depends()
):
    return await ticket_service.update_ticket(ticket_id, ticket_body)
