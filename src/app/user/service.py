from time import time
from typing import Union
import bcrypt
import jwt
from pydantic import EmailStr
from starlette import status
from starlette.responses import JSONResponse
from tortoise.exceptions import DoesNotExist
from src.app.settings import TOKEN_KEY, TOKEN_TIME
from src.app.user.model import User
from src.app.user.schemas import RegisterUserIn, LoginUserIn


class UserService:
    async def get_response_with_token(self, user: User):
        payload: dict = {
            "id": str(user.id),
            "email": user.email,
            "exp": time() + TOKEN_TIME
        }
        return {
            **user.__dict__,
            "token": jwt.encode(payload, TOKEN_KEY),
        }

    async def create_user(self, user: RegisterUserIn) -> Union[JSONResponse, dict]:
        password_hash: str = user.dict()["password"].encode()
        email: EmailStr = user.dict()["email"]

        if await User.filter(email=email):
            return JSONResponse({
                "detail": "Данный пользователь уже существует"
            }, status.HTTP_400_BAD_REQUEST)

        del user.dict()["password"]

        created_user = await User.create(
            **user.dict(), password_hash=password_hash
        )
        await created_user.save()
        return await self.get_response_with_token(created_user)

    async def auth_user(self, user: LoginUserIn) -> Union[dict, JSONResponse]:
        email: EmailStr = user.dict()["email"]
        password: bytes = user.dict()["password"].encode()
        try:
            current_user = await User.get(email=email)
        except DoesNotExist:
            return JSONResponse(
                {"detail": "Данного пользователя не существует"},
                status.HTTP_400_BAD_REQUEST
            )

        if bcrypt.checkpw(password, current_user.password_hash):
            return await self.get_response_with_token(current_user)
        return JSONResponse(
            {"detail": "Неверный пароль"},
            status.HTTP_400_BAD_REQUEST
        )
