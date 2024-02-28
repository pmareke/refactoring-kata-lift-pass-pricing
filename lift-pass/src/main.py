from flask import Flask

from src.delivery.api.get_lift_price_controller import GetLiftPriceController
from src.delivery.api.update_lifts_prices_controller import UpdateLiftsPricesController
from src.infrastructure.sql_lifts_repository import SqlLiftsRepository
from src.use_cases.commands.update_lifts_prices_command import (
    UpdateLiftsPricesCommandHandler,
)
from src.use_cases.queries.get_lift_price_query import GetLiftPriceQueryHandler


def create_app() -> Flask:
    app = Flask("lift-pass-pricing")
    lifts_repository = SqlLiftsRepository()

    get_price_lift_query_handler = GetLiftPriceQueryHandler(lifts_repository)
    get_price_lift_controller = GetLiftPriceController(get_price_lift_query_handler)
    app.route("/prices", methods=["GET"])(get_price_lift_controller.get_lift_price)

    update_lifts_prices_command_handler = UpdateLiftsPricesCommandHandler(
        lifts_repository
    )
    update_lifts_prices_controller = UpdateLiftsPricesController(
        update_lifts_prices_command_handler
    )
    app.route("/prices", methods=["PUT"])(update_lifts_prices_controller.update_lifts_prices)  # type: ignore

    return app


if __name__ == "__main__":
    port = 3005
    create_app().run(port=port)
