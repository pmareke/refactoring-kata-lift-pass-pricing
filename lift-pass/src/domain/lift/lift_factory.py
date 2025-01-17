from src.domain.lift.jour_lift import JourLift
from src.domain.lift.lift import Lift
from src.domain.lift.lift_date import LyftDate
from src.domain.lift.lift_type import LyftType
from src.domain.lift.night_lift import NightLift


class LiftFactory:
    @staticmethod
    def make(
        lift_type: LyftType, age: int | None = None, date: LyftDate | None = None
    ) -> Lift:
        if lift_type.is_night:
            return NightLift(age=age, date=date)
        return JourLift(age=age, date=date)
