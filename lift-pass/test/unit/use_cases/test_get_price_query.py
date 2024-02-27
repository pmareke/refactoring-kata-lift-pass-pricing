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
    def test_cost_should_be_zero(self):
        trip_type = "night"
        get_price_query = GetPriceQuery(trip_type)
        with Mimic(Stub, Cursor) as cursor:
            cursor.fetchone().returns([100])
            cursor.fetchall().returns([])
        get_price_query_handler = GetPriceQueryHandler(cursor)

        response = get_price_query_handler.execute(get_price_query)

        expect(response).to(equal({"cost": 0}))
