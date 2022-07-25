from fastapi import APIRouter, Depends, Header

from src.app.user.permission.schemas import TempUserIn, UserPermission
from src.app.user.permission.service import TempUserService

temp_user_router = APIRouter()
TEMP_USER_ENDPOINT = "/user/temporary/"


@temp_user_router.post(TEMP_USER_ENDPOINT)
async def create_temp_user(
    temp_user: TempUserIn,
    temp_user_service: TempUserService = Depends()
):
    return await temp_user_service.create_temp_user(temp_user)


@temp_user_router.get("/user/permission/{user_id}/", response_model=UserPermission)
async def get_user_permission(
    Authorization: str = Header(...),
    temp_user_service: TempUserService = Depends()
):
    return await temp_user_service.get_user_permission(Authorization)