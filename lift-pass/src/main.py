from flask import Flask

from src.delivery.api.get_price_controller import GetPriceController
from src.delivery.api.update_prices_controller import UpdatePricesController
from src.infrastructure.sql_trips_repository import SqlTripsRepository
from src.use_cases.queries.get_price_query import GetPriceQueryHandler
from src.use_cases.commands.update_prices_command import UpdatePricesCommandHandler

app = Flask("lift-pass-pricing")
trips_repository = SqlTripsRepository()
get_price_query_handler = GetPriceQueryHandler(trips_repository)
get_price_controller = GetPriceController(get_price_query_handler)
app.route("/prices", methods=["GET"])(get_price_controller.get_price)

update_prices_command_handler = UpdatePricesCommandHandler(trips_repository)
update_prices_controller = UpdatePricesController(update_prices_command_handler)
app.route("/prices", methods=["PUT"])(update_prices_controller.update_prices)

if __name__ == "__main__":
    app.run(port=3005)
