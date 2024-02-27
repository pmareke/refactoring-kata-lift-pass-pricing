import math

from flask import Flask
from flask import request
from datetime import datetime

from pymysql import Connection

from src.db import create_lift_pass_db_connection

app = Flask("lift-pass-pricing")

connection_options = {
    "host": "localhost",
    "user": "root",
    "database": "lift_pass",
    "password": "mysql",
}

connection = create_lift_pass_db_connection(connection_options)


@app.put("/prices")
def update_prices():
    lift_pass_cost = request.args["cost"]
    lift_pass_type = request.args["type"]
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO `base_price` (type, cost) VALUES (?, ?) "
        + "ON DUPLICATE KEY UPDATE cost = ?",
        (lift_pass_type, lift_pass_cost, lift_pass_cost),
    )
    return {}


@app.get("/prices")
def get_price():
    return _get_price(connection)


def _calculate_cost_for_night(response: dict, result: dict) -> None:
    if "age" in request.args and request.args.get("age", type=int) >= 6:
        if request.args.get("age", type=int) > 64:
            response["cost"] = math.ceil(result["cost"] * 0.4)
        else:
            response.update(result)
    else:
        response["cost"] = 0


def _fetch_one_trip(conn: Connection, trip_type: str):
    cursor = conn.cursor()
    cursor.execute(f"SELECT cost FROM base_price WHERE type = ? ", trip_type)
    return cursor.fetchone()


def _get_price(conn: Connection) -> dict:
    res = {}
    trip_type = request.args["type"]
    row = _fetch_one_trip(conn, trip_type)
    result = {"cost": row[0]}

    if "age" in request.args and request.args.get("age", type=int) < 6:
        res["cost"] = 0
        return res

    if trip_type == "night":
        _calculate_cost_for_night(res, result)
    else:
        _calculate_cost_for_non_nights(conn, res, result)
    return res


def _calculate_cost_for_non_nights(conn: Connection, response: dict, result: dict):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM holidays")
    is_holiday = False
    reduction = 0
    for row in cursor.fetchall():
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


if __name__ == "__main__":
    app.run(port=3005)
