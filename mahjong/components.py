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
    RYUUKYOKU = -1
    NOACT = 0
    NAKI = 1
    RIICHI = 2
    RON = 3
    TSUMO = 4
    DRAW = 5
    DRAW_RINSHAN = 6
    DISCARD = 7


class Tile:
    def __init__(self, suit: int, rank: int):
        self.suit = suit
        self.rank = rank
        self.index = self.calc_index()
        self.owner = None

    def __str__(self):
        if self._suit == Suit.JIHAI.value:
            return f"{ get_name(Jihai, self._rank) }"
        else:
            return f"{ self._rank } { get_name(Suit, self._suit) }"

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

    @property
    def owner(self):
        return self._owner

    @owner.setter
    def owner(self, seating_pos: int):
        if seating_pos is not None:
            if (not 0 <= seating_pos < 4) and seating_pos is not None:
                raise ValueError(
                    "Owner should be seating position (0~3) or None,"
                    f"Got {seating_pos} instead.")
        self._owner = seating_pos

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
        self.playing_wall = self.stack[:122].copy()
        self.rinshanpai = self.stack[-4:][::-1].copy()  # 王牌是最後七墩，嶺上牌是槓可以抽的最後四張

    def initiate(self):
        for suit in range(0, 4):
            max_rank = 8 if suit == 0 else 10  # Jihai only have 7 values
            for rank in range(1, max_rank):
                for _ in itertools.repeat(None, 4):
                    self.stack.append(Tile(suit, rank))

        random.shuffle(self.stack)
        self.add_dora_indicator()

    @property
    def is_haitei(self):
        return len(self.playing_wall) == 0

    def draw(self, from_rinshan: bool = False) -> Tile:
        if from_rinshan:
            self.playing_wall.pop(-1)
            return self.rinshanpai.pop(0)
        return self.playing_wall.pop(0)

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
    def __init__(self, naki_type: Naki, naki_tile: Tile, tiles: List[Tile]):
        self.naki_type = naki_type
        self.naki_tile = naki_tile
        self.tiles = tiles

    @property
    def tiles(self):
        return self._tiles

    @tiles.setter
    def tiles(self, tiles: List[Tile]):
        self._tiles = tiles

    def __str__(self):
        return "|".join(map(str, self.tiles))

    def add_kan(self, tile: Tile):
        # change type from PON to KAN
        if self.naki_type != Naki.PON:
            raise ValueError(
                "Adding kan is only available when the original "
                "naki type is PON"
            )
        self.naki_type = Naki.CHAKAN
        self._tiles.append(tile)

    def check_naki_type(self, naki_str: str) -> bool:
        """Check if the naki type is as the same as input
        Arg:
          naki_str: All naki actions including CHII, PON, DAMINKAN,
            CHAKAN, ANKAN, [KAN]
        Return:
          is_same: True if it meets the criterion
        """
        if naki_str == "CHII":
            return self.naki_type == Naki.CHII
        elif naki_str == "PON":
            return self.naki_type == Naki.PON
        elif naki_str == "KAN":
            return (
                self.naki_type == Naki.DAMINKAN
                or self.naki_type == Naki.CHAKAN
                or self.naki_type == Naki.ANKAN
            )
        elif naki_str == "DAMINKAN":
            return self.naki_type == Naki.DAMINKAN
        elif naki_str == "CHAKAN":
            return self.naki_type == Naki.CHAKAN
        elif naki_str == "ANKAN":
            return self.naki_type == Naki.ANKAN
        else:
            raise ValueError(f"{naki_str} not supported")
