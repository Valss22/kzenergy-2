from fastapi import APIRouter, Depends
from src.app.facility.schemas import FacilityIn, FacilityOut, FacilityTicketsOut, FacilityTotalOut
from src.app.facility.service import FacilityService
from typing import List

facility_router = APIRouter()
FACILITY_ENDPOINT = "/facility/"
FACILITY_TOTAL_ENDPOINT = "/facility/total/"


@facility_router.post(FACILITY_ENDPOINT)
async def create_facility(
    facility: FacilityIn,
    facility_service: FacilityService = Depends()
):
    return await facility_service.create_facility(facility)


@facility_router.get(FACILITY_ENDPOINT, response_model=List[FacilityOut])
async def get_facilities(
    facility_service: FacilityService = Depends()
):
    return await facility_service.get_facilities()


@facility_router.get(
    FACILITY_ENDPOINT + "{facility_id}",
    response_model=FacilityTicketsOut
)
async def get_facility_tickets(
    facility_id: str,
    facility_service: FacilityService = Depends()
):
    return await facility_service.get_facility_tickets(facility_id)


@facility_router.get(
    FACILITY_TOTAL_ENDPOINT,
    response_model=FacilityTotalOut
)
async def get_facility_total(facility_service: FacilityService = Depends()):
    return await facility_service.get_facility_total()


@facility_router.delete(FACILITY_ENDPOINT + "{facility_id}")
async def delete_facilities(
    facility_id: str,
    facility_service: FacilityService = Depends()
):
    return await facility_service.delete_facility(facility_id)
