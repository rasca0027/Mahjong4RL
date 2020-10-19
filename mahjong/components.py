import itertools
import random
from typing import Tuple, List
from enum import Enum, unique

from .utils import get_values, get_name


@unique
class Suit(Enum):
    JIHAI = 0
    MANZU = 1
    SOUZU = 2
    PINZU = 3


@unique
class Jihai(Enum):
    HAKU = 1
    HATSU = 2
    CHUN = 3
    TON = 4
    NAN = 5
    SHAA = 6
    PEI = 7


@unique
class Naki(Enum):
    NONE = 0
    CHII = 1
    PON = 2
    DAMINKAN = 3
    CHAKAN = 4
    ANKAN = 5


@unique
class Action(Enum):
    NOACT = 0
    NAKI = 1
    RIICHI = 2
    RON = 3
    TSUMO = 4


class Tile:
    def __init__(self, suit: int, rank: int):
        self.suit = suit
        self.rank = rank
        self.index = self.calc_index()

    def __str__(self):
        if self._suit == Suit.JIHAI.value:
            return f"Tile of { get_name(Jihai, self._rank) }"
        else:
            return f"Tile of { self._rank } { get_name(Suit, self._suit) }"

    @property
    def suit(self):
        return self._suit

    @suit.setter
    def suit(self, value: int):
        if not 0 <= value < 4:
            raise ValueError(f"Suit should be in: { get_values(Suit) }")
        self._suit = value

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, value: int):
        if self._suit == Suit.JIHAI.value:  # Jihai
            if not 1 <= value < 8:
                raise ValueError(
                    f"Value for Jihai should be in: "
                    f"{ get_values(Jihai) }")
        else:
            if not 1 <= value < 10:
                raise ValueError(
                    f"Value for { get_name(Suit, self._suit) }"
                    f"should be in: 1-9")
        self._rank = value

    def calc_index(self):
        return self._suit * 10 + self._rank

    @classmethod
    def from_index(cls, ind):
        return cls(ind // 10, ind % 10)

    @staticmethod
    def get_yaochuuhai() -> Tuple[List, List]:
        honor_tiles = []
        terminal_tiles = []
        for suit in Suit:
            if suit == Suit.JIHAI:
                for rank in Jihai:
                    honor_tiles.append(Tile(suit.value, rank.value))
            else:
                terminal_tiles.append(Tile(suit.value, 1))
                terminal_tiles.append(Tile(suit.value, 9))

        return honor_tiles, terminal_tiles

    def akadora(self):
        # red dora setter
        pass

    def next_tile(self):
        if self._suit == Suit.JIHAI.value:
            if self._rank <= Jihai.CHUN.value:
                new_rank = (self._rank % 3) + 1  # Sangenpai
            else:
                new_rank = (self._rank - 3) % 4 + 4  # Kazehai
        else:
            new_rank = (self.rank % 9) + 1  # MANZU, SOUZU, PINZU 1~9
        return self.from_index(self._suit * 10 + new_rank)

    def prev_tile(self):
        if self._suit == Suit.JIHAI.value:
            if self._rank <= Jihai.CHUN.value:
                new_rank = (self._rank + 1) % 3 + 1  # Sangenpai
            else:
                new_rank = (self._rank + 3) % 4 + 4  # Kazehai
        else:
            new_rank = (self.rank + 7) % 9 + 1  # MANZU, SOUZU, PINZU 1~9
        return self.from_index(self._suit * 10 + new_rank)

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __lt__(self, other):
        return self.suit < other.suit or (
            self.suit == other.suit and self.rank < other.rank
        )

    def __gt__(self, other):
        return self.suit > other.suit or (
            self.suit == other.suit and self.rank > other.rank
        )


class Stack:
    # TODO: maybe rename as Haiyama, which are the tiles arranged in walls?
    def __init__(self):
        self.stack = []

        self.dora_index = -5
        self.dora_indicators = []
        self.uradora_indicators = []
        self.doras = []
        self.uradoras = []

        self.initiate()
        self.playling_wall = iter(self.stack[:122])
        self.rinshanpai = iter(self.stack[-4:][::-1])  # 王牌是最後七墩，嶺上牌是槓可以抽的最後四張

    def initiate(self):
        for suit in range(0, 4):
            max_rank = 8 if suit == 0 else 10  # Jihai only have 7 values
            for rank in range(1, max_rank):
                for _ in itertools.repeat(None, 4):
                    self.stack.append(Tile(suit, rank))

        random.shuffle(self.stack)
        self.add_dora_indicator()

    def draw(self, from_rinshan: bool = False) -> Tile:
        if from_rinshan:
            return next(self.rinshanpai)
        return next(self.playling_wall)

    def add_dora_indicator(self):
        if len(self.doras) < 5:
            next_dora_ind = self.stack[self.dora_index]
            self.dora_indicators.append(next_dora_ind)

            next_uradora_ind = self.stack[self.dora_index - 1]
            self.uradora_indicators.append(next_uradora_ind)

            self.doras.append(self.compute_dora(next_dora_ind))
            self.uradoras.append(self.compute_dora(next_uradora_ind))
            self.dora_index -= 2
        else:
            raise ValueError(
                "Number of doras could only be less than 5"
            )
        return

    def get_dora_indicator(self):
        return self.dora_indicators

    def get_unadora_indicator(self):
        return self.uradora_indicators

    def get_dora(self):
        return self.doras

    def get_unadora(self):
        return self.uradoras

    @staticmethod
    def compute_dora(tile: Tile):
        return tile.next_tile()


class Huro:
    def __init__(self, naki_type: Naki, tiles: List[Tile]):
        self.naki_type = naki_type
        self.tiles = tiles

    @property
    def tiles(self):
        return self._tiles

    @tiles.setter
    def tiles(self, tiles: List[Tile]):
        self._tiles = tiles

    def add_kan(self, tile: Tile):
        # change type from PON to KAN
        if self.naki_type != Naki.PON:
            raise ValueError(
                "Adding kan is only available when the original "
                "naki type is PON"
            )
        self.naki_type = Naki.CHAKAN
        self._tiles.append(tile)
