from fastapi import APIRouter

ticket_router = APIRouter()
TICKET_ENDPOINT = "/ticket/"


@ticket_router.post(TICKET_ENDPOINT, )
async def create_ticket():
    ...
