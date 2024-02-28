import pymysql.cursors
from pymysql import Connection

from src.domain.lift.lift_date import LyftDate
from src.domain.lift.lift_type import LyftType
from src.domain.lift.lifts_repository import LiftsRepository
from src.infrastructure.sql_cursor_wrapper import PyMySQLCursorWrapper


class SqlLiftsRepository(LiftsRepository):

    def __init__(self) -> None:
        connection = self._create_connection()
        self.cursor = connection.cursor()

    def get_price_for_lift(self, lift_type: LyftType) -> int:
        self.cursor.execute(
            f"SELECT cost FROM base_price WHERE type = ? ", lift_type.value
        )
        return int(self.cursor.fetchone()[0])

    def is_holiday(self, lift_date: LyftDate) -> bool:
        holiday = self.cursor.execute(
            f"SELECT * FROM holidays WHERE holiday = ?  LIMIT 1",
            lift_date.date.strftime("%Y-%m-%d"),
        )
        return bool(holiday > 0)

    def add_price(self, lift_type: LyftType, cost: int) -> None:
        self.cursor.execute(
            "INSERT INTO `base_price` (type, cost) VALUES (?, ?) ON DUPLICATE KEY UPDATE cost = ?",
            (lift_type.value, cost, cost),
        )

    @staticmethod
    def _create_connection() -> Connection:
        try:
            return pymysql.connect(
                host="localhost",
                user="root",
                password="mysql",
                database="lift_pass",
                cursorclass=PyMySQLCursorWrapper,
            )
        except Exception as ex:
            print(f"unable to connect to db {ex}")
