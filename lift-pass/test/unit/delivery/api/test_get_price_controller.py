from doublex import Mimic, Spy
from doublex_expects import have_been_called
from expects import expect

from src.delivery.api.get_price_controller import GetPriceController
from src.main import app
from src.use_cases.get_price_query_handler import GetPriceQueryHandler


class TestGetPriceController:
    def test_get_price(self) -> None:
        handler = Mimic(Spy, GetPriceQueryHandler)
        controller = GetPriceController(handler)
        url_path = "/prices?type=night"

        with app.test_request_context(path=url_path):
            controller.get_price()

        expect(handler.execute).to(have_been_called)
