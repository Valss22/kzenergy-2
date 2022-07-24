from typing import Optional
from uuid import UUID

from pydantic import EmailStr
from pydantic.main import BaseModel

from src.app.user.types import UserRole


class Permission(BaseModel):
    write: bool
    read: bool


class TempUserIn(Permission):
    email: EmailStr
    role: UserRole


class PermanentUser(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole
    permission: Permission


class TemporaryUser(PermanentUser):
    id: UUID
    email: EmailStr
    role: UserRole
    permission: Permission
    password: str


class UserForAdminOut(BaseModel):
    permanent: list[PermanentUser]
    temporary: list[TemporaryUser]
