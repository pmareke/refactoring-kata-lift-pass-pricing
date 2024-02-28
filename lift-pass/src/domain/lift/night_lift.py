import math
from dataclasses import dataclass

from src.domain.lift.lift import Lift
from src.domain.lift.lift_date import LyftDate
from src.domain.lift.lift_type import LyftType
from src.domain.lift.lifts_repository import LiftsRepository


@dataclass
class NightLift(Lift):
    age: int | None = None
    date: LyftDate | None = None

    def calculate_cost(self, lifts_repository: LiftsRepository) -> int:
        cost = lifts_repository.get_price_for_lift(LyftType.NIGHT)

        if self.age and self.age < 6:
            return 0

        if not self.age:
            return 0

        if 6 < self.age and self.age > 64:
            return math.ceil(cost * 0.4)

        return cost
