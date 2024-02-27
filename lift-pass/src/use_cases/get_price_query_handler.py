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
        row = self._fetch_one_trip(query.trip_type)
        result = {"cost": row[0]}

        if query.age and query.age < 6:
            return {"cost": 0}

        if query.trip_type == "night":
            return self._calculate_cost_for_night(query, result)

        return self._calculate_cost_for_non_nights(query, result)

    def _fetch_one_trip(self, trip_type: str):
        self.cursor.execute(f"SELECT cost FROM base_price WHERE type = ? ", trip_type)
        return self.cursor.fetchone()

    @staticmethod
    def _calculate_cost_for_night(query: GetPriceQuery, result: dict) -> dict:
        if not query.age:
            return {"cost": 0}
        if 6 < query.age and query.age > 64:
            return {"cost": math.ceil(result["cost"] * 0.4)}
        return result

    def _calculate_cost_for_non_nights(
        self, query: GetPriceQuery, result: dict
    ) -> dict:
        response = {"cost": 0}
        is_holiday = False
        reduction = 0
        self.cursor.execute("SELECT * FROM holidays")
        holidays = self.cursor.fetchall()
        for holiday in holidays:
            holiday = holiday[0]
            if not query.date:
                continue

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
            return {"cost": math.ceil(result["cost"] * 0.7)}

        if not query.age:
            cost = result["cost"] * (1 - reduction / 100)
            return {"cost": math.ceil(cost)}

        if query.age > 64:
            cost = result["cost"] * 0.75 * (1 - reduction / 100)
            return {"cost": math.ceil(cost)}

        cost = result["cost"] * (1 - reduction / 100)
        response["cost"] = math.ceil(cost)
        return response
