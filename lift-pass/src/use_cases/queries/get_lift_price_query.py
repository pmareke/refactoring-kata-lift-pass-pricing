from dataclasses import dataclass

from src.domain.lift.lift import Lift
from src.domain.lift.lifts_repository import LiftsRepository
from src.domain.query import QueryHandler, Query


@dataclass
class GetLiftPriceQuery(Query):
    lift: Lift


class GetLiftPriceQueryHandler(QueryHandler):
    def __init__(self, lifts_repository: LiftsRepository) -> None:
        self.lifts_repository = lifts_repository

    def execute(self, query: GetLiftPriceQuery) -> list:
        cost = query.lift.calculate_cost(self.lifts_repository)
        return [{"cost": cost}]
