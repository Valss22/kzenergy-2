from httpx import AsyncClient
from src.app.facility.controller import FACILITY_ENDPOINT
from src.app.facility.model import Facility
from src.app.report.model import Report
from src.app.ticket.model import Ticket
from src.app.ticket.types import WasteDestinationType, AggregateState, MeasureSystem
from src.app.user.model import User
from src.app.user.types import UserRole
from src.app.waste.model import Waste


async def test_create_facility(client: AsyncClient):
    req_body = {
        "name": "КПК",
        "wastes": ["Металлолом", "Строительные отходы"]
    }
    response = await client.post(
        FACILITY_ENDPOINT,
        json=req_body
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


async def test_get_facility_tickets(client: AsyncClient):
    # FIXME: Create factories or setup fixtures
    report = await Report.create()
    facility = await Facility.get()
    worker = await User.create(
        fullname="Шокоров Влад",
        email="valss@gmail.com",
        role=UserRole.FACILITY_WORKER.value,
        password_hash="123".encode(),
        phone="777666"
    )
    await Ticket.create(
        facility=facility,
        waste_destination_type=WasteDestinationType.A.value,
        aggregate_state=AggregateState.SOLID.value,
        worker=worker,
        measure_system=MeasureSystem.ITEM.value,
        quantity=42,
        report=report,
        excel_url="some_excel_url",
        message="Сообщение для Талона"
    )
    response = await client.get(
        FACILITY_ENDPOINT + f"{str(facility.id)}"
    )
    print(response.json())
    assert response.status_code == 200
