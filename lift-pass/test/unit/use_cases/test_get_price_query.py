from doublex import Stub, Mimic, Spy
from doublex_expects import have_been_called_with
from expects import expect

from src.infrastructure.sql_lifts_repository import SqlLiftsRepository
from src.use_cases.queries.get_lift_price_query import (
    GetLiftPriceQuery,
    GetLiftPriceQueryHandler,
)


class TestGetPriceQueryHandler:
    def test_calculates_cost(self) -> None:
        lift = Spy()
        get_price_query = GetLiftPriceQuery(lift)
        repository = Mimic(Stub, SqlLiftsRepository)
        get_price_query_handler = GetLiftPriceQueryHandler(repository)

        get_price_query_handler.execute(get_price_query)

        expect(lift.calculate_cost).to(have_been_called_with(repository))
