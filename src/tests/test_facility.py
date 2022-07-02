import pytest
from httpx import AsyncClient
from src.app.facility.controller import CREATE_FACILITY_ENDPOINT
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
        CREATE_FACILITY_ENDPOINT,
        json=facility_setup["req_body"]
    )
    assert await Facility.all().count() == 1
    assert await Waste.all().count() == 2
    assert response.status_code == 200


# async def test_unique_error_on_waste_not_as_transaction(client: AsyncClient, facility_setup):
#     response = await client.post(
#         CREATE_FACILITY_ENDPOINT,
#         json={
#         "name": "УГПК-2",
#         "wastes": [
#             {
#                 "name": "Металлолом",
#             },
#             {
#                 "name": "Строительные отходы",
#                 "type": AggregateState.SOLID.value,
#                 "density": 0.065
#             }
#         ]
#     }
#     )
#     assert response.status_code == 200
#     assert await Waste.all().count() == 1
