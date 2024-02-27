from pymysql import Connection

from src.domain.lifts_repository import LiftsRepository


class SqlLiftsRepository(LiftsRepository):
    def __init__(self) -> None:
        connection = self._create_lift_pass_db_connection()
        self.cursor = connection.cursor()

    def get_price_for_lift(self, trip_type: str) -> int:
        self.cursor.execute(f"SELECT cost FROM base_price WHERE type = ? ", trip_type)
        return int(self.cursor.fetchone()[0])

    def find_all_holidays(self) -> list:
        self.cursor.execute("SELECT * FROM holidays")
        return [pair for pair in self.cursor.fetchall()]

    def add_price(self, trip_type: str, cost: int) -> None:
        self.cursor.execute(
            "INSERT INTO `base_price` (type, cost) VALUES (?, ?) ON DUPLICATE KEY UPDATE cost = ?",
            (trip_type, cost, cost),
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
