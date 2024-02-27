from dataclasses import dataclass

from src.domain.command import Command, CommandHandler
from src.domain.lifts_repository import LiftsRepository


@dataclass
class UpdateLiftsPricesCommand(Command):
    cost: int
    trip_type: str


class UpdateLiftsPricesCommandHandler(CommandHandler):
    def __init__(self, lifts_repository: LiftsRepository) -> None:
        self.lifts_repository = lifts_repository

    def execute(self, command: UpdateLiftsPricesCommand) -> None:
        self.lifts_repository.add_price(command.trip_type, command.cost)
