from dataclasses import dataclass

from src.domain.lift import Lift
from src.domain.query import QueryHandler, Query
from src.domain.lifts_repository import LiftsRepository


@dataclass
class GetLiftPriceQuery(Query):
    lift: Lift


class GetLiftPriceQueryHandler(QueryHandler):
    def __init__(self, lifts_repository: LiftsRepository) -> None:
        self.lifts_repository = lifts_repository

    def execute(self, query: GetLiftPriceQuery) -> int:
        return query.lift.calculate_cost(self.lifts_repository)
