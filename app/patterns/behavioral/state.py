"""Поведенческий паттерн: State."""

from abc import ABC, abstractmethod


class DealState(ABC):
    name: str

    @abstractmethod
    def next_status(self) -> str:
        raise NotImplementedError


class NewState(DealState):
    name = "new"

    def next_status(self) -> str:
        return "in_progress"


class InProgressState(DealState):
    name = "in_progress"

    def next_status(self) -> str:
        return "closed"


class ClosedState(DealState):
    name = "closed"

    def next_status(self) -> str:
        raise ValueError("Закрытую сделку нельзя перевести дальше")


STATES: dict[str, DealState] = {
    "new": NewState(),
    "in_progress": InProgressState(),
    "closed": ClosedState(),
}


def advance_status(current: str) -> str:
    try:
        state = STATES[current]
    except KeyError as exc:
        raise ValueError(f"Неизвестный статус сделки: {current}") from exc
    return state.next_status()
