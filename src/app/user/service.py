from time import time
from typing import Union
import bcrypt
import jwt
from fastapi import HTTPException
from pydantic import EmailStr
from starlette import status
from starlette.responses import JSONResponse
from tortoise.exceptions import DoesNotExist
from src.app.settings import TOKEN_KEY, TOKEN_TIME, SALT
from src.app.user.model import User
from src.app.user.permission.model import Permission
from src.app.user.permission.schemas import UserForAdminOut, UserPermission
from src.app.user.schemas import UserRegisterIn, UserLoginIn, UserPermissionPatch
from src.app.user.types import UserRole

ADMIN_EMAIL = "deger.begerrr@gmail.com"


async def get_current_user(auth_header: str) -> User:
    decoded_token: dict = jwt.decode(
        auth_header.split(" ")[1],
        TOKEN_KEY, algorithms='HS256'  # type: ignore
    )
    return await User.get(id=str(decoded_token['id']))


class UserService:

    async def check_email(self, email: EmailStr) -> None:
        if await User.filter(email=email):
            raise HTTPException(
                status_code=400,
                detail="This email already exists",
            )

    def check_admin(self, role: UserRole, email: EmailStr) -> None:
        if role == UserRole.ADMIN and email != ADMIN_EMAIL:
            raise HTTPException(
                status_code=400,
                detail="You dont have rights for this role",
            )

    async def response_with_token(self, user: User) -> dict:
        payload: dict = {
            "id": str(user.id),
            "email": user.email,
            "exp": time() + TOKEN_TIME
        }
        return {
            **user.__dict__,
            "token": jwt.encode(payload, TOKEN_KEY),
        }

    def failed_response(self) -> JSONResponse:
        return JSONResponse({
            "detail": "Auth failed"
        }, status.HTTP_400_BAD_REQUEST)

    async def create_user(self, user: UserRegisterIn) -> Union[JSONResponse, dict]:
        role: UserRole = user.dict()["role"]
        email: EmailStr = user.dict()["email"]

        self.check_admin(role, email)
        password = user.dict()["password"].encode()
        await self.check_email(email)

        created_user = await User.create(
            **user.dict(), password_hash=password
        )
        created_user.password_hash = bcrypt.hashpw(password, SALT)
        await created_user.save(update_fields=["password_hash"])

        await Permission.create(user=created_user)

        return await self.response_with_token(created_user)

    async def auth_user(self, user: UserLoginIn) -> Union[dict, JSONResponse]:
        email: EmailStr = user.dict()["email"]
        password = user.dict()["password"].encode()

        try:
            current_user = await User.get(email=email)
        except DoesNotExist:
            return self.failed_response()

        if bcrypt.checkpw(password, current_user.password_hash):
            return await self.response_with_token(current_user)

        return self.failed_response()

    async def get_users(self):
        permanent_users = await User.filter(permission__temporary=False)
        temp_users = await User.filter(permission__temporary=True)
        permanent = []
        temporary = []
        for permanent_user in permanent_users:
            permission = await Permission.get(user=permanent_user)
            write = permission.write
            read = permission.read
            temporaryValue = permission.temporary
            permanent.append({
                **permanent_user.__dict__,
                "permission": {"write": write, "read": read, "temporary": temporaryValue}
            })
        for temp_user in temp_users:
            permission = await Permission.get(user=temp_user)
            write = permission.write
            read = permission.read
            temporaryValue = permission.temporary
            temporary.append({
                **temp_user.__dict__,
                "permission": {"write": write, "read": read, "temporary": temporaryValue}
            })
        return UserForAdminOut(permanent=permanent, temporary=temporary)

    async def update_user_permission(self, user_id, user_permission: UserPermission):
        await Permission.filter(user_id=user_id).update(**user_permission.__dict__)

    async def delete_user(self, user_id):
        await User.filter(id=user_id).delete()
