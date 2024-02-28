from datetime import datetime

from flask import request

from src.domain.lift.lift import Lift
from src.domain.lift.lift_date import LyftDate
from src.domain.lift.lift_factory import LiftFactory
from src.domain.lift.lift_type import LyftType
from src.domain.query import QueryHandler
from src.use_cases.queries.get_lift_price_query import GetLiftPriceQuery


class GetLiftPriceController:
    def __init__(self, query_handler: QueryHandler) -> None:
        self.query_handler = query_handler

    def get_lift_price(self) -> dict:
        lift = self._generate_lift()
        query = GetLiftPriceQuery(lift)
        response: list[dict] = self.query_handler.execute(query)
        return response[0]

    def _generate_lift(self) -> Lift:
        lift_type = LyftType(request.args["type"])
        age = request.args.get("age", type=int)
        date = request.args.get("date")
        lift_date = self._get_lift_date(date)
        lift = LiftFactory.make(lift_type, age, lift_date)
        return lift

    @staticmethod
    def _get_lift_date(date: str | None) -> LyftDate | None:
        if not date:
            return None
        return LyftDate(datetime.fromisoformat(date))
