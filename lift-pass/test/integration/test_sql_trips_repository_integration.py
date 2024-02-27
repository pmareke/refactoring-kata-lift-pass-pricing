import datetime

from expects import expect, equal

from src.infrastructure.sql_lifts_repository import SqlLiftsRepository


class TestSqlTripsRepositoryIntegration:
    def test_get_night_price(self) -> None:
        trips_repository = SqlLiftsRepository()

        night_price = trips_repository.get_price_for_lift("night")

        expect(night_price).to(equal(19))

    def test_get_1jour_price(self) -> None:
        trips_repository = SqlLiftsRepository()

        night_price = trips_repository.get_price_for_lift("1jour")

        expect(night_price).to(equal(35))

    def test_find_all_holidays(self) -> None:
        trips_repository = SqlLiftsRepository()

        holidays = trips_repository.find_all_holidays()

        expect(holidays).to(
            equal(
                [
                    (datetime.date(2019, 2, 18), "winter"),
                    (datetime.date(2019, 2, 25), "winter"),
                    (datetime.date(2019, 3, 4), "winter"),
                ]
            )
        )
