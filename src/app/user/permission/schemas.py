from uuid import UUID
from pydantic import EmailStr
from pydantic.main import BaseModel
from src.app.user.types import UserRole


class UserPermission(BaseModel):
    write: bool
    read: bool


class TempUserIn(UserPermission):
    email: EmailStr
    role: UserRole
    temporary: bool


class PermanentUser(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole
    permission: UserPermission
    temporary: bool


class TemporaryUser(PermanentUser):
    id: UUID
    email: EmailStr
    role: UserRole
    permission: UserPermission


class UserForAdminOut(BaseModel):
    permanent: list[PermanentUser]
    temporary: list[TemporaryUser]
