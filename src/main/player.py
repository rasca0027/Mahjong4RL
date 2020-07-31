from enum import Enum, unique

from .utils import get_values, get_name


@unique
class Position(Enum):
    TON = 0
    NAN = 1
    SHAA = 2
    PEI = 3


class Player:
    def __init__(self, name, seating_position):
        self.name = name
        self.seating_position = seating_position
        self.points = 25_000
        self.is_riichi = False

    def __str__(self):
        return (
            f"Player: { self.name }, Seating Position: "
            f"{ get_name(Position, self.seating_position) }"
        )

    @property
    def seating_position(self):
        return self._seating_position

    @seating_position.setter
    def seating_position(self, value):
        if not 0 <= value < 4:
            raise ValueError(
                f"Seating Position should be in: "
                f"{ get_values(Position) }")
        self._seating_position = value
