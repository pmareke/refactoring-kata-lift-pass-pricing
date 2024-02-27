from flask import request

from src.domain.lift import Lift, LyftType
from src.domain.query import QueryHandler
from src.use_cases.queries.get_lift_price_query import GetLiftPriceQuery


class GetLiftPriceController:
    def __init__(self, query_handler: QueryHandler) -> None:
        self.query_handler = query_handler

    def get_lift_price(self) -> dict:
        lift_type = request.args["type"]
        age = request.args.get("age", type=int)
        date = request.args.get("date")
        lift = Lift(LyftType(lift_type), age, date)
        query = GetLiftPriceQuery(lift)

        cost = self.query_handler.execute(query)
        return {"cost": cost}
