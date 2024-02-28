import math
from datetime import datetime

from doublex import Stub, Mimic, ANY_ARG
from expects import expect, equal

from src.domain.lift.jour_lift import JourLift
from src.domain.lift.lift_date import LyftDate
from src.domain.lift.lift_type import LyftType
from src.infrastructure.sql_lifts_repository import SqlLiftsRepository


class TestJourLift:
    def test_1jour_type(self) -> None:
        lift = JourLift()
        cost = 19
        with Mimic(Stub, SqlLiftsRepository) as lifts_repository:
            lifts_repository.get_price_for_lift(LyftType.JOUR).returns(cost)

        lift_cost = lift.calculate_cost(lifts_repository)

        expect(lift_cost).to(equal(19))

    def test_people_under_6_not_pay(self) -> None:
        lift = JourLift(age=5)
        cost = 19
        with Mimic(Stub, SqlLiftsRepository) as lifts_repository:
            lifts_repository.get_price_for_lift(LyftType.JOUR).returns(cost)

        lift_cost = lift.calculate_cost(lifts_repository)

        expect(lift_cost).to(equal(0))

    def test_1jour_type_with_age_bellow_15(self) -> None:
        lift = JourLift(age=14)
        cost = 19
        with Mimic(Stub, SqlLiftsRepository) as lifts_repository:
            lifts_repository.get_price_for_lift(LyftType.JOUR).returns(cost)

        lift_cost = lift.calculate_cost(lifts_repository)

        expect(lift_cost).to(equal(math.ceil(cost * 0.7)))

    def test_1jour_type_with_age_between_16_and_63(self) -> None:
        lift = JourLift(age=50)
        cost = 19
        with Mimic(Stub, SqlLiftsRepository) as lifts_repository:
            lifts_repository.get_price_for_lift(LyftType.JOUR).returns(cost)

        lift_cost = lift.calculate_cost(lifts_repository)

        expect(lift_cost).to(equal(cost))

    def test_1jour_type_with_age_above_64(self) -> None:
        lift = JourLift(age=65)
        cost = 19
        with Mimic(Stub, SqlLiftsRepository) as lifts_repository:
            lifts_repository.get_price_for_lift(LyftType.JOUR).returns(cost)

        lift_cost = lift.calculate_cost(lifts_repository)

        expect(lift_cost).to(equal(math.ceil(cost * 0.75)))

    def test_1jour_type_on_holidays(self) -> None:
        date = datetime.fromisoformat("2019-02-18")
        lift_date = LyftDate(date)
        lift = JourLift(date=lift_date)
        cost = 19
        with Mimic(Stub, SqlLiftsRepository) as lifts_repository:
            lifts_repository.get_price_for_lift(LyftType.JOUR).returns(cost)
            lifts_repository.is_holiday(ANY_ARG).returns(True)

        lift_cost = lift.calculate_cost(lifts_repository)

        expect(lift_cost).to(equal(cost))

    def test_1jour_type_not_on_holidays_but_monday(self) -> None:
        date = datetime.fromisoformat("2019-02-18")
        lift_date = LyftDate(date)
        lift = JourLift(date=lift_date)
        cost = 19
        with Mimic(Stub, SqlLiftsRepository) as lifts_repository:
            lifts_repository.get_price_for_lift(LyftType.JOUR).returns(cost)
            lifts_repository.is_holiday(ANY_ARG).returns(False)

        lift_cost = lift.calculate_cost(lifts_repository)

        expect(lift_cost).to(equal(math.ceil(cost * 0.65)))

    def test_1jour_type_not_on_holidays_neither_monday(self) -> None:
        date = datetime.fromisoformat("2019-02-19")
        lift_date = LyftDate(date)
        lift = JourLift(date=lift_date)
        cost = 19
        with Mimic(Stub, SqlLiftsRepository) as lifts_repository:
            lifts_repository.get_price_for_lift(LyftType.JOUR).returns(cost)
            lifts_repository.is_holiday(ANY_ARG).returns(False)

        lift_cost = lift.calculate_cost(lifts_repository)

        expect(lift_cost).to(equal(cost))