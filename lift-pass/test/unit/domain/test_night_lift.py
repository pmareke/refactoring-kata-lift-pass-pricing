import math

from doublex import Stub, Mimic
from expects import expect, equal

from src.domain.lift import Lift
from src.domain.lift_type import LyftType
from src.infrastructure.sql_lifts_repository import SqlLiftsRepository


class TestNightLift:
    def test_nights_are_free(self) -> None:
        lift = Lift(LyftType.NIGHT)
        lifts_repository = Stub()

        cost = lift.calculate_cost(lifts_repository)

        expect(cost).to(equal(0))

    def test_people_under_6_not_pay(self) -> None:
        lift = Lift(LyftType.NIGHT, age=5)
        lifts_repository = Stub()

        cost = lift.calculate_cost(lifts_repository)

        expect(cost).to(equal(0))

    def test_nights_with_age_above_6_has_not_discount(self) -> None:
        lift = Lift(LyftType.NIGHT, age=40)
        with Mimic(Stub, SqlLiftsRepository) as lifts_repository:
            lifts_repository.get_price_for_lift(LyftType.NIGHT).returns(19)

        cost = lift.calculate_cost(lifts_repository)

        expect(cost).to(equal(19))

    def test_nights_with_age_above_64_has_40_percentage_discount(self) -> None:
        lift = Lift(LyftType.NIGHT, age=65)
        cost = 19
        with Mimic(Stub, SqlLiftsRepository) as lifts_repository:
            lifts_repository.get_price_for_lift(LyftType.NIGHT).returns(cost)

        lift_cost = lift.calculate_cost(lifts_repository)

        expect(lift_cost).to(equal(math.ceil(cost * 0.4)))
