from expects import expect, be_an

from src.domain.lift.jour_lift import JourLift
from src.domain.lift.lift_factory import LiftFactory
from src.domain.lift.lift_type import LyftType
from src.domain.lift.night_lift import NightLift


class TestLiftFactory:
    def test_create_night_lift(self) -> None:
        lift = LiftFactory.make(LyftType.NIGHT)

        expect(lift).to(be_an(NightLift))

    def test_create_jour_lift(self) -> None:
        lift = LiftFactory.make(LyftType.JOUR)

        expect(lift).to(be_an(JourLift))
