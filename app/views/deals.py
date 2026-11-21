from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.agency import AuditLog, Deal, Notification
from app.patterns.structural.facade import AgencyFacade
from app.schemas.agency import AuditOut, DealCreate, DealOut, NotificationOut

router = APIRouter(tags=["deals"])


@router.post("/deals", response_model=DealOut)
def create_deal(data: DealCreate, db: Session = Depends(get_db)) -> Deal:
    try:
        return AgencyFacade(db).open_deal(data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/deals", response_model=list[DealOut])
def list_deals(db: Session = Depends(get_db)) -> list[Deal]:
    return db.query(Deal).order_by(Deal.id.desc()).all()


@router.post("/deals/{deal_id}/advance", response_model=DealOut)
def advance_deal(deal_id: int, db: Session = Depends(get_db)) -> Deal:
    try:
        return AgencyFacade(db).advance_deal(deal_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/notifications", response_model=list[NotificationOut])
def list_notifications(db: Session = Depends(get_db)) -> list[Notification]:
    return db.query(Notification).order_by(Notification.id.desc()).all()


@router.get("/audit", response_model=list[AuditOut])
def list_audit(db: Session = Depends(get_db)) -> list[AuditLog]:
    return db.query(AuditLog).order_by(AuditLog.id.desc()).all()
