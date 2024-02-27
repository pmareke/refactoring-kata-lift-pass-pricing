from flask import request
from pymysql import Connection
from pymysql.cursors import Cursor


class UpdatePricesController:
    def __init__(self, cursor: Cursor) -> None:
        self.cursor = cursor

    def update_prices(self) -> None:
        lift_pass_cost = request.args["cost"]
        lift_pass_type = request.args["type"]
        self.cursor.execute(
            "INSERT INTO `base_price` (type, cost) VALUES (?, ?) ON DUPLICATE KEY UPDATE cost = ?",
            (lift_pass_type, lift_pass_cost, lift_pass_cost),
        )
