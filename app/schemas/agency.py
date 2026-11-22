from datetime import datetime

from pydantic import BaseModel, Field


class PropertyCreate(BaseModel):
    kind: str = Field(description="Тип объекта: apartment (квартира), house (дом), commercial")
    title: str = Field(description="Заголовок объявления для каталога")
    legacy_address: str = Field(
        description="Адрес в формате старой CRM: Город|Улица|Дом (например Пермь|Ленина|10)"
    )
    price: int = Field(gt=0, description="Цена, руб.")
    area: int = Field(gt=0, description="Площадь, м²")
    floor: int | None = Field(default=None, description="Этаж — обязателен для apartment")
    land_area: int | None = Field(default=None, description="Площадь участка, соток/м² — для house")
    purpose: str | None = Field(default=None, description="Назначение помещения — для commercial")


class PropertyOut(BaseModel):
    id: int
    kind: str
    title: str
    address: str = Field(description="Адрес после Adapter")
    price: int
    area: int
    details: str = Field(description="Доп. поля от Factory (этаж, участок, назначение)")
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class DealCreate(BaseModel):
    property_id: int = Field(description="ID опубликованного объекта")
    client_name: str = Field(description="ФИО или название клиента")
    amount: int = Field(gt=0, description="Сумма сделки, руб.")
    commission_strategy: str = Field(
        description="Расчёт комиссии (Strategy): percent — 3%, fixed — 50 000 руб."
    )


class DealOut(BaseModel):
    id: int
    property_id: int
    client_name: str
    amount: int
    commission: int = Field(description="Рассчитанная комиссия агентства")
    commission_strategy: str
    status: str = Field(description="new | in_progress | closed")
    created_at: datetime

    model_config = {"from_attributes": True}


class NotificationOut(BaseModel):
    id: int
    deal_id: int
    channel: str = Field(description="agent — агенту; journal — журнал агентства")
    message: str
    created_at: datetime

    model_config = {"from_attributes": True}


class AuditOut(BaseModel):
    id: int
    action: str = Field(description="open_deal | advance_deal")
    entity: str
    entity_id: int
    detail: str
    created_at: datetime

    model_config = {"from_attributes": True}