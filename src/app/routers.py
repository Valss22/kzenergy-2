from fastapi import APIRouter

from src.app.facility.controller import facility_router
from src.app.ticket.controller import ticket_router
from src.app.user.controller import user_router

api_router = APIRouter()
api_router.include_router(user_router)
api_router.include_router(facility_router)
api_router.include_router(ticket_router)
