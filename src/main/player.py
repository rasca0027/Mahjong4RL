from enum import Enum, unique
from typing import List

from .mahjong import Suit, Jihai
from .utils import get_values, get_name
from .mahjong import Huro


@unique
class Position(Enum):
    TON = 0
    NAN = 1
    SHAA = 2
    PEI = 3


class OrderedMJDict:
    '''Data type for storing Tile objects
    usage example: 
        Player.hand = OrderedMJDict()
        摸牌
        new_tile = Tile(Suit.SOUZU.value,1)
        Player.hand.tiles[new_tile.suit][new_tile.rank] += 1
        打牌
        discard_tile = Tile(Suit.SOUZU.value,2)
        Player.hand.tiles[discard_tile.suit][discard_tile.rank] -= 1
    '''
    def __init__(self):
        self.tiles = {Suit.JIHAI: dict.fromkeys(range(len(Jihai)),0),
                      Suit.MANZU: dict.fromkeys(range(1, 10),0),
                      Suit.SOUZU: dict.fromkeys(range(1, 10),0),
                      Suit.PINZU: dict.fromkeys(range(1, 10),0)
                      }


class Player:
    def __init__(self, name, seating_position):
        self.name: str = name
        self.seating_position = seating_position
        self.points: int = 25_000
        self.is_riichi: bool = False
        self.hand = OrderedMJList() # 手牌
        self.kabe: List[Huro] = [] # 副露/鳴き
        self.kawa: List[Tile] = [] # 河 is formed by the discarded tiles. 這個順序蠻重要的，也許用 list if Tile 就好？

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
