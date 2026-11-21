# Паттерны в ИС агентства недвижимости

## Порождающие

- **Builder** — `app/patterns/creational/listing.py`, класс `ListingBuilder`. Объявление собирается по шагам: название, адрес, цена, площадь, этаж. Вызывается из `AgencyFacade.publish_property`.
- **Factory Method** — там же, `factory_for(kind)`. По типу `apartment` / `house` / `commercial` выбирается своя фабрика и свои правила карточки объекта.

## Структурные

- **Adapter** — `app/patterns/structural/address.py`. Старый адрес из CRM вида `Город|Улица|Дом` переводится в обычную строку. Builder вызывает его в `from_legacy_address`.
- **Decorator** — `app/patterns/structural/deal_audit.py`, `AuditedDealService`. Оборачивает операции со сделкой и пишет строку в журнал аудита (`AuditLog`).
- **Facade** — `app/patterns/structural/facade.py`, `AgencyFacade`. Один сценарий для агента: опубликовать объект, открыть сделку, сменить статус. Скрывает Builder, Factory, Strategy, State, Decorator и Observer.

## Поведенческие

- **Strategy** — `app/patterns/behavioral/commission.py`. Комиссия сделки: `percent` (3%) или фиксированные 50 000. Выбор в `open_deal` по полю `commission_strategy`.
- **State** — `app/patterns/behavioral/state.py`. Переход статуса сделки: `new` → `in_progress` → `closed`. Дальше закрытую сделку перевести нельзя. Вызывается при `advance`.
- **Observer** — `app/patterns/behavioral/observers.py`. После открытия и смены статуса `DealEventSubject` уведомляет двух подписчиков: канал агента и журнал агентства (`Notification`).
