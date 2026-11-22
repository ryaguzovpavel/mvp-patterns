from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from app.models.agency import Deal, Notification


class DealObserver(ABC):
    @abstractmethod
    def update(self, deal: Deal, event: str) -> None:
        raise NotImplementedError


class DealEventSubject:
    def __init__(self) -> None:
        self._observers: list[DealObserver] = []

    def attach(self, observer: DealObserver) -> None:
        self._observers.append(observer)

    def notify(self, deal: Deal, event: str) -> None:
        for observer in self._observers:
            observer.update(deal, event)


class ChannelNotificationObserver(DealObserver):
    """
    Пишет уведомление в выбранный канал: агенту или в журнал агентства
    """

    def __init__(self, db: Session, channel: str) -> None:
        self._db = db
        self._channel = channel

    def update(self, deal: Deal, event: str) -> None:
        self._db.add(
            Notification(
                deal_id=deal.id,
                channel=self._channel,
                message=f"{event}: сделка #{deal.id}, клиент {deal.client_name}, статус {deal.status}",
            )
        )
