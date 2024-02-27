from expects import expect, equal

from src.infrastructure.sql_trips_repository import SqlTripsRepository


class TestSqlTripsRepositoryIntegration:
    def test_get_night_price(self) -> None:
        trips_repository = SqlTripsRepository()

        night_price = trips_repository.get_price("night")

        expect(night_price).to(equal(19))

    def test_get_1jour_price(self) -> None:
        trips_repository = SqlTripsRepository()

        night_price = trips_repository.get_price("1jour")

        expect(night_price).to(equal(35))
