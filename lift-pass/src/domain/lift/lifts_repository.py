from abc import ABC, abstractmethod

from src.domain.lift.lift_date import LyftDate
from src.domain.lift.lift_type import LyftType


class LiftsRepository(ABC):
    @abstractmethod
    def get_price_for_lift(self, lift_type: LyftType) -> int:
        raise NotImplementedError

    @abstractmethod
    def is_holiday(self, date: LyftDate) -> bool:
        raise NotImplementedError

    @abstractmethod
    def add_price(self, lift_type: LyftType, cost: int) -> None:
        raise NotImplementedError
