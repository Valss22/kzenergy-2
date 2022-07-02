import pytest
from httpx import AsyncClient

from src.app.user.controller import REGISTER_ENDPOINT, LOGIN_ENDPOINT
from src.app.user.types import UserRole


@pytest.fixture(scope="module")
def user_setup() -> dict:
    login_req_body = {
        "email": "test@gmail.com",
        "password": "123"
    }
    register_req_body = login_req_body.copy()
    register_req_body.update({
        "fullname": "Shok Vlad",
        "role": UserRole.ECOLOGIS.value,
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
    response = await client.post(
        REGISTER_ENDPOINT,
        json=req_body
    )
    assert response.status_code == 200
    assert list(response.json().keys()) == user_setup["response_keys"]


async def test_register_admin_user(client: AsyncClient, user_setup):
    req_body = user_setup["register_req_body"]
    req_body.update({
        "role": UserRole.ADMIN.value,
    })
    response = await client.post(
        REGISTER_ENDPOINT,
        json=req_body
    )
    assert response.status_code == 400


async def test_successful_login_user(client: AsyncClient, user_setup):
    req_body = user_setup["login_req_body"]
    response = await client.post(
        LOGIN_ENDPOINT,
        json=req_body
    )
    assert response.status_code == 200
    assert list(response.json().keys()) == user_setup["response_keys"]


async def test_unsuccessful_login_user(client: AsyncClient, user_setup):
    req_body = user_setup["login_req_body"]
    req_body.update({"email": "test2@gmail.com"})
    response = await client.post(
        LOGIN_ENDPOINT,
        json=req_body
    )
    assert response.status_code == 400
