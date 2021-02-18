import math
from enum import Enum

unicode_block = {1: '\U0001f004',
                 2: '\U0001f005',
                 3: '\U0001f006',
                 4: '\U0001f000',
                 5: '\U0001f001',
                 6: '\U0001f002',
                 7: '\U0001f003',
                 11: '\U0001f007',
                 12: '\U0001f008',
                 13: '\U0001f009',
                 14: '\U0001f00A',
                 15: '\U0001f00B',
                 16: '\U0001f00C',
                 17: '\U0001f00D',
                 18: '\U0001f00E',
                 19: '\U0001f00F',
                 21: '\U0001f010',
                 22: '\U0001f011',
                 23: '\U0001f012',
                 24: '\U0001f013',
                 25: '\U0001f014',
                 26: '\U0001f015',
                 27: '\U0001f016',
                 28: '\U0001f017',
                 29: '\U0001f018',
                 31: '\U0001f019',
                 32: '\U0001f01A',
                 33: '\U0001f01B',
                 34: '\U0001f01C',
                 35: '\U0001f01D',
                 36: '\U0001f01E',
                 37: '\U0001f01F',
                 38: '\U0001f020',
                 39: '\U0001f021'}


def get_values(en: Enum):
    return list(en.__members__.keys())


def get_name(en: Enum, key: str):
    return en(key).name


def roundup(x):
    return int(math.ceil(x / 100.0)) * 100
