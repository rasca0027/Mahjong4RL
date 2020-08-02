import itertools
import random
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
    HAKU = 0
    HATSU = 1
    CHUN = 2
    TON = 3
    NAN = 4
    SHAA = 5
    PEI = 6


class Tile:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        if self._suit == 0:
            return f"Tile of { get_name(Jihai, self._rank) }"
        else:
            return f"Tile of { self._rank } { get_name(Suit, self._suit) }"

    @property
    def suit(self):
        return self._suit

    @suit.setter
    def suit(self, value):
        if not 0 <= value < 4:
            raise ValueError(f"Suit should be in: { get_values(Suit) }")
        self._suit = value

    @property
    def rank(self):
        return self._rank

    @rank.setter
    def rank(self, value):
        if self._suit == 0:  # Jihai
            if not 0 <= value < 7:
                raise ValueError(
                    f"Value for Jihai should be in: "
                    f"{ get_values(Jihai) }")
        else:
            if not 1 <= value < 10:
                raise ValueError(
                    f"Value for { get_name(Suit, self._suit) }"
                    f"should be in: 1-9")
        self._rank = value

    def akadora(self):
        # red dora setter
        pass


class Stack:
    def __init__(self):
        self.stack = []

        self.dora_index = -5
        self.dora_indicator = []
        self.unadora_indicator = []
        self.dora = []
        self.unadora = []

        self.initiate()
        self.playling_wall = iter(self.stack[:122])
        self.dead_wall = iter(self.stack[-14:])  # 嶺上牌

    def initiate(self):
        for suit in range(0, 4):
            max_rank = 7 if suit == 0 else 10  # Jihai only have 7 values
            for rank in range(1, max_rank):
                for _ in itertools.repeat(None, 4):
                    self.stack.append(Tile(suit, rank))

        random.shuffle(self.stack)
        self.add_dora_indicator()

    def add_dora_indicator(self):
        if self.can_add_dora_indicator():
            next_dora_ind = self.stack[self.dora_index]
            self.dora_indicator.append(next_dora_ind)

            next_unadora_ind = self.stack[self.dora_index-1]
            self.unadora_indicator.append(next_unadora_ind)

            self.dora.append(self.compute_dora(next_dora_ind))
            self.unadora.append(self.compute_dora(next_unadora_ind))
            self.dora_index -= 2
        else:
            raise ValueError(
                "Number of doras could only be less than 4"
            )
        return

    def get_dora_indicator(self):
        return self.dora_indicator

    def get_unadora_indicator(self):
        return self.unadora_indicator

    def get_dora(self):
        return self.dora

    def get_unadora(self):
        return self.unadora

    def can_add_dora_indicator(self):
        if self.dora_index < -11:
            return False
        return True

    @staticmethod
    def compute_dora(tile: Tile):
        target_rank = 0
        if tile.suit == Suit.JIHAI.value:
            if tile.rank < 3:
                # Sangenpai
                target_rank = (tile.rank + 1) % 3
            else:
                # Kazehai
                target_rank = (tile.rank - 3 + 1) % 4 + 3
        else:
            # others
            target_rank = tile.rank % 9 + 1

        return Tile(tile.suit, target_rank)
