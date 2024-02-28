from abc import ABC, abstractmethod

from src.domain.lift.lift_date import LyftDate
from src.domain.lift.lift_type import LyftType
from src.domain.lift.lifts_repository import LiftsRepository


class Lift(ABC):
    type: LyftType
    age: int | None
    date: LyftDate | None

    @abstractmethod
    def calculate_cost(self, lifts_repository: LiftsRepository) -> int:
        raise NotImplementedError
