from typing import TypedDict

import pytest
from httpx import AsyncClient

from src.app.user.model import User
from src.app.user.types import Roles


@pytest.fixture(scope="module")
def user_setup() -> dict:
    login_req_body = {
        "email": "test@gmail.com",
        "password": "123"
    }
    register_req_body = login_req_body.copy()
    register_req_body.update({
        "fullname": "Shok Vlad",
        "role": Roles.ECOLOGIS.value,
        "phone": "87775556774"
    })
    return {
        "register_req_body": register_req_body,
        "login_req_body": login_req_body,
        "response_keys": [
            "id", "role",
            "fullname", "email",
            "phone", "token"
        ]
    }


async def test_register_user(client: AsyncClient, user_setup):
    req_body = user_setup["register_req_body"]
    password = req_body["password"].encode()
    req_body.update({"password": password.decode()})
    response = await client.post(
        "/user/register/",
        json=req_body
    )
    assert response.status_code == 200
    assert list(response.json().keys()) == user_setup["response_keys"]


async def test_successful_login_user(client: AsyncClient, user_req_body):
    register_req_body = user_req_body["register_req_body"]
    req_body = user_req_body["login_req_body"]
    # password_hash = register_req_body["password"].encode()
    # del register_req_body["password"]
    # await User.create(
    #     **register_req_body, password_hash=password_hash
    # )
    response = await client.post(
        "/user/login/",
        json=req_body
    )
    assert response.status_code == 200
    assert list(response.json().keys()) == user_setup["response_keys"]
