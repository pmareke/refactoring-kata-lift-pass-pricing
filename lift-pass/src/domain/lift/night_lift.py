import math
from dataclasses import dataclass

from src.domain.lift.lift import Lift
from src.domain.lift.lift_date import LyftDate
from src.domain.lift.lift_type import LyftType
from src.domain.lift.lifts_repository import LiftsRepository


@dataclass
class NightLift(Lift):

    type: LyftType = LyftType.NIGHT
    age: int | None = None
    date: LyftDate | None = None

    NO_COST = 0
    SIX_YEARS_OLD = 6
    SIXTY_FOUR_YEARS_OLD = 64

    def date_iso_format(self) -> str:
        assert self.date
        return self.date.date.strftime("%Y-%m-%d")

    def calculate_cost(self, lifts_repository: LiftsRepository) -> int:
        cost = lifts_repository.get_price_for_lift(self.type)

        if not self.age:
            return self.NO_COST

        if self._is_younger_than_six():
            return self.NO_COST

        if self._is_older_than_sixty_four():
            return math.ceil(cost * 0.4)

        return cost

    def _is_younger_than_six(self) -> bool:
        assert self.age
        return bool(self.age < self.SIX_YEARS_OLD)

    def _is_older_than_sixty_four(self) -> bool:
        assert self.age
        return bool(self.age > self.SIXTY_FOUR_YEARS_OLD)
