from flask import request

from src.domain.query import QueryHandler
from src.use_cases.queries.get_price_query import GetPriceQuery


class GetPriceController:
    def __init__(self, query_handler: QueryHandler) -> None:
        self.query_handler = query_handler

    def get_price(self) -> dict:
        trip_type = request.args["type"]
        age = request.args.get("age", type=int)
        date = request.args.get("date")
        query = GetPriceQuery(trip_type, age, date)

        return self.query_handler.execute(query)
