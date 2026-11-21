# MVP: паттерны в ИС агентства недвижимости

Монолит на FastAPI и PostgreSQL. Без микросервисов: каталог объектов и сделки. Каждый паттерн закрывает одну задачу предметной области.

## Запуск

```bash
docker compose up --build
```

API: http://localhost:8001/docs  
Postgres с хоста: `localhost:5433`, база `realty` / `realty` / `realty`.

## Паттерны

| Группа | Паттерн | Задача |
|---|---|---|
| Порождающий | Builder | Собрать объявление по шагам |
| Порождающий | Factory Method | Квартира, дом и коммерция создаются по своим правилам |
| Структурный | Adapter | Адрес из старой CRM: `Город\|Улица\|Дом` |
| Структурный | Decorator | Журнал аудита вокруг операций со сделкой |
| Структурный | Facade | Один сценарий для агента: объект и сделка |
| Поведенческий | Strategy | Комиссия 3% или фикс 50 000 |
| Поведенческий | State | Статусы `new` → `in_progress` → `closed` |
| Поведенческий | Observer | Уведомление агенту и в журнал агентства |

Список также отдаёт `GET /patterns`.

## Сценарий

```bash
curl -X POST http://localhost:8001/properties \
  -H 'Content-Type: application/json' \
  -d '{"kind":"apartment","title":"2к на Ленина","legacy_address":"Пермь|Ленина|10","price":4500000,"area":54,"floor":5}'

curl -X POST http://localhost:8001/deals \
  -H 'Content-Type: application/json' \
  -d '{"property_id":1,"client_name":"Иванов Иван","amount":4500000,"commission_strategy":"percent"}'

curl -X POST http://localhost:8001/deals/1/advance
curl http://localhost:8001/notifications
curl http://localhost:8001/audit
```
