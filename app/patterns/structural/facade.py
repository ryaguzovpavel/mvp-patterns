"""Структурный паттерн: Facade."""

from sqlalchemy.orm import Session

from app.models.agency import Deal, Property
from app.patterns.behavioral.commission import strategy_for
from app.patterns.behavioral.observers import ChannelNotificationObserver, DealEventSubject
from app.patterns.creational.listing import ListingBuilder, factory_for
from app.patterns.structural.deal_audit import AuditedDealService, DealOperations
from app.schemas.agency import DealCreate, PropertyCreate


class AgencyFacade:
    """Один вход для агента: публикация объекта и ведение сделки."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def publish_property(self, data: PropertyCreate) -> Property:
        draft = (
            ListingBuilder()
            .titled(data.title)
            .from_legacy_address(data.legacy_address)
            .priced(data.price)
            .with_area(data.area)
            .with_floor(data.floor)
            .with_land(data.land_area)
            .with_purpose(data.purpose)
            .build()
        )
        spec = factory_for(data.kind).create(draft)
        prop = Property(
            kind=spec.kind,
            title=spec.title,
            address=spec.address,
            price=spec.price,
            area=spec.area,
            details=spec.details,
            status="published",
        )
        self._db.add(prop)
        self._db.commit()
        self._db.refresh(prop)
        return prop

    def open_deal(self, data: DealCreate) -> Deal:
        prop = self._db.get(Property, data.property_id)
        if prop is None:
            raise ValueError("Объект не найден")
        strategy = strategy_for(data.commission_strategy)
        deal = Deal(
            property_id=prop.id,
            client_name=data.client_name.strip(),
            amount=data.amount,
            commission=strategy.calculate(data.amount),
            commission_strategy=strategy.name,
            status="draft",
        )
        self._db.add(deal)
        self._db.flush()
        AuditedDealService(DealOperations(), self._db).open(deal)
        self._notify(deal, "сделка открыта")
        self._db.commit()
        self._db.refresh(deal)
        return deal

    def advance_deal(self, deal_id: int) -> Deal:
        deal = self._db.get(Deal, deal_id)
        if deal is None:
            raise ValueError("Сделка не найдена")
        AuditedDealService(DealOperations(), self._db).advance(deal)
        self._notify(deal, "статус изменён")
        self._db.commit()
        self._db.refresh(deal)
        return deal

    def _notify(self, deal: Deal, event: str) -> None:
        subject = DealEventSubject()
        subject.attach(ChannelNotificationObserver(self._db, "agent"))
        subject.attach(ChannelNotificationObserver(self._db, "journal"))
        subject.notify(deal, event)
