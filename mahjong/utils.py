import math
from enum import Enum
from typing import List

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
