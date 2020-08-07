from enum import Enum


def get_values(en: Enum):
    return list(en.__members__.keys())


def get_name(en: Enum, key: str):
    return en(key).name
