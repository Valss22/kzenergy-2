from fastapi import APIRouter, Depends

from src.app.user.permission.schemas import UserForAdminOut
from src.app.user.schemas import UserRegisterIn, UserLoginIn, UserOut
from src.app.user.service import UserService

user_router = APIRouter()
REGISTER_ENDPOINT = "/user/register/"
LOGIN_ENDPOINT = "/user/login/"


@user_router.post(REGISTER_ENDPOINT, response_model=UserOut)
async def register_user(
    user: UserRegisterIn,
    user_service: UserService = Depends()
):
    return await user_service.create_user(user)


@user_router.post(LOGIN_ENDPOINT, response_model=UserOut)
async def login_user(
    user: UserLoginIn,
    user_service: UserService = Depends()
):
    return await user_service.auth_user(user)


@user_router.get("/user/", response_model=UserForAdminOut)
async def get_users(user_service: UserService = Depends()):
    return await user_service.get_users()