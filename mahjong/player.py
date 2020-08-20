from enum import Enum, unique
from typing import List, DefaultDict
from collections import defaultdict

from .utils import get_values, get_name
from .components import Huro, Tile, Action
from .naki_and_actions import (
    check_pon, check_daminkan, check_riichi, check_ron,
    check_chakan, check_ankan,
)


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
        self.tmp_huro: Huro = None

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

    def action_with_discard_tile(self, tile: Tile, pos: int):
        """"Player has to select an action reacting to
          the discarded tile.
        Args:
          tile: discarded tile
          pos: the seating position of the person discarded the tile
        Returns:
          action: CHI/PON/DAMINKAN/RON
        """
        self.tmp_huro = None
        # Check the tile with different situation
        # Check Ron -> receive player's action?
        # Check Daminkan
        # Check Pon
        # Check Chi
        # Ron: directly put the tile into hand
        return

    def action_with_new_tile(self, tile: Tile):
        self.tmp_huro = None
        # Check Tsumo
        # Check Riichi
        # Check Ankan
        # Check Chakan
        return

    def action_with_naki(self, action: Action):
        # add tmp_huro to kabe
        self.kabe.append(self.tmp_huro)
        self.tmp_huro = None
        return

    def discard_after_naki(self) -> Tile:
        return
