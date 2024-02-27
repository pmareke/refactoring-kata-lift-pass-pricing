from doublex import Mimic, Spy
from doublex_expects import have_been_called_with
from expects import expect, be_true
from pymysql.cursors import Cursor

from src.delivery.api.update_prices_controller import UpdatePricesController
from src.prices import app


class TestUpdatePricesController:

    def test_update_prices(self) -> None:
        cursor = Mimic(Spy, Cursor)
        controller = UpdatePricesController(cursor)
        url_path = "/prices?cost=100&type=night"

        with app.test_request_context(path=url_path):
            controller.update_prices()

        expect(cursor.execute).to(have_been_called_with(
            "INSERT INTO `base_price` (type, cost) VALUES (?, ?) ON DUPLICATE KEY UPDATE cost = ?",
            ("night", "100", "100")
        ))

