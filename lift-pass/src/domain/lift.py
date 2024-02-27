from dataclasses import dataclass
from enum import Enum


class LyftType(Enum):
    NIGHT = "night"
    JOUR = "1jour"

    @property
    def is_night(self) -> bool:
        return self == LyftType.NIGHT


@dataclass
class Lift:
    type: LyftType
    age: int | None = None
    date: str | None = None
