import math
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from src.domain.lifts_repository import LiftsRepository


@dataclass
class LyftDate:
    date: datetime

    def is_monday(self) -> bool:
        return self.date.weekday() == 0


class LyftType(Enum):
    NIGHT = "night"
    JOUR = "1jour"

    @property
    def is_night(self) -> bool:
        return self == LyftType.NIGHT


@dataclass
class Lift:
    type: LyftType
    age: int | None = None
    date: LyftDate | None = None

    def calculate_cost(self, lifts_repository: LiftsRepository) -> int:
        cost = lifts_repository.get_price_for_lift(self.type)

        if self.age and self.age < 6:
            return 0

        if self.type.is_night:
            return self._calculate_cost_for_one_night_lift(cost)

        return self._calculate_cost_for_non_night_lifts(cost, lifts_repository)

    def _calculate_cost_for_one_night_lift(self, cost: int) -> int:
        if not self.age:
            return 0
        if 6 < self.age and self.age > 64:
            return math.ceil(cost * 0.4)
        return cost

    def _calculate_cost_for_non_night_lifts(
        self, cost: int, lifts_repository: LiftsRepository
    ) -> int:
        reduction = 0
        is_holiday = lifts_repository.is_holiday(self.date)
        if not is_holiday and self.date and self.date.is_monday():
            reduction = 35

        # TODO: apply reduction for others
        if self.age and self.age < 15:
            return math.ceil(cost * 0.7)

        if not self.age:
            new_cost = cost * (1 - reduction / 100)
            return math.ceil(new_cost)

        if self.age > 64:
            new_cost = cost * 0.75 * (1 - reduction / 100)
            return math.ceil(new_cost)

        new_cost = cost * (1 - reduction / 100)
        return math.ceil(new_cost)
