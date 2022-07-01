from httpx import AsyncClient

from src.app.facility.controller import CREATE_FACILITY_ENDPOINT
from src.app.waste.types import AggregateState


async def test_create_facility(client: AsyncClient):
    req_body = {
        "name": "КПК",
        "wastes": [
            {
                "name": "Металлолом",
                "type": AggregateState.SOLID.value,
                "density": 0.063
            }
        ]
    }
    response = await client.post(
        CREATE_FACILITY_ENDPOINT,
        json=req_body
    )
    assert response.status_code == 200