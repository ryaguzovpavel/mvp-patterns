from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.core.database import Base, engine
from app.models import agency as agency_models  # noqa: F401
from app.views import api_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


OPENAPI_TAGS = [
    {
        "name": "properties",
        "description": (
            "Объекты недвижимости агентства. Публикация через фасад: Builder и Factory Method, "
            "адрес из старой CRM через Adapter."
        ),
    },
    {
        "name": "deals",
        "description": (
            "Сделки, комиссии (Strategy), смена статуса (State), уведомления (Observer) "
            "и журнал аудита (Decorator)."
        ),
    },
]


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        lifespan=lifespan,
        openapi_tags=OPENAPI_TAGS,
    )
    app.include_router(api_router)
    return app
