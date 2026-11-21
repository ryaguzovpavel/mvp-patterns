from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.agency import Property
from app.patterns.structural.facade import AgencyFacade
from app.schemas.agency import PropertyCreate, PropertyOut

router = APIRouter(prefix="/properties", tags=["properties"])


@router.post("", response_model=PropertyOut)
def create_property(data: PropertyCreate, db: Session = Depends(get_db)) -> Property:
    try:
        return AgencyFacade(db).publish_property(data)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("", response_model=list[PropertyOut])
def list_properties(kind: str | None = None, db: Session = Depends(get_db)) -> list[Property]:
    query = db.query(Property).order_by(Property.id.desc())
    if kind:
        query = query.filter(Property.kind == kind)
    return query.all()
