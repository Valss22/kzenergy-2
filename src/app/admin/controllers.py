from typing import Final

from fastapi import APIRouter

admin_router = APIRouter()
CREATE_FACILITY_ENDPOINT: Final[str] = "/user/register/"


@admin_router.post(CREATE_FACILITY_ENDPOINT)
async def create_facility(
    user: UserRegisterIn,
    user_service: UserService = Depends()
):
    pass
    return await user_service.create_user(user)