from flask import request

from src.domain.command import CommandHandler
from src.use_cases.commands.update_prices_command import (
    UpdatePricesCommand,
)


class UpdatePricesController:
    def __init__(self, command_handler: CommandHandler) -> None:
        self.command_handler = command_handler

    def update_prices(self) -> None:
        lift_pass_cost = int(request.args["cost"])
        lift_pass_type = request.args["type"]
        command = UpdatePricesCommand(lift_pass_cost, lift_pass_type)

        self.command_handler.execute(command)
