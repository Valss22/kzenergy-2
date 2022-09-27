from uuid import UUID
from datetime import date
from pydantic.main import BaseModel
from typing import List
from src.app.ticket.types import TicketStatus


class User(BaseModel):
    fullname: str


class Ticket(BaseModel):
    id: UUID
    date: date
    wasteName: str
    status: TicketStatus


class ReportOut(BaseModel):
    id: UUID
    date: date
    user: User
    tickets: List[Ticket]
