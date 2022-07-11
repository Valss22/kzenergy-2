from uuid import UUID
from datetime import date
from pydantic.main import BaseModel


class User(BaseModel):
    fullname: str


class Ticket(BaseModel):
    id: UUID
    date: date
    wasteName: str


class ReportOut(BaseModel):
    id: UUID
    date: date
    user: User
    tickets: list[Ticket]
