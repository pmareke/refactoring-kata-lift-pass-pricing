from datetime import datetime

from flask import request

from src.domain.lift.lift import Lift
from src.domain.lift.lift_date import LyftDate
from src.domain.lift.lift_factory import LiftFactory
from src.domain.lift.lift_type import LyftType
from src.domain.query import QueryHandler
from src.use_cases.queries.get_lift_prices_query import GetLiftPricesQuery


class GetLiftPricesController:
    def __init__(self, query_handler: QueryHandler) -> None:
        self.query_handler = query_handler

    def get_lift_prices(self) -> list:
        lift_json = request.json
        if not lift_json:
            return []

        lifts = self._generate_lifts(lift_json)
        query = GetLiftPricesQuery(lifts)
        return self.query_handler.execute(query)

    def _generate_lifts(self, lift_json: dict) -> list[Lift]:
        lifts = []
        for lift in lift_json:
            lift_type = LyftType(lift["type"])
            age = lift.get("age")
            lift_date = self._get_lyft_date(lift)
            lift = LiftFactory.make(lift_type, age, lift_date)
            lifts.append(lift)
        return lifts

    @staticmethod
    def _get_lyft_date(lift: dict) -> LyftDate | None:
        if not lift.get("date"):
            return None

        return LyftDate(datetime.fromisoformat(lift["date"]))
