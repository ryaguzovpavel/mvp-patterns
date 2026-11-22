from fastapi import APIRouter

from app.views import deals, properties

api_router = APIRouter()
api_router.include_router(properties.router)
api_router.include_router(deals.router)
