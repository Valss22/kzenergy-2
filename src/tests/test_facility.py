import pytest
from httpx import AsyncClient
from src.app.facility.controller import FACILITY_ENDPOINT
from src.app.facility.model import Facility
from src.app.waste.model import Waste


@pytest.fixture(scope="module")
def facility_setup() -> dict:
    req_body = {
        "name": "КПК",
        "wastes": ["Металлолом", "Строительные отходы"]
    }
    return {
        "req_body": req_body,
    }


async def test_create_facility(client: AsyncClient, facility_setup):
    response = await client.post(
        FACILITY_ENDPOINT,
        json=facility_setup["req_body"]
    )
    assert await Facility.all().count() == 1
    assert await Waste.all().count() == 2
    assert response.status_code == 200


async def test_get_facilities(client: AsyncClient):
    response = await client.get(
        FACILITY_ENDPOINT
    )
    assert len(response.json()) == 1
    assert list(response.json()[0].keys()) == ["id", "name", "wastes"]
    assert response.status_code == 200
