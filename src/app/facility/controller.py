from typing import Final

from fastapi import APIRouter, Depends

from src.app.facility.schemas import FacilityIn
from src.app.facility.service import FacilityService

admin_router = APIRouter()
CREATE_FACILITY_ENDPOINT: Final[str] = "/admin/facility/"


@admin_router.post(CREATE_FACILITY_ENDPOINT)
async def create_facility(
    facility: FacilityIn,
    facility_service: FacilityService = Depends()
):
    return await facility_service.create_facility(facility)
