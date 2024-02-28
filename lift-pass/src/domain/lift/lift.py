from abc import ABC, abstractmethod

from src.domain.lift.lifts_repository import LiftsRepository


class Lift(ABC):
    @abstractmethod
    def calculate_cost(self, lifts_repository: LiftsRepository) -> int:
        raise NotImplementedError
