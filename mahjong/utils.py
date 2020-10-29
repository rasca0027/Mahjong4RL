from typing import DefaultDict
import math
import copy
from enum import Enum

from .components import Tile, Suit


def get_values(en: Enum):
    return list(en.__members__.keys())


def get_name(en: Enum, key: str):
    return en(key).name


def roundup(x):
    return int(math.ceil(x / 100.0)) * 100


def is_yaochuu(suit: int, rank: int) -> bool:
    '''determine the tile is yaochuu or not by its suit and rank
    '''
    if suit == 0:
        return True
    else:
        if rank == 1 or rank == 9:
            return True

    return False


def separate_sets(hand: DefaultDict[int, int], huro_count: int):
    """Helper function for seperating player's remaining hands into sets.
    It should either be 14, 11, 8, 5, or 2 tiles.
    Note that there's priority for koutsu over shuntsu,
    so might not be useful for yaku types like 混老頭, 清老頭, etc
    """

    for possible_jantou in hand.keys():
        if hand[possible_jantou] >= 2:  # try using it as jantou
            remain_tiles = copy.deepcopy(hand)
            remain_tiles[possible_jantou] -= 2

            koutsu = []
            shuntsu = []
            sets_to_find = 4 - huro_count
            for tile_index in sorted(remain_tiles.keys()):
                if tile_index < Tile(Suit.MANZU.value, 1).index:
                    if remain_tiles[tile_index] == 3:
                        sets_to_find -= 1
                        koutsu.append(Tile.from_index(tile_index))
                else:  # numbered tiles
                    if remain_tiles[tile_index] >= 3:  # check for Koutsu
                        remain_tiles[tile_index] -= 3
                        sets_to_find -= 1
                        koutsu.append(Tile.from_index(tile_index))
                    if remain_tiles[tile_index + 2] > 0:  # check for Shuntsu
                        chii_n = min(
                            remain_tiles[tile_index],
                            remain_tiles[tile_index + 1],
                            remain_tiles[tile_index + 2]
                        )
                        if chii_n > 0:
                            remain_tiles[tile_index] -= chii_n
                            remain_tiles[tile_index + 1] -= chii_n
                            remain_tiles[tile_index + 2] -= chii_n
                            sets_to_find -= chii_n
                            for _ in range(chii_n):
                                shuntsu.append([
                                    Tile.from_index(tile_index),
                                    Tile.from_index(tile_index) + 1,
                                    Tile.from_index(tile_index) + 2
                                ])
            if sets_to_find == 0:
                return koutsu, shuntsu, Tile.from_index(possible_jantou)
    return None
