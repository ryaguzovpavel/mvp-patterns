from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.agency import AuditLog, Deal, Notification
from app.patterns.structural.facade import AgencyFacade
from app.schemas.agency import AuditOut, DealCreate, DealOut, NotificationOut

router = APIRouter(tags=["deals"])


@router.post(
    "/deals",
    response_model=DealOut,
    summary="Открыть сделку по объекту",
    description=(
        "Привязывает клиента к property_id, рассчитывает комиссию (percent 3% или fixed 50 000), "
        "фиксирует аудит и уведомления агенту и в журнал агентства."
    ),
    response_description="Новая сделка со статусом new и рассчитанной комиссией",
)
def create_deal(data: DealCreate, db: Session = Depends(get_db)) -> Deal:
    try:
        return AgencyFacade(db).open_deal(data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/deals",
    response_model=list[DealOut],
    summary="Список сделок",
    description="Все сделки: объект, клиент, сумма, стратегия комиссии, статус new / in_progress / closed.",
    response_description="Все сделки с суммой, комиссией и текущим статусом",
)
def list_deals(db: Session = Depends(get_db)) -> list[Deal]:
    return db.query(Deal).order_by(Deal.id.desc()).all()


@router.post(
    "/deals/{deal_id}/advance",
    response_model=DealOut,
    summary="Перевести сделку на следующий статус",
    description=(
        "Перевод по цепочке new → in_progress → closed. Для closed повторный вызов вернёт ошибку. "
        "Дополняет журнал аудита и уведомления."
    ),
    response_description="Сделка после перехода по цепочке State",
)
def advance_deal(
    deal_id: int = Path(..., description="Идентификатор сделки"),
    db: Session = Depends(get_db),
) -> Deal:
    try:
        return AgencyFacade(db).advance_deal(deal_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get(
    "/notifications",
    response_model=list[NotificationOut],
    summary="Журнал уведомлений",
    description="Уведомления, созданные при open_deal и advance_deal; каналы agent и journal.",
    response_description="Сообщения по каналам agent и journal",
)
def list_notifications(db: Session = Depends(get_db)) -> list[Notification]:
    return db.query(Notification).order_by(Notification.id.desc()).all()


@router.get(
    "/audit",
    response_model=list[AuditOut],
    summary="Журнал аудита сделок",
    description="Записи об операциях open_deal и advance_deal с деталями смены статуса.",
    response_description="Записи Decorator по операциям со сделками",
)
def list_audit(db: Session = Depends(get_db)) -> list[AuditLog]:
    return db.query(AuditLog).order_by(AuditLog.id.desc()).all()