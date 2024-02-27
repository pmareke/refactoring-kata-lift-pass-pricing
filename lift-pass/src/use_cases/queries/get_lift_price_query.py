import math

from datetime import datetime
from dataclasses import dataclass

from src.domain.lift import Lift, LyftType
from src.domain.query import QueryHandler, Query
from src.domain.lifts_repository import LiftsRepository


@dataclass
class GetLiftPriceQuery(Query):
    lift: Lift


class GetLiftPriceQueryHandler(QueryHandler):
    def __init__(self, lifts_repository: LiftsRepository) -> None:
        self.lifts_repository = lifts_repository

    def execute(self, query: GetLiftPriceQuery) -> dict:
        cost = self.lifts_repository.get_price_for_lift(query.lift.type.value)
        result = {"cost": cost}

        if query.lift.age and query.lift.age < 6:
            return {"cost": 0}

        if query.lift.type.is_night:
            return self._calculate_cost_for_one_lift_night(query, result)

        return self._calculate_cost_for_non_lift_nights(query, result)

    @staticmethod
    def _calculate_cost_for_one_lift_night(query: GetLiftPriceQuery, result: dict) -> dict:
        if not query.lift.age:
            return {"cost": 0}
        if 6 < query.lift.age and query.lift.age > 64:
            return {"cost": math.ceil(result["cost"] * 0.4)}
        return result

    def _calculate_cost_for_non_lift_nights(
        self, query: GetLiftPriceQuery, result: dict
    ) -> dict:
        response = {"cost": 0}
        is_holiday = False
        reduction = 0
        holidays = self.lifts_repository.find_all_holidays()
        for holiday in holidays:
            holiday = holiday[0]
            if not query.lift.date:
                continue

            lift_date = datetime.fromisoformat(query.lift.date)
            if (
                lift_date.year == holiday.year
                and lift_date.month == holiday.month
                and holiday.day == lift_date.day
            ):
                is_holiday = True

        if (
            not is_holiday
            and query.lift.date
            and datetime.fromisoformat(query.lift.date).weekday() == 0
        ):
            reduction = 35

        # TODO: apply reduction for others
        if query.lift.age and query.lift.age < 15:
            return {"cost": math.ceil(result["cost"] * 0.7)}

        if not query.lift.age:
            cost = result["cost"] * (1 - reduction / 100)
            return {"cost": math.ceil(cost)}

        if query.lift.age > 64:
            cost = result["cost"] * 0.75 * (1 - reduction / 100)
            return {"cost": math.ceil(cost)}

        cost = result["cost"] * (1 - reduction / 100)
        response["cost"] = math.ceil(cost)
        return response
