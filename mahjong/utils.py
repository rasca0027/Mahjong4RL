import math
from enum import Enum


def get_values(en: Enum):
    return list(en.__members__.keys())


def get_name(en: Enum, key: str):
    return en(key).name


def roundup(x):
    return int(math.ceil(x / 100.0)) * 100


def isYaochuu(suit: int, rank: int) -> bool:
    '''determine the tile is yaochuu or not by its suit and rank
    '''
    if suit == 0:
        return True
    else:
        if rank == 1 or rank == 9:
            return True
