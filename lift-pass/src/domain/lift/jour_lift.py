import math
from dataclasses import dataclass

from src.domain.lift.lift import Lift
from src.domain.lift.lift_date import LyftDate
from src.domain.lift.lift_type import LyftType
from src.domain.lift.lifts_repository import LiftsRepository


@dataclass
class JourLift(Lift):
    age: int | None = None
    date: LyftDate | None = None

    def calculate_cost(self, lifts_repository: LiftsRepository) -> int:
        cost = lifts_repository.get_price_for_lift(LyftType.JOUR)

        if self.age and self.age < 6:
            return 0

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
