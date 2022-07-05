from uuid import UUID
from datetime import datetime
from pydantic.main import BaseModel


class ReportOut(BaseModel):
    id: UUID
    date: datetime
