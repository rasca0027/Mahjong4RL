from enum import Enum, unique
from typing import List, DefaultDict
from collections import defaultdict

from .utils import get_values, get_name
from .mahjong import Huro, Tile


@unique
class Position(Enum):
    TON = 0
    NAN = 1
    SHAA = 2
    PEI = 3


class Player:
    def __init__(self, name, seating_position):
        self.name: str = name
        self.seating_position = seating_position
        self.points: int = 25_000
        self.is_riichi: bool = False
        self.hand: DefaultDict[int] = defaultdict(int)
        self.kabe: List[Huro] = []  # 副露/鳴き
        self.kawa: List[Tile] = []  # 河 is formed by the discarded tiles.

    def __str__(self):
        return (
            f"Player: { self.name }, Seating Position: "
            f"{ get_name(Position, self.seating_position) }"
        )

    @property
    def seating_position(self):
        return self._seating_position

    @seating_position.setter
    def seating_position(self, value: Position):
        if not 0 <= value < 4:
            raise ValueError(
                f"Seating Position should be in: "
                f"{ get_values(Position) }")
        self._seating_position = value
