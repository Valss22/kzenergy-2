from uuid import UUID

from pydantic import BaseModel


class WasteSchema(BaseModel):
    id: UUID
    name: str
