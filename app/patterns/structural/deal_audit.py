"""Структурный паттерн: Decorator."""

from sqlalchemy.orm import Session

from app.models.agency import AuditLog, Deal
from app.patterns.behavioral.state import advance_status


class DealOperations:
    """Базовая операция со сделкой — без журнала."""

    def open(self, deal: Deal) -> Deal:
        deal.status = "new"
        return deal

    def advance(self, deal: Deal) -> Deal:
        deal.status = advance_status(deal.status)
        return deal


class AuditedDealService(DealOperations):
    """Decorator: та же операция, плюс запись в журнал аудита."""

    def __init__(self, wrapped: DealOperations, db: Session) -> None:
        self._wrapped = wrapped
        self._db = db

    def open(self, deal: Deal) -> Deal:
        result = self._wrapped.open(deal)
        self._write("open_deal", result.id, f"сделка создана, статус {result.status}")
        return result

    def advance(self, deal: Deal) -> Deal:
        before = deal.status
        result = self._wrapped.advance(deal)
        self._write("advance_deal", result.id, f"{before} → {result.status}")
        return result

    def _write(self, action: str, entity_id: int, detail: str) -> None:
        self._db.add(
            AuditLog(
                action=action,
                entity="deal",
                entity_id=entity_id,
                detail=detail,
            )
        )
