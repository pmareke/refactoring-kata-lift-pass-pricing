from expects import expect, equal

from src.domain.lift.lift_type import LyftType
from src.main import create_app


class TestGetLiftPricesAcceptance:
    def setup_method(self) -> None:
        self.client = create_app().test_client()

    def test_get_empty(self) -> None:
        response = self.client.post("/prices", json=[])

        expect(response.json).to(equal([]))

    def test_get_prices_with_type(self) -> None:
        lyft_type_jour_value = LyftType.JOUR.value
        lyft_type_night_value = LyftType.NIGHT.value
        payload = [
            {"type": lyft_type_jour_value},
            {"type": lyft_type_night_value},
        ]
        response = self.client.post("/prices", json=payload)

        expect(response.json).to(
            equal(
                [
                    {"cost": 35, "type": lyft_type_jour_value},
                    {"cost": 0, "type": lyft_type_night_value},
                ]
            )
        )

    def test_get_prices_with_age(self) -> None:
        lyft_type_jour_value = LyftType.JOUR.value
        lyft_type_night_value = LyftType.NIGHT.value
        age = 18
        other_age = 50
        payload = [
            {"type": lyft_type_jour_value, "age": age},
            {"type": lyft_type_night_value, "age": other_age},
        ]
        response = self.client.post("/prices", json=payload)

        expect(response.json).to(
            equal(
                [
                    {"cost": 35, "type": lyft_type_jour_value, "age": age},
                    {"cost": 19, "type": lyft_type_night_value, "age": other_age},
                ]
            )
        )

    def test_get_prices_with_date(self) -> None:
        lyft_type_jour_value = LyftType.JOUR.value
        lyft_type_night_value = LyftType.NIGHT.value
        date = "2021-01-01"
        payload = [
            {"type": lyft_type_jour_value, "date": date},
            {"type": lyft_type_night_value, "date": date},
        ]
        response = self.client.post("/prices", json=payload)

        expect(response.json).to(
            equal(
                [
                    {"cost": 35, "type": lyft_type_jour_value, "date": date},
                    {"cost": 0, "type": lyft_type_night_value, "date": date},
                ]
            )
        )
