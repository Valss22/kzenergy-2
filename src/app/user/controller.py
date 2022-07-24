from fastapi import APIRouter, Depends

from src.app.user.permission.schemas import UserForAdminOut, UserPermission
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


@user_router.patch("/user/{user_id}/")
async def update_user_permission(
    user_id: str,
    user_permission: UserPermission,
    user_service: UserService = Depends()
):
    return await user_service.update_user_permission(user_id, user_permission)


@user_router.delete("/user/{user_id}/")
async def delete_user(
    user_id: str,
    user_service: UserService = Depends()
):
    return await user_service.delete_user(user_id)

