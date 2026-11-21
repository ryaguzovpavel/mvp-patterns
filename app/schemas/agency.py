from datetime import datetime

from pydantic import BaseModel, Field


class PropertyCreate(BaseModel):
    kind: str = Field(description="apartment | house | commercial")
    title: str
    legacy_address: str = Field(description="Формат старой CRM: Город|Улица|Дом")
    price: int = Field(gt=0)
    area: int = Field(gt=0)
    floor: int | None = None
    land_area: int | None = None
    purpose: str | None = None


class PropertyOut(BaseModel):
    id: int
    kind: str
    title: str
    address: str
    price: int
    area: int
    details: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class DealCreate(BaseModel):
    property_id: int
    client_name: str
    amount: int = Field(gt=0)
    commission_strategy: str = Field(description="percent | fixed")


class DealOut(BaseModel):
    id: int
    property_id: int
    client_name: str
    amount: int
    commission: int
    commission_strategy: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class NotificationOut(BaseModel):
    id: int
    deal_id: int
    channel: str
    message: str
    created_at: datetime

    model_config = {"from_attributes": True}


class AuditOut(BaseModel):
    id: int
    action: str
    entity: str
    entity_id: int
    detail: str
    created_at: datetime

    model_config = {"from_attributes": True}
