from uuid import UUID
from pydantic import BaseModel, EmailStr, validator

from src.app.user.types import UserRole
from src.app.user.validation.schemas.validators import validate_fullname


class UserLoginIn(BaseModel):
    email: EmailStr
    password: str
 

class UserRegisterIn(UserLoginIn):
    fullname: str
    role: UserRole
    phone: str

    @validator("fullname")
    def fullname_format(cls, v: str):
        return validate_fullname(v)


class UserOut(BaseModel):
    id: UUID
    role: UserRole
    fullname: str
    email: EmailStr
    phone: str
    token: str


class UserPermissionPatch(BaseModel):
    write: bool
    read: bool
