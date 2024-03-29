from uuid import UUID
from pydantic import EmailStr
from pydantic.main import BaseModel
from src.app.user.types import UserRole
from typing import List

class UserPermission(BaseModel):
    write: bool
    read: bool


class UserPermissionFull(UserPermission):
    temporary: bool


class TempUserIn(UserPermission):
    email: EmailStr
    role: UserRole


class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    role: UserRole
    permission: UserPermissionFull


class UserForAdminOut(BaseModel):
    permanent: List[UserOut]
    temporary: List[UserOut]
