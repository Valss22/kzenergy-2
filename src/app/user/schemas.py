from typing import Union, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, validator

from src.app.user.types import Roles
from src.app.user.validation.schemas.validators import validate_fullname


class LoginUserIn(BaseModel):
    email: EmailStr
    password: str


class RegisterUserIn(LoginUserIn):
    fullname: str
    role: Roles
    phone: str

    @validator("fullname")
    def fullname_format(cls, v: str):
        return validate_fullname(v)


class UserOut(BaseModel):
    id: UUID
    role: Roles
    fullname: str
    email: EmailStr
    phone: str
    token: Optional[str]
