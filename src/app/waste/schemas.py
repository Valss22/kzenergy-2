from uuid import UUID

from pydantic import BaseModel


class WasteOut(BaseModel):
    id: UUID
    name: str
