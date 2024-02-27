from dataclasses import dataclass

from src.domain.trips_repository import TripsRepository


@dataclass
class UpdatePricesCommand:
    cost: int
    trip_type: str


class UpdatePricesCommandHandler:
    def __init__(self, trips_repository: TripsRepository) -> None:
        self.trips_repository = trips_repository

    def execute(self, command: UpdatePricesCommand) -> None:
        self.trips_repository.add_price(command.trip_type, command.cost)
