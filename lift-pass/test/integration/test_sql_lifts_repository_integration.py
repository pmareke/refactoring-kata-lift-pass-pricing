import datetime

from expects import expect, equal, be_true, be_false

from src.infrastructure.sql_lifts_repository import SqlLiftsRepository


class TestSqlLiftsRepositoryIntegration:
    def test_get_night_price(self) -> None:
        trips_repository = SqlLiftsRepository()

        night_price = trips_repository.get_price_for_lift("night")

        expect(night_price).to(equal(19))

    def test_get_1jour_price(self) -> None:
        trips_repository = SqlLiftsRepository()

        night_price = trips_repository.get_price_for_lift("1jour")

        expect(night_price).to(equal(35))

    def test_is_holiday(self) -> None:
        lifts_repository = SqlLiftsRepository()

        is_holiday = lifts_repository.is_holiday("2019-02-18")

        expect(is_holiday).to(be_true)

    def test_is_not_holiday(self) -> None:
        lifts_repository = SqlLiftsRepository()

        is_holiday = lifts_repository.is_holiday("2024-02-18")

        expect(is_holiday).to(be_false)
