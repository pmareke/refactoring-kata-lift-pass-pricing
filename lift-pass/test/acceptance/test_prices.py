from src.prices import app

from expects import expect, equal


class TestPricesAcceptance:
    def setup_method(self) -> None:
        self.client = app.test_client()

    def test_1jour_type(self) -> None:
        response = self.client.get("/prices", query_string={"type": "1jour"})

        expect(response.json).to(equal({"cost": 35}))

    def test_1jour_type_with_age_above_64(self) -> None:
        response = self.client.get("/prices", query_string={"type": "1jour", "age": 65})

        expect(response.json).to(equal({"cost": 27}))

    def test_night_type_with_age_below_6(self):
        response = self.client.get("/prices", query_string={"type": "night", "age": 5})

        expect(response.json).to(equal({"cost": 0}))

    def test_night_type_with_age_above_6(self) -> None:
        response = self.client.get("/prices", query_string={"type": "night", "age": 40})

        expect(response.json).to(equal({"cost": 19}))

    def test_night_type_with_age_above_64(self) -> None:
        response = self.client.get("/prices", query_string={"type": "night", "age": 65})

        expect(response.json).to(equal({"cost": 8}))
