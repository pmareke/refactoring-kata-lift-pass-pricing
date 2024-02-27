from datetime import datetime

from doublex import Stub, Mimic, ANY_ARG
from expects import expect, equal

from src.domain.lift import Lift
from src.domain.lift_date import LyftDate
from src.domain.lift_type import LyftType
from src.infrastructure.sql_lifts_repository import SqlLiftsRepository
from src.use_cases.queries.get_lift_price_query import (
    GetLiftPriceQuery,
    GetLiftPriceQueryHandler,
)


class TestGetPriceQueryHandler:
    def test_nights_are_free(self) -> None:
        cost = 100
        lift = Lift(LyftType.NIGHT)
        get_price_query = GetLiftPriceQuery(lift)
        with Mimic(Stub, SqlLiftsRepository) as repository:
            repository.get_price_for_lift(lift.type).returns(cost)
            repository.is_holiday(ANY_ARG).returns(False)
        get_price_query_handler = GetLiftPriceQueryHandler(repository)

        lift_cost = get_price_query_handler.execute(get_price_query)

        expect(lift_cost).to(equal(0))

    def test_people_under_6_not_pay_nights(self) -> None:
        cost = 100
        age = 5
        lift = Lift(LyftType.NIGHT, age)
        get_price_query = GetLiftPriceQuery(lift)
        with Mimic(Stub, SqlLiftsRepository) as repository:
            repository.get_price_for_lift(lift.type).returns(cost)
            repository.is_holiday(ANY_ARG).returns(False)
        get_price_query_handler = GetLiftPriceQueryHandler(repository)

        lift_cost = get_price_query_handler.execute(get_price_query)

        expect(lift_cost).to(equal(0))

    def test_nights_with_age_above_6_has_not_discount(self) -> None:
        cost = 100
        age = 40
        lift = Lift(LyftType.NIGHT, age)
        get_price_query = GetLiftPriceQuery(lift)
        with Mimic(Stub, SqlLiftsRepository) as repository:
            repository.get_price_for_lift(lift.type).returns(cost)
            repository.is_holiday(ANY_ARG).returns(False)
        get_price_query_handler = GetLiftPriceQueryHandler(repository)

        lift_cost = get_price_query_handler.execute(get_price_query)

        expect(lift_cost).to(equal(cost))

    def test_nights_with_age_above_64_has_40_percentage_discount(self) -> None:
        cost = 100
        age = 65
        lift = Lift(LyftType.NIGHT, age)
        get_price_query = GetLiftPriceQuery(lift)
        with Mimic(Stub, SqlLiftsRepository) as repository:
            repository.get_price_for_lift(lift.type).returns(cost)
            repository.is_holiday(ANY_ARG).returns(False)
        get_price_query_handler = GetLiftPriceQueryHandler(repository)

        lift_cost = get_price_query_handler.execute(get_price_query)

        expect(lift_cost).to(equal(cost * 0.4))

    def test_1jour_has_not_discount(self) -> None:
        cost = 100
        lift = Lift(LyftType.JOUR)
        get_price_query = GetLiftPriceQuery(lift)
        with Mimic(Stub, SqlLiftsRepository) as repository:
            repository.get_price_for_lift(lift.type).returns(cost)
            repository.is_holiday(ANY_ARG).returns(False)
        get_price_query_handler = GetLiftPriceQueryHandler(repository)

        lift_cost = get_price_query_handler.execute(get_price_query)

        expect(lift_cost).to(equal(cost))

    def test_people_under_6_not_pay_1jour(self) -> None:
        cost = 100
        age = 5
        lift = Lift(LyftType.JOUR, age)
        get_price_query = GetLiftPriceQuery(lift)
        with Mimic(Stub, SqlLiftsRepository) as repository:
            repository.get_price_for_lift(lift.type).returns(cost)
            repository.is_holiday(ANY_ARG).returns(False)
        get_price_query_handler = GetLiftPriceQueryHandler(repository)

        lift_cost = get_price_query_handler.execute(get_price_query)

        expect(lift_cost).to(equal(0))

    def test_people_under_15_has_30_percent_discount(self) -> None:
        cost = 100
        age = 14
        lift = Lift(LyftType.JOUR, age)
        get_price_query = GetLiftPriceQuery(lift)
        with Mimic(Stub, SqlLiftsRepository) as repository:
            repository.get_price_for_lift(lift.type).returns(cost)
            repository.is_holiday(ANY_ARG).returns(False)
        get_price_query_handler = GetLiftPriceQueryHandler(repository)

        lift_cost = get_price_query_handler.execute(get_price_query)

        expect(lift_cost).to(equal(cost * 0.7))

    def test_people_between_16_and_6O_has_not_discount(self) -> None:
        cost = 100
        age = 50
        lift = Lift(LyftType.JOUR, age)
        get_price_query = GetLiftPriceQuery(lift)
        with Mimic(Stub, SqlLiftsRepository) as repository:
            repository.get_price_for_lift(lift.type).returns(cost)
            repository.is_holiday(ANY_ARG).returns(False)
        get_price_query_handler = GetLiftPriceQueryHandler(repository)

        lift_cost = get_price_query_handler.execute(get_price_query)

        expect(lift_cost).to(equal(cost))

    def test_people_above_64_has_25_percent_discount(self) -> None:
        cost = 100
        age = 65
        lift = Lift(LyftType.JOUR, age)
        get_price_query = GetLiftPriceQuery(lift)
        with Mimic(Stub, SqlLiftsRepository) as repository:
            repository.get_price_for_lift(lift.type).returns(cost)
            repository.is_holiday(ANY_ARG).returns(False)
        get_price_query_handler = GetLiftPriceQueryHandler(repository)

        lift_cost = get_price_query_handler.execute(get_price_query)

        expect(lift_cost).to(equal(cost * 0.75))

    def test_1jour_holidays_has_not_discount(self) -> None:
        cost = 100
        date = datetime.fromisoformat("2019-02-18")
        lift_date = LyftDate(date)
        lift = Lift(LyftType.JOUR, date=lift_date)
        get_price_query = GetLiftPriceQuery(lift)
        with Mimic(Stub, SqlLiftsRepository) as repository:
            repository.get_price_for_lift(lift.type).returns(cost)
            repository.is_holiday(lift_date).returns(True)
        get_price_query_handler = GetLiftPriceQueryHandler(repository)

        lift_cost = get_price_query_handler.execute(get_price_query)

        expect(lift_cost).to(equal(cost))

    def test_1jour_not_on_holidays_has_35_percent_discount(self) -> None:
        cost = 100
        date = datetime.fromisoformat("2024-02-26")
        lift_date = LyftDate(date)
        lift = Lift(LyftType.JOUR, date=lift_date)
        get_price_query = GetLiftPriceQuery(lift)
        with Mimic(Stub, SqlLiftsRepository) as repository:
            repository.get_price_for_lift(lift.type).returns(cost)
            repository.is_holiday(ANY_ARG).returns(False)
        get_price_query_handler = GetLiftPriceQueryHandler(repository)

        lift_cost = get_price_query_handler.execute(get_price_query)

        expect(lift_cost).to(equal(cost * 0.65))
