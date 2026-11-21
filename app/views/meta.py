from fastapi import APIRouter

router = APIRouter(tags=["meta"])

PATTERNS = [
    {
        "group": "порождающий",
        "name": "Builder",
        "task": "Собрать объявление по шагам: название, адрес, цена, площадь и поля типа",
        "where": "app/patterns/creational/listing.py → ListingBuilder",
    },
    {
        "group": "порождающий",
        "name": "Factory Method",
        "task": "Создать квартиру, дом или коммерцию со своими обязательными полями",
        "where": "app/patterns/creational/listing.py → PropertyFactory",
    },
    {
        "group": "структурный",
        "name": "Adapter",
        "task": "Принять адрес из старой CRM в виде Город|Улица|Дом",
        "where": "app/patterns/structural/address.py → AddressAdapter",
    },
    {
        "group": "структурный",
        "name": "Decorator",
        "task": "Писать журнал аудита при открытии и смене статуса сделки",
        "where": "app/patterns/structural/deal_audit.py → AuditedDealService",
    },
    {
        "group": "структурный",
        "name": "Facade",
        "task": "Дать агенту один вход: опубликовать объект или провести сделку",
        "where": "app/patterns/structural/facade.py → AgencyFacade",
    },
    {
        "group": "поведенческий",
        "name": "Strategy",
        "task": "Посчитать комиссию процентом или фиксированной суммой",
        "where": "app/patterns/behavioral/commission.py",
    },
    {
        "group": "поведенческий",
        "name": "State",
        "task": "Вести сделку по цепочке new → in_progress → closed",
        "where": "app/patterns/behavioral/state.py",
    },
    {
        "group": "поведенческий",
        "name": "Observer",
        "task": "После события по сделке уведомить агента и журнал агентства",
        "where": "app/patterns/behavioral/observers.py",
    },
]


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/patterns")
def patterns() -> list[dict[str, str]]:
    return PATTERNS
