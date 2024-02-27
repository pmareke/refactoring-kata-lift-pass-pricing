from doublex import Mimic, Spy
from doublex_expects import have_been_called
from expects import expect

from src.delivery.api.update_prices_controller import UpdatePricesController
from src.main import app
from src.use_cases.commands.update_prices_command import (
    UpdatePricesCommandHandler,
)


class TestUpdatePricesController:

    def test_update_prices(self) -> None:
        cost = 100
        trip_type = "night"
        command_handler = Mimic(Spy, UpdatePricesCommandHandler)
        controller = UpdatePricesController(command_handler)
        url_path = f"/prices?cost={cost}&type={trip_type}"

        with app.test_request_context(path=url_path):
            controller.update_prices()

        expect(command_handler.execute).to(have_been_called)
