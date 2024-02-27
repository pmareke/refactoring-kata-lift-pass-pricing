from flask import request
from pymysql.cursors import Cursor

from src.use_cases.update_prices_command import UpdatePricesCommand, UpdatePricesCommandHandler


class UpdatePricesController:
    def __init__(self, command_handler: UpdatePricesCommandHandler) -> None:
        self.command_handler = command_handler

    def update_prices(self) -> None:
        lift_pass_cost = request.args["cost"]
        lift_pass_type = request.args["type"]
        command = UpdatePricesCommand(lift_pass_cost, lift_pass_type)

        self.command_handler.execute(command)
