from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.agency import Property
from app.patterns.structural.facade import AgencyFacade
from app.schemas.agency import PropertyCreate, PropertyOut

router = APIRouter(prefix="/properties", tags=["properties"])


@router.post(
    "",
    response_model=PropertyOut,
    summary="Опубликовать объект недвижимости",
    description=(
        "Создаёт карточку объекта в каталоге через AgencyFacade.publish_property: "
        "ListingBuilder, AddressAdapter для legacy_address, Factory Method по полю kind."
    ),
    response_description="Созданная карточка объекта со статусом published",
)
def create_property(data: PropertyCreate, db: Session = Depends(get_db)) -> Property:
    try:
        return AgencyFacade(db).publish_property(data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "",
    response_model=list[PropertyOut],
    summary="Список объектов",
    description="Возвращает опубликованные объекты, сначала новые. Параметр kind сужает выборку по типу.",
    response_description="Все объекты, от новых к старым",
)
def list_properties(
    kind: str | None = Query(
        default=None,
        description="Фильтр по типу: apartment, house или commercial",
    ),
    db: Session = Depends(get_db),
) -> list[Property]:
    query = db.query(Property).order_by(Property.id.desc())
    if kind:
        query = query.filter(Property.kind == kind)
    return query.all()