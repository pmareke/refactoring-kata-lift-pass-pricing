from doublex import Spy, Mimic
from doublex_expects import have_been_called_with
from expects import expect

from src.domain.lift.lift_type import LyftType
from src.infrastructure.sql_lifts_repository import SqlLiftsRepository
from src.use_cases.commands.update_lifts_prices_command import (
    UpdateLiftsPricesCommand,
    UpdateLiftsPricesCommandHandler,
)


class TestUpdatePricesCommandHandler:
    def test_execute(self) -> None:
        cost = 100
        lyft_type = LyftType.NIGHT
        update_prices_command = UpdateLiftsPricesCommand(cost, lyft_type)
        repository = Mimic(Spy, SqlLiftsRepository)
        update_prices_command_handler = UpdateLiftsPricesCommandHandler(repository)

        update_prices_command_handler.execute(update_prices_command)

        expect(repository.add_price).to(have_been_called_with(lyft_type, cost))
