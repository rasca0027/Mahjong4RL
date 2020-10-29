import math
import copy
from enum import Enum
from typing import DefaultDict, List

from .naki_and_actions import check_remains_are_sets
from .components import Tile


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


def consists_jantou_and_sets(remain_tiles: DefaultDict[int, int],
                             took_out_sets_n: int) -> bool:
    """Helper function to check all tiles in remain_tiles consists one Jantou
    and the other tiles can form into sets

    Args:
        remain_tiles (DefaultDict):
            tiles in hand after taking out some sets
        took_out_sets_n:
            how many sets been taken out

    Returns:
        bool: True for tiles can form sets, False otherwise.
    """
    for tile_index in remain_tiles.keys():
        if remain_tiles[tile_index] >= 2:
            tmp_hand = copy.deepcopy(remain_tiles)
            tmp_hand[tile_index] -= 2
            if check_remains_are_sets(tmp_hand, took_out_sets_n):
                return True
    return False


def is_chi(tile_set: List[Tile]) -> bool:
    '''input a list of tiles and determine it's a chi set or not
    '''
    if len(tile_set) != 3:
        return False
    tile_set.sort()
    return tile_set[0].next_tile == tile_set[1] and \
        tile_set[1].next_tile == tile_set[2]


def is_pon(tile_set: List[Tile]) -> bool:
    '''input a list of tiles and determine it's a pon set or not
    '''
    if len(tile_set) != 3:
        return False
    return tile_set[0] == tile_set[1] == tile_set[2]
