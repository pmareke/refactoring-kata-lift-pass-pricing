from datetime import datetime

from doublex import Spy, Stub, Mimic
from doublex_expects import have_been_called_with
from expects import expect, equal
from pymysql.cursors import Cursor

from src.use_cases.get_price_query_handler import GetPriceQuery, GetPriceQueryHandler
from src.use_cases.update_prices_command import (
    UpdatePricesCommand,
    UpdatePricesCommandHandler,
)


class TestGetPriceQueryHandler:
    def test_nights_are_free(self) -> None:
        cost = 100
        trip_type = "night"
        get_price_query = GetPriceQuery(trip_type)
        with Mimic(Stub, Cursor) as cursor:
            cursor.fetchone().returns([cost])
            cursor.fetchall().returns([])
        get_price_query_handler = GetPriceQueryHandler(cursor)

        response = get_price_query_handler.execute(get_price_query)

        expect(response).to(equal({"cost": 0}))

    def test_people_under_6_not_pay_nights(self) -> None:
        trip_type = "night"
        age = 5
        cost = 100
        get_price_query = GetPriceQuery(trip_type, age)
        with Mimic(Stub, Cursor) as cursor:
            cursor.fetchone().returns([cost])
            cursor.fetchall().returns([])
        get_price_query_handler = GetPriceQueryHandler(cursor)

        response = get_price_query_handler.execute(get_price_query)

        expect(response).to(equal({"cost": 0}))

    def test_nights_with_age_above_6_has_not_discount(self) -> None:
        trip_type = "night"
        age = 40
        cost = 100
        get_price_query = GetPriceQuery(trip_type, age)
        with Mimic(Stub, Cursor) as cursor:
            cursor.fetchone().returns([cost])
            cursor.fetchall().returns([])
        get_price_query_handler = GetPriceQueryHandler(cursor)

        response = get_price_query_handler.execute(get_price_query)

        expect(response).to(equal({"cost": cost}))

    def test_nights_with_age_above_64_has_40_percentage_discount(self) -> None:
        trip_type = "night"
        age = 65
        cost = 100
        get_price_query = GetPriceQuery(trip_type, age)
        with Mimic(Stub, Cursor) as cursor:
            cursor.fetchone().returns([cost])
            cursor.fetchall().returns([])
        get_price_query_handler = GetPriceQueryHandler(cursor)

        response = get_price_query_handler.execute(get_price_query)

        expect(response).to(equal({"cost": cost * 0.4}))

    def test_1jour_has_not_discount(self) -> None:
        cost = 100
        trip_type = "1jour"
        get_price_query = GetPriceQuery(trip_type)
        with Mimic(Stub, Cursor) as cursor:
            cursor.fetchone().returns([cost])
            cursor.fetchall().returns([])
        get_price_query_handler = GetPriceQueryHandler(cursor)

        response = get_price_query_handler.execute(get_price_query)

        expect(response).to(equal({"cost": cost}))

    def test_people_under_6_not_pay_1jour(self) -> None:
        trip_type = "1jour"
        age = 5
        cost = 100
        get_price_query = GetPriceQuery(trip_type, age)
        with Mimic(Stub, Cursor) as cursor:
            cursor.fetchone().returns([cost])
            cursor.fetchall().returns([])
        get_price_query_handler = GetPriceQueryHandler(cursor)

        response = get_price_query_handler.execute(get_price_query)

        expect(response).to(equal({"cost": 0}))

    def test_people_under_15_has_30_percent_discount(self) -> None:
        trip_type = "1jour"
        age = 14
        cost = 100
        get_price_query = GetPriceQuery(trip_type, age)
        with Mimic(Stub, Cursor) as cursor:
            cursor.fetchone().returns([cost])
            cursor.fetchall().returns([])
        get_price_query_handler = GetPriceQueryHandler(cursor)

        response = get_price_query_handler.execute(get_price_query)

        expect(response).to(equal({"cost": cost * 0.7}))

    def test_people_between_16_and_6O_has_not_discount(self) -> None:
        trip_type = "1jour"
        age = 50
        cost = 100
        get_price_query = GetPriceQuery(trip_type, age)
        with Mimic(Stub, Cursor) as cursor:
            cursor.fetchone().returns([cost])
            cursor.fetchall().returns([])
        get_price_query_handler = GetPriceQueryHandler(cursor)

        response = get_price_query_handler.execute(get_price_query)

        expect(response).to(equal({"cost": cost}))

    def test_people_above_64_has_25_percent_discount(self) -> None:
        trip_type = "1jour"
        age = 65
        cost = 100
        get_price_query = GetPriceQuery(trip_type, age)
        with Mimic(Stub, Cursor) as cursor:
            cursor.fetchone().returns([cost])
            cursor.fetchall().returns([])
        get_price_query_handler = GetPriceQueryHandler(cursor)

        response = get_price_query_handler.execute(get_price_query)

        expect(response).to(equal({"cost": cost * 0.75}))

    def test_1jour_holidays_has_not_discount(self) -> None:
        trip_type = "1jour"
        date = "2019-02-18"
        cost = 100
        get_price_query = GetPriceQuery(trip_type, date=date)
        with Mimic(Stub, Cursor) as cursor:
            cursor.fetchone().returns([cost])
            cursor.fetchall().returns([(datetime.fromisoformat(date), "1jour")])
        get_price_query_handler = GetPriceQueryHandler(cursor)

        response = get_price_query_handler.execute(get_price_query)

        expect(response).to(equal({"cost": cost}))

    def test_1jour_not_on_holidays_has_35_percent_discount(self) -> None:
        trip_type = "1jour"
        date = "2024-02-26"
        cost = 100
        get_price_query = GetPriceQuery(trip_type, date=date)
        with Mimic(Stub, Cursor) as cursor:
            cursor.fetchone().returns([cost])
            cursor.fetchall().returns([])
        get_price_query_handler = GetPriceQueryHandler(cursor)

        response = get_price_query_handler.execute(get_price_query)

        expect(response).to(equal({"cost": cost * 0.65}))
