from enum import Enum, unique
from collections import OrderedDict
import numpy as np

from .mahjong import Suit, Jihai
from .utils import get_values, get_name


@unique
class Position(Enum):
    TON = 0
    NAN = 1
    SHAA = 2
    PEI = 3


class OrderedMJList(list):
    def __init__(self, ls=[]):
        super(OrderedMJList, self).__init__(ls)

    def ordered_tiles(self):
        return sorted(self, key=lambda tile: (tile.suit, tile.rank))

    def honor_tiles(self):
        '''
        http://arcturus.su/wiki/Mahjong_equipment#Japanese_tiles
        '''
        return [tile for tile in self if tile.suit == Suit.JIHAI.value]

    def manzu_tiles(self):
        return [tile for tile in self if tile.suit == Suit.MANZU.value]

    def souzu_tiles(self):
        return [tile for tile in self if tile.suit == Suit.SOUZU.value]

    def pinzu_tiles(self):
        return [tile for tile in self if tile.suit == Suit.PINZU.value]


class OrderedMJDict:
    def __init__(self):
        self.tiles = {Suit.JIHAI.value: dict.fromkeys(range(len(Jihai)),0),
                      Suit.MANZU.value: dict.fromkeys(range(1, 10),0),
                      Suit.SOUZU.value: dict.fromkeys(range(1, 10),0),
                      Suit.PINZU.value: dict.fromkeys(range(1, 10),0)
                      }

    #  usage: 
    #  Player.hand = OrderedMJDict()
    #  new_tile = Tile(2,1)
    #  Player.hand.tiles[new_tile.suit][new_tile.rank] += 1


class MJarray(np.ndarray):
    pass


class Player:
    def __init__(self, name, seating_position):
        self.name = name
        self.seating_position = seating_position
        self.points = 25_000
        self.is_riichi = False
        self.hand = OrderedMJList() # 手牌
        self.fuuro = OrderedMJList() # 副露/鳴き
        self.kawa = OrderedMJList() # 河 is formed by the discarded tiles.


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
