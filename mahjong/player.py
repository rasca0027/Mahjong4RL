from enum import Enum, unique
from typing import List, DefaultDict
from collections import defaultdict

from .utils import get_values, get_name
from .components import Huro, Tile, Action


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
        # TODO: Build Player's connection (socket)?

    def __str__(self):
        return (
            f"Player: { self.name }, Seating Position: "
            f"{ get_name(Position, self.seating_position) }"
        )

    def add_kawa(self, tile: Tile) -> None:
        if tile:
            self.kawa.append(tile)
        return

    @property
    def seating_position(self) -> int:
        return self._seating_position

    @seating_position.setter
    def seating_position(self, value: Position) -> None:
        if not 0 <= value < 4:
            raise ValueError(
                f"Seating Position should be in: "
                f"{ get_values(Position) }")
        self._seating_position = value

    def get_komicha(self) -> int:
        return (self.seating_position - 1) % 4

    def get_toimen(self) -> int:
        return (self.seating_position + 2) % 4

    def get_shimocha(self) -> int:
        return (self.seating_position + 1) % 4

    def action_with_discard_tile(self, tile: Tile, pos: int) -> None:
        """"Player has to select an action reacting to
          the discarded tile.
        Args:
          tile: discarded tile
          pos: the seating position of the person discarded the tile
        Returns:
          action: CHI/PON/DAMINKAN/RON
        """
        self.tmp_huro = None
        # TODO: connect player's input with the action
        return

    def action_with_new_tile(self, tile: Tile) -> None:
        self.tmp_huro = None
        # TODO: connect player's input with the action
        return

    def action_with_naki(self, action: Action) -> None:
        # add tmp_huro to kabe
        self.kabe.append(self.tmp_huro)
        self.tmp_huro = None
        return

    def discard_after_naki(self) -> Tile:
        return
