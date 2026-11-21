"""Структурный паттерн: Adapter."""


class LegacyCrmAddress:
    """Старый формат карточки: «Город|Улица|Дом»."""

    def pack(self, raw: str) -> tuple[str, str, str]:
        parts = [part.strip() for part in raw.split("|")]
        if len(parts) != 3 or not all(parts):
            raise ValueError("Адрес старой CRM: Город|Улица|Дом")
        return parts[0], parts[1], parts[2]


class AddressAdapter:
    """Adapter: приводит строку старой CRM к адресу объявления."""

    def __init__(self, legacy: LegacyCrmAddress | None = None) -> None:
        self._legacy = legacy or LegacyCrmAddress()

    def to_display(self, raw: str) -> str:
        city, street, house = self._legacy.pack(raw)
        return f"г. {city}, ул. {street}, д. {house}"
