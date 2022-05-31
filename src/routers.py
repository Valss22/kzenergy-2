from fastapi import APIRouter

from src.user.controllers import user_router

api_router = APIRouter()
api_router.include_router(user_router)
