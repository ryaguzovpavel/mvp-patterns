from fastapi import APIRouter

from app.views import deals, meta, properties

api_router = APIRouter()
api_router.include_router(meta.router)
api_router.include_router(properties.router)
api_router.include_router(deals.router)
