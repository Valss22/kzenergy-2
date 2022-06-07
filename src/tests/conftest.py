import asyncio
from src.app.main import app
import os
from src.app.settings import APP_MODELS
import pytest
from httpx import AsyncClient
from tortoise import Tortoise
from pytest_factoryboy import register

from src.factory.user.factory import UserFactory

register(UserFactory)

DB_URL = os.environ.get("TEST_DB")


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


async def init_db(
    db_url, create_db: bool = False,
    schemas: bool = False
) -> None:
    await Tortoise.init(
        db_url=db_url,
        modules={"models": APP_MODELS},
        _create_db=create_db
    )
    if schemas:
        await Tortoise.generate_schemas()


async def init(db_url: str = DB_URL):
    await init_db(db_url, True, True)


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    await init()
    yield
    await Tortoise._drop_databases()
