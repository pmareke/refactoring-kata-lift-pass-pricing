from doublex import Spy
from doublex_expects import have_been_called_with
from expects import expect

from src.domain.lift.lift_type import LyftType
from src.infrastructure.sql_lifts_repository import SqlLiftsRepository


class TestSqlLiftsRepositoryIntegration:
    def test_update_prices(self) -> None:
        lift_type = LyftType.NIGHT
        cost = 100
        cursor = Spy()
        lifts_repository = SqlLiftsRepository(cursor)

        lifts_repository.add_price(lift_type, cost)

        expect(cursor.execute).to(
            have_been_called_with(
                "INSERT INTO `base_price` (type, cost) VALUES (?, ?) ON DUPLICATE KEY UPDATE cost = ?",
                (lift_type.value, cost, cost),
            )
        )
