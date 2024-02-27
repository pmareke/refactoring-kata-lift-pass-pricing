from expects import expect, equal

from src.domain.lift_type import LyftType
from src.main import create_app


class TestNightPricesAcceptance:
    def setup_method(self) -> None:
        self.client = create_app().test_client()

    def test_nights_are_free(self) -> None:
        lift_type = LyftType.NIGHT

        response = self.client.get(f"/prices?type={lift_type.value}")

        expect(response.json).to(equal({"cost": 0}))

    def test_people_under_6_not_pay(self) -> None:
        lift_type = LyftType.NIGHT

        response = self.client.get(f"/prices?type={lift_type.value}&age=5")

        expect(response.json).to(equal({"cost": 0}))

    def test_nights_with_age_above_6_has_not_discount(self) -> None:
        lift_type = LyftType.NIGHT

        response = self.client.get(f"/prices?type={lift_type.value}&age=40")

        expect(response.json).to(equal({"cost": 19}))

    def test_nights_with_age_above_64_has_40_percentage_discount(self) -> None:
        lift_type = LyftType.NIGHT

        response = self.client.get(f"/prices?type={lift_type.value}&age=65")

        expect(response.json).to(equal({"cost": 8}))
