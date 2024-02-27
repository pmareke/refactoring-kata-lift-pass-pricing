from flask import request

from src.domain.command import CommandHandler
from src.domain.lift_type import LyftType
from src.use_cases.commands.update_lifts_prices_command import (
    UpdateLiftsPricesCommand,
)


class UpdateLiftsPricesController:
    def __init__(self, command_handler: CommandHandler) -> None:
        self.command_handler = command_handler

    def update_lifts_prices(self) -> None:
        lift_pass_cost = int(request.args["cost"])
        lift_pass_type = LyftType(request.args["type"])
        command = UpdateLiftsPricesCommand(lift_pass_cost, lift_pass_type)

        self.command_handler.execute(command)
