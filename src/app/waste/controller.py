from fastapi import APIRouter, Depends

from src.app.waste.schemas import WasteQuantity
from src.app.waste.service import WasteService

waste_router = APIRouter()
WASTE_QUANTITY_ENDPOINT = "/stat/waste/"


@waste_router.get(WASTE_QUANTITY_ENDPOINT, response_model=list[WasteQuantity])
async def get_wastes_quantity(waste_service: WasteService = Depends()):
    return await waste_service.get_wastes_quantity()

