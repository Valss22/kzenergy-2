import bcrypt
from src.app.settings import SALT
from src.app.user.model import User
from src.app.user.permission.model import Permission
from src.app.user.permission.schemas import TempUserIn
from src.app.user.service import UserService, get_current_user


class TempUserService:
    def __init__(self):
        self.user_service = UserService()

    async def create_temp_user(self, temp_user: TempUserIn):
        email = temp_user.dict()["email"]
        password = email.split("@")[0].encode()
        await self.user_service.check_email(email)
        created_user = await User.create(
            email=email,
            role=temp_user.dict()["role"],
            password_hash=password,
            fullname="undefined",
            phone="undefined"
        )
        created_user.password_hash = bcrypt.hashpw(password, SALT)
        await created_user.save(update_fields=["password_hash"])
        await Permission.create(
            write=temp_user.dict()["write"],
            read=temp_user.dict()["read"],
            temporary=True,
            user=created_user
        )

    async def get_user_permission(self, auth_header: str):
        user = await get_current_user(auth_header)
        return await Permission.get(user_id=user)
