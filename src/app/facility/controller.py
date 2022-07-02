from fastapi import APIRouter, Depends
from src.app.facility.schemas import FacilityIn
from src.app.facility.service import FacilityService

facility_router = APIRouter()
CREATE_FACILITY_ENDPOINT = "/admin/facility/"


@facility_router.post(CREATE_FACILITY_ENDPOINT)
async def create_facility(
    facility: FacilityIn,
    facility_service: FacilityService = Depends()
):
    return await facility_service.create_facility(facility)
