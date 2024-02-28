from doublex import ANY_ARG, Stub
from expects import expect, raise_error

from src.domain.lift.exceptions import SqlLiftsRepositoryException
from src.infrastructure.sql_lifts_repository import SqlLiftsRepositoryFactory


class TestSqlLiftsRepositoryFactory:
    def test_raise_exception_creating_the_connection(self) -> None:
        with Stub() as connector:
            connector.connect(ANY_ARG).raises(Exception)

        expect(lambda: SqlLiftsRepositoryFactory.make(connector)).to(
            raise_error(SqlLiftsRepositoryException)
        )
