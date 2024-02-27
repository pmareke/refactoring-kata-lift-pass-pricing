from doublex import Mimic, Spy
from doublex_expects import have_been_called
from expects import expect

from src.delivery.api.get_price_controller import GetPriceController
from src.main import create_app
from src.use_cases.queries.get_price_query import GetPriceQueryHandler


class TestGetPriceController:
    def test_get_price(self) -> None:
        handler = Mimic(Spy, GetPriceQueryHandler)
        controller = GetPriceController(handler)
        url_path = "/prices?type=night"

        with create_app().test_request_context(path=url_path):
            controller.get_price()

        expect(handler.execute).to(have_been_called)
