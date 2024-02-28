from src.domain.lift.jour_lift import JourLift
from src.domain.lift.lift import Lift
from src.domain.lift.lift_type import LyftType
from src.domain.lift.night_lift import NightLift


class LiftFactory:
    @staticmethod
    def make(lift_type: LyftType, age: int | None = None, date: str | None = None) -> Lift:
        if lift_type.is_night:
            return NightLift(age, date)
        return JourLift(age, date)
