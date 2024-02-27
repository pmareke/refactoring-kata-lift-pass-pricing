from dataclasses import dataclass
from datetime import datetime


@dataclass
class LyftDate:
    date: datetime

    def is_monday(self) -> bool:
        return self.date.weekday() == 0
