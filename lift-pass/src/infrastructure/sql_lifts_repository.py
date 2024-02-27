from pymysql import Connection

from src.domain.lift import LyftDate, LyftType
from src.domain.lifts_repository import LiftsRepository


class SqlLiftsRepository(LiftsRepository):

    def __init__(self) -> None:
        connection = self._create_lift_pass_db_connection()
        self.cursor = connection.cursor()

    def get_price_for_lift(self, lift_type: LyftType) -> int:
        self.cursor.execute(f"SELECT cost FROM base_price WHERE type = ? ", lift_type.value)
        return int(self.cursor.fetchone()[0])

    def is_holiday(self, lift_date: LyftDate | None) -> bool:
        if lift_date is None:
            return False
        holiday = self.cursor.execute(
            f"SELECT * FROM holidays WHERE holiday = ? ", lift_date.date.strftime("%Y-%m-%d")
        )
        return bool(holiday > 0)

    def add_price(self, lift_type: LyftType, cost: int) -> None:
        self.cursor.execute(
            "INSERT INTO `base_price` (type, cost) VALUES (?, ?) ON DUPLICATE KEY UPDATE cost = ?",
            (lift_type.value, cost, cost),
        )

    def _create_lift_pass_db_connection(self) -> Connection:
        try:
            connection = self._try_to_connect_with_pymysql()
            if connection is not None:
                return connection
        except Exception:
            print(f"unable to connect to db with {self._try_to_connect_with_pymysql}")

    def _try_to_connect_with_pymysql(self) -> Connection:
        import pymysql.cursors

        class PyMySQLCursorWrapper(pymysql.cursors.Cursor):
            """
            The pymysql.cursors.Cursor class very nearly works the same as the odbc equivalent. Unfortunately it doesn't
            understand the '?' in a SQL statement as an argument placeholder, and instead uses '%s'. This wrapper fixes that.
            """

            def mogrify(self, query: str, args: object = ...) -> str:
                query = query.replace("?", "%s")
                return str(super().mogrify(query, args))

        return pymysql.connect(
            host="localhost",
            user="root",
            password="mysql",
            database="lift_pass",
            cursorclass=PyMySQLCursorWrapper,
        )
