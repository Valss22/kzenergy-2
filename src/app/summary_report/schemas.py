from pydantic import BaseModel

from src.app.settings import to_camel


class SummaryReportIn(BaseModel):
    reports_id: list[str]

    class Config:
        alias_generator = to_camel
