from doublex import Spy, Mimic
from doublex_expects import have_been_called_with
from expects import expect

from src.infrastructure.sql_trips_repository import SqlTripsRepository
from src.use_cases.commands.update_prices_command import (
    UpdatePricesCommand,
    UpdatePricesCommandHandler,
)


class TestUpdatePricesCommandHandler:
    def test_execute(self) -> None:
        trip_type = "night"
        cost = 100
        update_prices_command = UpdatePricesCommand(cost, trip_type)
        repository = Mimic(Spy, SqlTripsRepository)
        update_prices_command_handler = UpdatePricesCommandHandler(repository)

        update_prices_command_handler.execute(update_prices_command)

        expect(repository.add_price).to(have_been_called_with(trip_type, cost))
