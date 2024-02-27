from dataclasses import dataclass

from pymysql.cursors import Cursor


@dataclass
class UpdatePricesCommand:
    cost: int
    trip_type: str


class UpdatePricesCommandHandler:
    def __init__(self, cursor: Cursor) -> None:
        self.cursor = cursor

    def execute(self, command: UpdatePricesCommand) -> None:
        self.cursor.execute(
            "INSERT INTO `base_price` (type, cost) VALUES (?, ?) ON DUPLICATE KEY UPDATE cost = ?",
            (command.trip_type, command.cost, command.cost),
        )
