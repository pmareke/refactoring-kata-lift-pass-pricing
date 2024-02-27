from abc import ABC, abstractmethod


class LiftsRepository(ABC):
    @abstractmethod
    def get_price_for_lift(self, trip_type: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def is_holiday(self, date: str | None) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add_price(self, trip_type: str, cost: int) -> None:
        raise NotImplementedError
