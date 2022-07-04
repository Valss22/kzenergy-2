from uuid import UUID
from datetime import datetime

from pydantic import Field
from pydantic.main import BaseModel


class ReportOut(BaseModel):
    id: UUID
    date: datetime
    excel_url: str = Field(alias="excel")