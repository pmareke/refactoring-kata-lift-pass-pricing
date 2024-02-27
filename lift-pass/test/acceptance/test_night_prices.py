from src.main import app
from expects import expect, equal


class TestNightPricesAcceptance:
    def setup_method(self) -> None:
        self.client = app.test_client()

    def test_nights_are_free(self) -> None:
        response = self.client.get("/prices", query_string={"type": "night"})

        expect(response.json).to(equal({"cost": 0}))

    def test_people_under_6_not_pay(self) -> None:
        response = self.client.get("/prices", query_string={"type": "night", "age": 5})

        expect(response.json).to(equal({"cost": 0}))

    def test_nights_with_age_above_6_has_not_discount(self) -> None:
        response = self.client.get("/prices", query_string={"type": "night", "age": 40})

        expect(response.json).to(equal({"cost": 19}))

    def test_nights_with_age_above_64_has_40_percentage_discount(self) -> None:
        response = self.client.get("/prices", query_string={"type": "night", "age": 65})

        expect(response.json).to(equal({"cost": 8}))
