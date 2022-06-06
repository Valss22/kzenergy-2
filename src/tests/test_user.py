from time import time

import bcrypt
import jwt

from src.app.settings import SALT, TOKEN_TIME, TOKEN_KEY
from src.app.user.model import User
from src.app.user.types import Roles

ADMIN_EMAIL = "deger.begerrr@gmail.com"


async def test_register_user(client):
    request_body = {
        "email": "deger.begerrr@gmail.com",
        "password": "123",
        "fullname": "Shok Vlad",
        "role": Roles.ADMIN.value,
        "phone": "87775556774"
    }
    password = request_body["password"].encode()
    del request_body["password"]
    created_user = await User.create(
        **request_body,
        password_hash=bcrypt.hashpw(password, SALT)
    )
    await created_user.save()
    payload = {
        "id": str(created_user.id),
        "email": created_user.email,
        "exp": time() + TOKEN_TIME
    }
    request_body["password"] = password.decode()
    response = await client.post(
        "/user/register/",
        json=request_body
    )
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {
        "id": str(created_user.id),
        "role": Roles.ECOLOGIS.value,
        "email": "test233@gmail.com",
        "phone": "87775556774",
        "fullname": "Shok Vlad",
        "token": jwt.encode(payload, TOKEN_KEY)
    }
