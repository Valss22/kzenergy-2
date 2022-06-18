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
from src.app.user.schemas import UserRegisterIn, UserLoginIn
from src.app.user.types import Roles

ADMIN_EMAIL = "deger.begerrr@gmail.com"


class UserService:
    async def check_email(self, email: EmailStr) -> None:
        if await User.filter(email=email):
            raise HTTPException(
                status_code=400,
                detail="This email already exists",
            )

    def check_admin(self, role: Roles, email: EmailStr) -> None:
        if role == Roles.ADMIN and email != ADMIN_EMAIL:
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
        role: Roles = user.dict()["role"]
        email: EmailStr = user.dict()["email"]

        self.check_admin(role, email)

        password = user.dict()["password"].encode()

        await self.check_email(email)

        del user.dict()["password"]
        created_user = await User.create(
            **user.dict(), password_hash=password
        )
        created_user.password_hash = bcrypt.hashpw(password, SALT)
        await created_user.save(update_fields=["password_hash"])

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
