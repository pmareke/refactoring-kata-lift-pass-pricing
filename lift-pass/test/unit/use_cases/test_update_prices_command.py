from doublex import Spy
from expects import expect

from src.use_cases.update_prices_command import UpdatePricesCommand, UpdatePricesCommandHandler


class TestUpdatePricesCommandHandler:
    def test_execute(self):
        trip_type = "night"
        cost = 100
        update_prices_command = UpdatePricesCommand(cost, trip_type)
        cursor = Spy()
        update_prices_command_handler = UpdatePricesCommandHandler(cursor)

        update_prices_command_handler.execute(update_prices_command)

        expect(cursor.execute).to.have.been.called_with(
            "INSERT INTO `base_price` (type, cost) VALUES (?, ?) ON DUPLICATE KEY UPDATE cost = ?",
            (trip_type, cost, cost),
        )


