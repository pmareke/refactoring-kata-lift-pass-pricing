from doublex import Mimic, Spy, ANY_ARG
from doublex_expects import have_been_called
from expects import expect

from src.delivery.api.get_lift_price_controller import GetLiftPriceController
from src.domain.lift.lift_type import LyftType
from src.main import create_app
from src.use_cases.queries.get_lift_price_query import GetLiftPriceQueryHandler


class TestGetLiftPriceController:
    def test_get_lift_price(self) -> None:
        lift_type = LyftType.NIGHT
        with Mimic(Spy, GetLiftPriceQueryHandler) as handler:
            handler.execute(ANY_ARG).returns([{"cost": 10}])
        controller = GetLiftPriceController(handler)
        url_path = f"/prices?type={lift_type.value}"

        with create_app().test_request_context(path=url_path):
            controller.get_lift_price()

        expect(handler.execute).to(have_been_called)
