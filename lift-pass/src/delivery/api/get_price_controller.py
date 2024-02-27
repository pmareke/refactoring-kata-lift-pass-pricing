import math

from flask import request
from datetime import datetime

from pymysql.cursors import Cursor


class GetPriceController:
    def __init__(self, cursor: Cursor) -> None:
        self.cursor = cursor

    def get_price(self):
        response = {"cost": 0}
        trip_type = request.args["type"]
        row = self._fetch_one_trip(trip_type)
        result = {"cost": row[0]}

        if "age" in request.args and request.args.get("age", type=int) < 6:
            response["cost"] = 0
            return response

        if trip_type == "night":
            self._calculate_cost_for_night(response, result)
        else:
            self._calculate_cost_for_non_nights(response, result)
        return response

    def _fetch_one_trip(self, trip_type: str):
        self.cursor.execute(f"SELECT cost FROM base_price WHERE type = ? ", trip_type)
        return self.cursor.fetchone()

    @staticmethod
    def _calculate_cost_for_night(response: dict, result: dict) -> None:
        if "age" in request.args and request.args.get("age", type=int) >= 6:
            if request.args.get("age", type=int) > 64:
                response["cost"] = math.ceil(result["cost"] * 0.4)
            else:
                response.update(result)
        else:
            response["cost"] = 0

    def _calculate_cost_for_non_nights(self, response: dict, result: dict):
        self.cursor.execute("SELECT * FROM holidays")
        is_holiday = False
        reduction = 0
        for row in self.cursor.fetchall():
            holiday = row[0]
            if "date" in request.args:
                d = datetime.fromisoformat(request.args["date"])
                if (
                    d.year == holiday.year
                    and d.month == holiday.month
                    and holiday.day == d.day
                ):
                    is_holiday = True
        if (
            not is_holiday
            and "date" in request.args
            and datetime.fromisoformat(request.args["date"]).weekday() == 0
        ):
            reduction = 35
        # TODO: apply reduction for others
        if "age" in request.args and request.args.get("age", type=int) < 15:
            response["cost"] = math.ceil(result["cost"] * 0.7)
        else:
            if "age" not in request.args:
                cost = result["cost"] * (1 - reduction / 100)
                response["cost"] = math.ceil(cost)
            else:
                if "age" in request.args and request.args.get("age", type=int) > 64:
                    cost = result["cost"] * 0.75 * (1 - reduction / 100)
                    response["cost"] = math.ceil(cost)
                elif "age" in request.args:
                    cost = result["cost"] * (1 - reduction / 100)
                    response["cost"] = math.ceil(cost)
