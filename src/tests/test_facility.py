from httpx import AsyncClient
from src.app.facility.controller import FACILITY_ENDPOINT, FACILITY_TOTAL_ENDPOINT
from src.app.facility.model import Facility
from src.app.report.model import Report
from src.app.summary_report.controller import SUMMARY_REPORT_ENDPOINT
from src.app.summary_report.model import SummaryReport
from src.app.ticket.controller import TICKET_ENDPOINT
from src.app.ticket.excel.service import write_ticket_to_excel
from src.app.ticket.model import Ticket
from src.app.ticket.types import WasteDestinationType, AggregateState, MeasureSystem, TicketStatus
from src.app.user.controller import REGISTER_ENDPOINT
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
    assert list(response.json()["reports"][0].keys()) == ["id", "date", "user", "tickets", "facilityName"]
    assert response.json()["reports"][0]["facilityName"] == "КПК"
    assert response.json()["facilityNumber"] == 1
    assert response.status_code == 200


async def test_update_ticket(client: AsyncClient):
    req_body = {
        "status": TicketStatus.ACCEPTED.value,
        "message": "updated"
    }
    ticket = await Ticket.get()
    ticket_waste_old = ticket.wasteName
    ticket_msg_old = ticket.message
    response = await client.patch(
        TICKET_ENDPOINT + f"{str(ticket.id)}",
        json=req_body
    )
    ticket = await Ticket.get()
    ticket_msg_new = ticket.message
    ticket_waste_new = ticket.wasteName
    assert ticket_msg_new != ticket_msg_old
    assert ticket_waste_new == ticket_waste_old
    assert response.status_code == 200


async def test_create_sum_report(client: AsyncClient):
    user_response = await client.post(
        REGISTER_ENDPOINT,
        json={
            "email": "test22@gmail.com",
            "password": "123",
            "fullname": "Shok Vlad",
            "role": UserRole.ECOLOGIS.value,
            "phone": "87775556774"
        }
    )
    auth_header = "baerer " + user_response.json()["token"]
    assert await SummaryReport.all().count() == 0
    response = await client.post(
        SUMMARY_REPORT_ENDPOINT,
        headers={"Authorization": auth_header}
    )
    assert await SummaryReport.all().count() == 1
    assert response.status_code == 200


async def test_get_sum_reports(client: AsyncClient):
    response = await client.get(
        "/archive/summary/"
    )
    assert response.status_code == 200
