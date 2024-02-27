import pytest
from doublex import Mimic, Spy
from expects import expect, be_true
from pymysql.cursors import Cursor

from src.delivery.api.get_price_controller import GetPriceController
from src.prices import app


@pytest.mark.skip(reason="Not implemented yet")
class TestGetPriceController:
    def test_get_price(self) -> None:
        with Mimic(Spy, Cursor) as cursor:
            pass
        controller = GetPriceController(cursor)
        url_path = "/prices?type=night"

        with app.test_request_context(path=url_path):
            controller.get_price()

        expect(True).to(be_true)

