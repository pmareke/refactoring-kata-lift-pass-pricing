from dataclasses import dataclass

from src.domain.lift.lift import Lift
from src.domain.lift.lifts_repository import LiftsRepository
from src.domain.query import QueryHandler, Query


@dataclass
class GetLiftPricesQuery(Query):
    lifts: list[Lift]


class GetLiftPricesQueryHandler(QueryHandler):
    def __init__(self, lifts_repository: LiftsRepository) -> None:
        self.lifts_repository = lifts_repository

    def execute(self, query: GetLiftPricesQuery) -> list:
        costs = []
        for lift in query.lifts:
            cost = lift.calculate_cost(self.lifts_repository)
            result = {"type": lift.type.value, "cost": cost}
            if lift.date:
                result["date"] = lift.date_iso_format()
            if lift.age:
                result["age"] = lift.age
            costs.append(result)
        return costs
