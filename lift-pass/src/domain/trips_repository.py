from abc import ABC, abstractmethod


class TripsRepository(ABC):
    @abstractmethod
    def get_price_for_type(self, trip_type: str) -> int:
        raise NotImplementedError

    @abstractmethod
    def find_all_holidays(self) -> list:
        raise NotImplementedError

    @abstractmethod
    def add_price(self, trip_type: str, cost: int) -> None:
        raise NotImplementedError
