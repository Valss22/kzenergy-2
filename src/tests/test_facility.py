from httpx import AsyncClient
from src.app.facility.controller import FACILITY_ENDPOINT, FACILITY_TOTAL_ENDPOINT
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
    facility = await Facility.get()
    user = await User.create(
        fullname="Шокоров Влад",
        email="valss@gmail.com",
        role=UserRole.FACILITY_WORKER.value,
        password_hash="123".encode(),
        phone="777666"
    )
    report = await Report.create(user=user)
    await Ticket.create(
        wasteName="Мусор",
        facility=facility,
        wasteDestinationType=WasteDestinationType.A.value,
        aggregateState=AggregateState.SOLID.value,
        user=user,
        measureSystem=MeasureSystem.ITEM.value,
        quantity=42,
        report=report,
        excelUrl="some_excel_url",
        message="Сообщение для Талона"
    )
    response = await client.get(
        FACILITY_ENDPOINT + f"{str(facility.id)}"
    )
    assert response.status_code == 200


async def test_facility_total(client: AsyncClient):
    response = await client.get(FACILITY_TOTAL_ENDPOINT)
    assert response.status_code == 200
