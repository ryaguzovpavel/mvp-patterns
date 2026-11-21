"""Порождающие паттерны: Builder и Factory Method."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.patterns.structural.address import AddressAdapter


@dataclass
class ListingDraft:
    """Черновик объявления, который собирает Builder."""

    title: str
    address: str
    price: int
    area: int
    floor: int | None = None
    land_area: int | None = None
    purpose: str | None = None


@dataclass
class PropertySpec:
    kind: str
    title: str
    address: str
    price: int
    area: int
    details: str


class ListingBuilder:
    """Builder: объявление собирается по шагам, адрес приводится через Adapter."""

    def __init__(self, address_adapter: AddressAdapter | None = None) -> None:
        self._address_adapter = address_adapter or AddressAdapter()
        self._title = ""
        self._address = ""
        self._price = 0
        self._area = 0
        self._floor: int | None = None
        self._land_area: int | None = None
        self._purpose: str | None = None

    def titled(self, title: str) -> "ListingBuilder":
        self._title = title.strip()
        return self

    def from_legacy_address(self, raw: str) -> "ListingBuilder":
        self._address = self._address_adapter.to_display(raw)
        return self

    def priced(self, price: int) -> "ListingBuilder":
        self._price = price
        return self

    def with_area(self, area: int) -> "ListingBuilder":
        self._area = area
        return self

    def with_floor(self, floor: int | None) -> "ListingBuilder":
        self._floor = floor
        return self

    def with_land(self, land_area: int | None) -> "ListingBuilder":
        self._land_area = land_area
        return self

    def with_purpose(self, purpose: str | None) -> "ListingBuilder":
        self._purpose = purpose
        return self

    def build(self) -> ListingDraft:
        if not self._title or not self._address or self._price <= 0 or self._area <= 0:
            raise ValueError("Не хватает данных объявления: название, адрес, цена, площадь")
        return ListingDraft(
            title=self._title,
            address=self._address,
            price=self._price,
            area=self._area,
            floor=self._floor,
            land_area=self._land_area,
            purpose=self._purpose,
        )


class PropertyFactory(ABC):
    """Factory Method: общий каркас создания объекта, тип задаёт подкласс."""

    def create(self, draft: ListingDraft) -> PropertySpec:
        spec = self._make(draft)
        if spec.price <= 0:
            raise ValueError("Цена должна быть больше нуля")
        return spec

    @abstractmethod
    def _make(self, draft: ListingDraft) -> PropertySpec:
        raise NotImplementedError


class ApartmentFactory(PropertyFactory):
    def _make(self, draft: ListingDraft) -> PropertySpec:
        if draft.floor is None:
            raise ValueError("Для квартиры нужен этаж")
        return PropertySpec(
            kind="apartment",
            title=draft.title,
            address=draft.address,
            price=draft.price,
            area=draft.area,
            details=f"этаж {draft.floor}",
        )


class HouseFactory(PropertyFactory):
    def _make(self, draft: ListingDraft) -> PropertySpec:
        if draft.land_area is None:
            raise ValueError("Для дома нужна площадь участка")
        return PropertySpec(
            kind="house",
            title=draft.title,
            address=draft.address,
            price=draft.price,
            area=draft.area,
            details=f"участок {draft.land_area} м²",
        )


class CommercialFactory(PropertyFactory):
    def _make(self, draft: ListingDraft) -> PropertySpec:
        purpose = (draft.purpose or "").strip()
        if not purpose:
            raise ValueError("Для коммерции нужно назначение помещения")
        return PropertySpec(
            kind="commercial",
            title=draft.title,
            address=draft.address,
            price=draft.price,
            area=draft.area,
            details=f"назначение: {purpose}",
        )


FACTORIES: dict[str, PropertyFactory] = {
    "apartment": ApartmentFactory(),
    "house": HouseFactory(),
    "commercial": CommercialFactory(),
}


def factory_for(kind: str) -> PropertyFactory:
    try:
        return FACTORIES[kind]
    except KeyError as exc:
        raise ValueError("Тип объекта: apartment, house или commercial") from exc
