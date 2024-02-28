import math
from dataclasses import dataclass

from src.domain.lift.lift import Lift
from src.domain.lift.lift_date import LyftDate
from src.domain.lift.lift_type import LyftType
from src.domain.lift.lifts_repository import LiftsRepository


@dataclass
class JourLift(Lift):
    type: LyftType = LyftType.JOUR
    age: int | None = None
    date: LyftDate | None = None

    ZERO_COST = 0
    ZERO_REDUCTION = 0
    THIRTY_FIVE_REDUCTION = 35

    SEVENTY_DISCOUNT = 0.7
    SEVENTY_FIVE_DISCOUNT = 0.75

    SIX_YEARS_OLD = 6
    FIFTEEN_YEARS_OLD = 15
    SIXTY_FOUR_YEARS_OLD = 64

    def date_iso_format(self) -> str:
        assert self.date
        return self.date.date.strftime("%Y-%m-%d")

    def calculate_cost(self, lifts_repository: LiftsRepository) -> int:
        cost = lifts_repository.get_price_for_lift(self.type)
        reduction = self._calculate_reduction(lifts_repository)
        discount = self._calculate_discount(reduction)

        if not self.age:
            return math.ceil(cost * discount)

        if self._is_younger_than_six():
            return self.ZERO_COST

        # TODO: apply reduction for others
        if self._is_younger_than_fifteen():
            return math.ceil(cost * self.SEVENTY_DISCOUNT)

        if self._is_older_than_sixty_four():
            return math.ceil(cost * self.SEVENTY_FIVE_DISCOUNT * discount)

        new_cost = cost * discount
        return math.ceil(new_cost)

    @staticmethod
    def _calculate_discount(reduction: int) -> float:
        return 1 - reduction / 100

    def _calculate_reduction(self, lifts_repository: LiftsRepository) -> int:
        if not self.date:
            return self.ZERO_REDUCTION

        is_holiday = lifts_repository.is_holiday(self.date)
        if is_holiday:
            return self.ZERO_REDUCTION

        if self.date.is_monday():
            return self.THIRTY_FIVE_REDUCTION

        return self.ZERO_REDUCTION

    def _is_younger_than_six(self) -> bool:
        assert self.age
        return bool(self.age < self.SIX_YEARS_OLD)

    def _is_younger_than_fifteen(self) -> bool:
        assert self.age
        return bool(self.age < self.FIFTEEN_YEARS_OLD)

    def _is_older_than_sixty_four(self) -> bool:
        assert self.age
        return bool(self.age > self.SIXTY_FOUR_YEARS_OLD)
