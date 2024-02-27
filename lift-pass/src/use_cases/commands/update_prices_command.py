from dataclasses import dataclass

from src.domain.command import Command, CommandHandler
from src.domain.trips_repository import TripsRepository


@dataclass
class UpdatePricesCommand(Command):
    cost: int
    trip_type: str


class UpdatePricesCommandHandler(CommandHandler):
    def __init__(self, trips_repository: TripsRepository) -> None:
        self.trips_repository = trips_repository

    def execute(self, command: UpdatePricesCommand) -> None:
        self.trips_repository.add_price(command.trip_type, command.cost)
