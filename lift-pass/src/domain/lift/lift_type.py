from enum import Enum


class LyftType(Enum):
    NIGHT = "night"
    JOUR = "1jour"

    @property
    def is_night(self) -> bool:
        return self == LyftType.NIGHT
