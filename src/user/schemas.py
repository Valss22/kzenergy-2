from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, validator

from src.user.validation.schemas.validators import validate_fullname


class UserIn(BaseModel):
    fullname: str
    email: EmailStr
    phone: str
    password: Optional[str]

    @validator("fullname")
    def fullname_format(cls, v: str):
        return validate_fullname(v)


class UserOut(BaseModel):
    id: UUID
    fullname: str
    email: EmailStr
    phone: str
    token: str
    is_admin: bool = Field(alias="isAdmin")
