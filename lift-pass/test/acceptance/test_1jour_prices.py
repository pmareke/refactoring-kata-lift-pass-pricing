import pytest

from src.prices import app
from expects import expect, equal


class Test1JourPricesAcceptance:
    def setup_method(self) -> None:
        self.client = app.test_client()

    def test_1jour_type(self) -> None:
        response = self.client.get("/prices", query_string={"type": "1jour"})

        expect(response.json).to(equal({"cost": 35}))

    def test_people_under_6_not_pay(self) -> None:
        response = self.client.get("/prices", query_string={"type": "1jour", "age": 5})

        expect(response.json).to(equal({"cost": 0}))

    def test_1jour_type_with_age_bellow_15(self) -> None:
        response = self.client.get("/prices", query_string={"type": "1jour", "age": 14})

        expect(response.json).to(equal({"cost": 25}))

    def test_1jour_type_with_age_between_16_and_63(self) -> None:
        response = self.client.get("/prices", query_string={"type": "1jour", "age": 50})

        expect(response.json).to(equal({"cost": 35}))

    def test_1jour_type_with_age_above_64(self) -> None:
        response = self.client.get("/prices", query_string={"type": "1jour", "age": 65})

        expect(response.json).to(equal({"cost": 27}))

    def test_1jour_type_on_holidays(self) -> None:
        date = "2019-02-18"
        response = self.client.get(
            "/prices", query_string={"type": "1jour", "date": date}
        )

        expect(response.json).to(equal({"cost": 35}))

    def test_1jour_type_not_on_holidays(self) -> None:
        date = "2024-02-26"
        response = self.client.get(
            "/prices", query_string={"type": "1jour", "date": date}
        )

        expect(response.json).to(equal({"cost": 23}))
