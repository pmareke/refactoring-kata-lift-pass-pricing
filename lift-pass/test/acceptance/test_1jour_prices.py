from expects import expect, equal

from src.domain.lift.lift_type import LyftType
from src.main import create_app


class Test1JourPricesAcceptance:
    def setup_method(self) -> None:
        self.client = create_app().test_client()

    def test_1jour_type(self) -> None:
        lift_type = LyftType.JOUR

        response = self.client.get(f"/prices?type={lift_type.value}")

        expect(response.json).to(equal({"cost": 35}))

    def test_people_under_6_not_pay(self) -> None:
        lift_type = LyftType.JOUR

        response = self.client.get(f"/prices?type={lift_type.value}&age=5")

        expect(response.json).to(equal({"cost": 0}))

    def test_1jour_type_with_age_bellow_15(self) -> None:
        lift_type = LyftType.JOUR

        response = self.client.get(f"/prices?type={lift_type.value}&age=14")

        expect(response.json).to(equal({"cost": 25}))

    def test_1jour_type_with_age_between_16_and_63(self) -> None:
        lift_type = LyftType.JOUR

        response = self.client.get(f"/prices?type={lift_type.value}&age=50")

        expect(response.json).to(equal({"cost": 35}))

    def test_1jour_type_with_age_above_64(self) -> None:
        lift_type = LyftType.JOUR

        response = self.client.get(f"/prices?type={lift_type.value}&age=65")

        expect(response.json).to(equal({"cost": 27}))

    def test_1jour_type_on_holidays(self) -> None:
        lift_type = LyftType.JOUR
        holiday_date = "2019-02-18"

        response = self.client.get(
            f"/prices?type={lift_type.value}&date={holiday_date}"
        )

        expect(response.json).to(equal({"cost": 35}))

    def test_1jour_type_not_on_holidays(self) -> None:
        lift_type = LyftType.JOUR
        non_holiday_date = "2024-02-26"

        response = self.client.get(
            f"/prices?type={lift_type.value}&date={non_holiday_date}"
        )

        expect(response.json).to(equal({"cost": 23}))
