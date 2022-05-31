from fastapi import APIRouter, Depends
from src.app.user.schemas import RegisterUserIn, LoginUserIn, UserOut
from src.app.user.service import UserService

user_router = APIRouter(
    prefix="/user"
)


@user_router.post("/register/", response_model=UserOut)
async def register_user(
    user: RegisterUserIn,
    user_service: UserService = Depends()
):
    return await user_service.create_user(user)


@user_router.post("/login/", response_model=UserOut)
async def login_user(
    user: LoginUserIn,
    user_service: UserService = Depends()
):
    return await user_service.auth_user(user)
