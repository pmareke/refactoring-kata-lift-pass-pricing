import math

from datetime import datetime
from dataclasses import dataclass
from pymysql.cursors import Cursor


@dataclass
class GetPriceQuery:
    trip_type: str
    age: int | None = None
    date: str | None = None


class GetPriceQueryHandler:
    def __init__(self, cursor: Cursor) -> None:
        self.cursor = cursor

    def execute(self, query: GetPriceQuery) -> dict:
        response = {"cost": 0}
        row = self._fetch_one_trip(query.trip_type)
        result = {"cost": row[0]}

        if query.age and query.age < 6:
            response["cost"] = 0
            return response

        if query.trip_type == "night":
            self._calculate_cost_for_night(query, response, result)
        else:
            self._calculate_cost_for_non_nights(query, response, result)
        return response

    def _fetch_one_trip(self, trip_type: str):
        self.cursor.execute(f"SELECT cost FROM base_price WHERE type = ? ", trip_type)
        return self.cursor.fetchone()

    @staticmethod
    def _calculate_cost_for_night(
        query: GetPriceQuery, response: dict, result: dict
    ) -> None:
        if query.age and query.age >= 6:
            if query.age > 64:
                response["cost"] = math.ceil(result["cost"] * 0.4)
            else:
                response.update(result)
        else:
            response["cost"] = 0

    def _calculate_cost_for_non_nights(
        self, query: GetPriceQuery, response: dict, result: dict
    ):
        self.cursor.execute("SELECT * FROM holidays")
        is_holiday = False
        reduction = 0
        for row in self.cursor.fetchall():
            holiday = row[0]
            if query.date:
                d = datetime.fromisoformat(query.date)
                if (
                    d.year == holiday.year
                    and d.month == holiday.month
                    and holiday.day == d.day
                ):
                    is_holiday = True
        if (
            not is_holiday
            and query.date
            and datetime.fromisoformat(query.date).weekday() == 0
        ):
            reduction = 35
        # TODO: apply reduction for others
        if query.age and query.age < 15:
            response["cost"] = math.ceil(result["cost"] * 0.7)
        else:
            if not query.age:
                cost = result["cost"] * (1 - reduction / 100)
                response["cost"] = math.ceil(cost)
            else:
                if query.age and query.age > 64:
                    cost = result["cost"] * 0.75 * (1 - reduction / 100)
                    response["cost"] = math.ceil(cost)
                elif query.age:
                    cost = result["cost"] * (1 - reduction / 100)
                    response["cost"] = math.ceil(cost)
