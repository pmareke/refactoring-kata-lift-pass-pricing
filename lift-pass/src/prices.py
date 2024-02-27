from flask import Flask

from src.db import create_lift_pass_db_connection
from src.delivery.api.get_price_controller import GetPriceController
from src.delivery.api.update_prices_controller import UpdatePricesController
from src.use_cases.get_price_query_handler import GetPriceQueryHandler
from src.use_cases.update_prices_command import UpdatePricesCommandHandler

app = Flask("lift-pass-pricing")
connection = create_lift_pass_db_connection()
cursor = connection.cursor()

get_price_query_handler = GetPriceQueryHandler(cursor)
get_price_controller = GetPriceController(get_price_query_handler)
app.route("/prices", methods=["GET"])(get_price_controller.get_price)

update_prices_command_handler = UpdatePricesCommandHandler(cursor)
update_prices_controller = UpdatePricesController(update_prices_command_handler)
app.route("/prices", methods=["PUT"])(update_prices_controller.update_prices)

if __name__ == "__main__":
    app.run(port=3005)
