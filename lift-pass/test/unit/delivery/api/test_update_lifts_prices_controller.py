from doublex import Mimic, Spy
from doublex_expects import have_been_called
from expects import expect

from src.delivery.api.update_lifts_prices_controller import UpdateLiftsPricesController
from src.domain.lift_type import LyftType
from src.main import create_app
from src.use_cases.commands.update_lifts_prices_command import (
    UpdateLiftsPricesCommandHandler,
)


class TestUpdateLiftsPricesController:

    def test_update_lift_prices(self) -> None:
        cost = 100
        lift_type = LyftType.NIGHT
        command_handler = Mimic(Spy, UpdateLiftsPricesCommandHandler)
        controller = UpdateLiftsPricesController(command_handler)
        url_path = f"/prices?cost={cost}&type={lift_type.value}"

        with create_app().test_request_context(path=url_path):
            controller.update_lifts_prices()

        expect(command_handler.execute).to(have_been_called)
