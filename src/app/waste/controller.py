from fastapi import APIRouter, Depends

from src.app.waste.schemas import WasteQuantity, UpdateWaste
from src.app.waste.service import WasteService

waste_router = APIRouter()
WASTE_QUANTITY_ENDPOINT = "/stat/waste/"


@waste_router.get(WASTE_QUANTITY_ENDPOINT, response_model=list[WasteQuantity])
async def get_wastes_quantity(waste_service: WasteService = Depends()):
    return await waste_service.get_wastes_quantity()


@waste_router.patch(WASTE_QUANTITY_ENDPOINT)
def update_waste_limit(
    waste: UpdateWaste,
    waste_service: WasteService = Depends()
):
    return waste_service.update_waste_limit(waste)


