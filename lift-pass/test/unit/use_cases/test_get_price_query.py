from datetime import datetime

from doublex import Stub, Mimic
from expects import expect, equal

from src.domain.lift import Lift, LyftType
from src.infrastructure.sql_lifts_repository import SqlLiftsRepository
from src.use_cases.queries.get_lift_price_query import GetLiftPriceQuery, GetLiftPriceQueryHandler


class TestGetPriceQueryHandler:
    def test_nights_are_free(self) -> None:
        cost = 100
        lift = Lift(LyftType.NIGHT)
        get_price_query = GetLiftPriceQuery(lift)
        with Mimic(Stub, SqlLiftsRepository) as repository:
            repository.get_price_for_lift(lift.type.value).returns(cost)
            repository.find_all_holidays().returns([])
        get_price_query_handler = GetLiftPriceQueryHandler(repository)

        response = get_price_query_handler.execute(get_price_query)

        expect(response).to(equal({"cost": 0}))

    def test_people_under_6_not_pay_nights(self) -> None:
        age = 5
        lift = Lift(LyftType.NIGHT, age)
        cost = 100
        get_price_query = GetLiftPriceQuery(lift)
        with Mimic(Stub, SqlLiftsRepository) as repository:
            repository.get_price_for_lift(lift.type.value).returns(cost)
            repository.find_all_holidays().returns([])
        get_price_query_handler = GetLiftPriceQueryHandler(repository)

        response = get_price_query_handler.execute(get_price_query)

        expect(response).to(equal({"cost": 0}))

    def test_nights_with_age_above_6_has_not_discount(self) -> None:
        age = 40
        lift = Lift(LyftType.NIGHT, age)
        cost = 100
        get_price_query = GetLiftPriceQuery(lift)
        with Mimic(Stub, SqlLiftsRepository) as repository:
            repository.get_price_for_lift(lift.type.value).returns(cost)
            repository.find_all_holidays().returns([])
        get_price_query_handler = GetLiftPriceQueryHandler(repository)

        response = get_price_query_handler.execute(get_price_query)

        expect(response).to(equal({"cost": cost}))

    def test_nights_with_age_above_64_has_40_percentage_discount(self) -> None:
        age = 65
        lift = Lift(LyftType.NIGHT, age)
        cost = 100
        get_price_query = GetLiftPriceQuery(lift)
        with Mimic(Stub, SqlLiftsRepository) as repository:
            repository.get_price_for_lift(lift.type.value).returns(cost)
            repository.find_all_holidays().returns([])
        get_price_query_handler = GetLiftPriceQueryHandler(repository)

        response = get_price_query_handler.execute(get_price_query)

        expect(response).to(equal({"cost": cost * 0.4}))

    def test_1jour_has_not_discount(self) -> None:
        cost = 100
        lift = Lift(LyftType.JOUR)
        get_price_query = GetLiftPriceQuery(lift)
        with Mimic(Stub, SqlLiftsRepository) as repository:
            repository.get_price_for_lift(lift.type.value).returns(cost)
            repository.find_all_holidays().returns([])
        get_price_query_handler = GetLiftPriceQueryHandler(repository)

        response = get_price_query_handler.execute(get_price_query)

        expect(response).to(equal({"cost": cost}))

    def test_people_under_6_not_pay_1jour(self) -> None:
        age = 5
        lift = Lift(LyftType.JOUR, age)
        cost = 100
        get_price_query = GetLiftPriceQuery(lift)
        with Mimic(Stub, SqlLiftsRepository) as repository:
            repository.get_price_for_lift(lift.type.value).returns(cost)
            repository.find_all_holidays().returns([])
        get_price_query_handler = GetLiftPriceQueryHandler(repository)

        response = get_price_query_handler.execute(get_price_query)

        expect(response).to(equal({"cost": 0}))

    def test_people_under_15_has_30_percent_discount(self) -> None:
        trip_type = "1jour"
        age = 14
        lift = Lift(LyftType.JOUR, age)
        cost = 100
        get_price_query = GetLiftPriceQuery(lift)
        with Mimic(Stub, SqlLiftsRepository) as repository:
            repository.get_price_for_lift(lift.type.value).returns(cost)
            repository.find_all_holidays().returns([])
        get_price_query_handler = GetLiftPriceQueryHandler(repository)

        response = get_price_query_handler.execute(get_price_query)

        expect(response).to(equal({"cost": cost * 0.7}))

    def test_people_between_16_and_6O_has_not_discount(self) -> None:
        age = 50
        lift = Lift(LyftType.JOUR, age)
        cost = 100
        get_price_query = GetLiftPriceQuery(lift)
        with Mimic(Stub, SqlLiftsRepository) as repository:
            repository.get_price_for_lift(lift.type.value).returns(cost)
            repository.find_all_holidays().returns([])
        get_price_query_handler = GetLiftPriceQueryHandler(repository)

        response = get_price_query_handler.execute(get_price_query)

        expect(response).to(equal({"cost": cost}))

    def test_people_above_64_has_25_percent_discount(self) -> None:
        age = 65
        lift = Lift(LyftType.JOUR, age)
        cost = 100
        get_price_query = GetLiftPriceQuery(lift)
        with Mimic(Stub, SqlLiftsRepository) as repository:
            repository.get_price_for_lift(lift.type.value).returns(cost)
            repository.find_all_holidays().returns([])
        get_price_query_handler = GetLiftPriceQueryHandler(repository)

        response = get_price_query_handler.execute(get_price_query)

        expect(response).to(equal({"cost": cost * 0.75}))

    def test_1jour_holidays_has_not_discount(self) -> None:
        date = "2019-02-18"
        cost = 100
        lift = Lift(LyftType.JOUR, date=date)
        get_price_query = GetLiftPriceQuery(lift)
        with Mimic(Stub, SqlLiftsRepository) as repository:
            repository.get_price_for_lift(lift.type.value).returns(cost)
            repository.find_all_holidays().returns(
                [(datetime.fromisoformat(date), "1jour")]
            )
        get_price_query_handler = GetLiftPriceQueryHandler(repository)

        response = get_price_query_handler.execute(get_price_query)

        expect(response).to(equal({"cost": cost}))

    def test_1jour_not_on_holidays_has_35_percent_discount(self) -> None:
        date = "2024-02-26"
        cost = 100
        lift = Lift(LyftType.JOUR, date=date)
        get_price_query = GetLiftPriceQuery(lift)
        with Mimic(Stub, SqlLiftsRepository) as repository:
            repository.get_price_for_lift(lift.type.value).returns(cost)
            repository.find_all_holidays().returns([])
        get_price_query_handler = GetLiftPriceQueryHandler(repository)

        response = get_price_query_handler.execute(get_price_query)

        expect(response).to(equal({"cost": cost * 0.65}))
