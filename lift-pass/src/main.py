from flask import Flask

from src.delivery.api.get_lift_price_controller import GetLiftPriceController
from src.delivery.api.get_lift_prices_controller import GetLiftPricesController
from src.delivery.api.update_lifts_prices_controller import UpdateLiftsPricesController
from src.infrastructure.sql_lifts_repository import SqlLiftsRepositoryFactory
from src.use_cases.commands.update_lifts_prices_command import (
    UpdateLiftsPricesCommandHandler,
)
from src.use_cases.queries.get_lift_price_query import GetLiftPriceQueryHandler
from src.use_cases.queries.get_lift_prices_query import GetLiftPricesQueryHandler


def create_app() -> Flask:
    app = Flask("lift-pass-pricing")
    lifts_repository = SqlLiftsRepositoryFactory.make()

    get_lift_price_query_handler = GetLiftPriceQueryHandler(lifts_repository)
    get_lift_price_controller = GetLiftPriceController(get_lift_price_query_handler)
    app.route("/prices", methods=["GET"])(get_lift_price_controller.get_lift_price)

    get_lift_prices_query_handler = GetLiftPricesQueryHandler(lifts_repository)
    get_lift_prices_controller = GetLiftPricesController(get_lift_prices_query_handler)
    app.route("/prices", methods=["POST"])(get_lift_prices_controller.get_lift_prices)

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
