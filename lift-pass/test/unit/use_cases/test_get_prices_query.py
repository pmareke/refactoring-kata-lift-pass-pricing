from datetime import datetime

from doublex import Stub, Mimic, ANY_ARG
from expects import expect, equal

from src.domain.lift.jour_lift import JourLift
from src.domain.lift.lift_date import LyftDate
from src.domain.lift.lift_type import LyftType
from src.domain.lift.night_lift import NightLift
from src.infrastructure.sql_lifts_repository import SqlLiftsRepository
from src.use_cases.queries.get_lift_prices_query import (
    GetLiftPricesQuery,
    GetLiftPricesQueryHandler,
)


class TestGetPricesQueryHandler:
    def test_calculates_costs(self) -> None:
        cost = 0
        age = 1
        date = LyftDate(datetime.fromisoformat("2021-01-01"))
        night_lift = NightLift(age=age, date=date)
        jour_lift = JourLift(age=age, date=date)
        get_prices_query = GetLiftPricesQuery(lifts=[night_lift, jour_lift])
        repository = Mimic(Stub, SqlLiftsRepository)
        get_prices_query_handler = GetLiftPricesQueryHandler(repository)

        costs = get_prices_query_handler.execute(get_prices_query)

        expect(costs).to(
            equal(
                [
                    {
                        "type": "night",
                        "age": night_lift.age,
                        "date": night_lift.date,
                        "cost": cost,
                    },
                    {
                        "type": "1jour",
                        "age": jour_lift.age,
                        "date": jour_lift.date,
                        "cost": cost,
                    },
                ]
            )
        )

    def test_calculates_costs_without_date(self) -> None:
        cost = 0
        age = 1
        night_lift = NightLift(age=age)
        jour_lift = JourLift(age=age)
        get_prices_query = GetLiftPricesQuery(lifts=[night_lift, jour_lift])
        repository = Mimic(Stub, SqlLiftsRepository)
        get_prices_query_handler = GetLiftPricesQueryHandler(repository)

        costs = get_prices_query_handler.execute(get_prices_query)

        expect(costs).to(
            equal(
                [
                    {"type": "night", "age": night_lift.age, "cost": cost},
                    {"type": "1jour", "age": jour_lift.age, "cost": cost},
                ]
            )
        )

    def test_calculates_costs_without_age(self) -> None:
        cost = 0
        date = LyftDate(datetime.fromisoformat("2021-01-01"))
        night_lift = NightLift(date=date)
        jour_lift = JourLift(date=date)
        get_prices_query = GetLiftPricesQuery(lifts=[night_lift, jour_lift])
        with Mimic(Stub, SqlLiftsRepository) as repository:
            repository.get_price_for_lift(LyftType.NIGHT).returns(cost)
            repository.get_price_for_lift(LyftType.JOUR).returns(cost)
            repository.is_holiday(ANY_ARG).returns(True)
        get_prices_query_handler = GetLiftPricesQueryHandler(repository)

        costs = get_prices_query_handler.execute(get_prices_query)

        expect(costs).to(
            equal(
                [
                    {"type": "night", "date": night_lift.date, "cost": cost},
                    {"type": "1jour", "date": jour_lift.date, "cost": cost},
                ]
            )
        )
