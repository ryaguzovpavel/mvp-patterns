"""Поведенческий паттерн: Strategy."""

from abc import ABC, abstractmethod


class CommissionStrategy(ABC):
    name: str

    @abstractmethod
    def calculate(self, amount: int) -> int:
        raise NotImplementedError


class PercentCommission(CommissionStrategy):
    """3% от суммы сделки, как типовая комиссия агентства."""

    name = "percent"

    def calculate(self, amount: int) -> int:
        return amount * 3 // 100


class FixedCommission(CommissionStrategy):
    """Фиксированная комиссия за сопровождение."""

    name = "fixed"

    def calculate(self, amount: int) -> int:
        return 50_000


STRATEGIES: dict[str, CommissionStrategy] = {
    "percent": PercentCommission(),
    "fixed": FixedCommission(),
}


def strategy_for(name: str) -> CommissionStrategy:
    try:
        return STRATEGIES[name]
    except KeyError as exc:
        raise ValueError("Стратегия комиссии: percent или fixed") from exc
