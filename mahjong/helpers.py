import copy
from typing import DefaultDict, List, Tuple

from .components import Tile, Suit
from .naki_and_actions import check_remains_are_sets


def convert_hand(hand: DefaultDict[int, int]) -> List[Tile]:
    """Convert hand in default dict format to list of tiles
    """
    hand_tiles = []
    for tile_index, tile_count in sorted(hand.items()):
        for i in range(tile_count):
            hand_tiles.append(Tile.from_index(tile_index))
    return hand_tiles


def is_yaochuu(suit: int, rank: int) -> bool:
    '''determine the tile is yaochuu or not by its suit and rank
    '''
    if suit == 0:
        return True
    else:
        if rank == 1 or rank == 9:
            return True
    return False


def nine_yaochuus(hand: DefaultDict[int, int], new_tile: Tile) -> bool:
    yaochuu_found = 0
    for tile_index in hand.keys():
        suit = tile_index // 10
        rank = tile_index % 10
        if is_yaochuu(suit, rank):
            yaochuu_found += 1
    if is_yaochuu(new_tile.suit, new_tile.rank):
        yaochuu_found += 1
    return yaochuu_found >= 9


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


def separate_sets(
    hand: DefaultDict[int, int], huro_count: int, koutsu_first: bool = True
) -> Tuple[List[Tile], List[List[Tile]], Tile]:
    """Helper function for seperating player's remaining hands into sets.
    It should either be 14, 11, 8, 5, or 2 tiles.
    The arg koutsu_first would change the priority for koutsu and shuntsu,
    for example in the usecase for checking 全帯么九, shuntsu should have
    priority over koutsu.
    """

    def check_koutsu(sets_to_find):
        if remain_tiles[tile_index] >= 3:  # check for Koutsu
            remain_tiles[tile_index] -= 3
            sets_to_find -= 1
            koutsu.append(Tile.from_index(tile_index))
        return sets_to_find

    def check_shuntsu(sets_to_find):
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
                        Tile.from_index(tile_index + 1),
                        Tile.from_index(tile_index + 2)
                    ])
        return sets_to_find

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
                    if koutsu_first:
                        sets_to_find = check_koutsu(sets_to_find)
                        sets_to_find = check_shuntsu(sets_to_find)
                    else:
                        sets_to_find = check_shuntsu(sets_to_find)
                        sets_to_find = check_koutsu(sets_to_find)
            if sets_to_find == 0:
                return koutsu, shuntsu, Tile.from_index(possible_jantou)
    return [], [], None


def is_chi(tile_set: List[Tile]) -> bool:
    '''input a list of tiles and determine it's a chi set or not
    '''
    if len(tile_set) != 3:
        return False
    tile_set.sort()
    return tile_set[0].next_tile() == tile_set[1] and \
        tile_set[1].next_tile() == tile_set[2]


def is_pon(tile_set: List[Tile]) -> bool:
    '''input a list of tiles and determine it's a pon set or not
    '''
    if len(tile_set) != 3:
        return False
    return tile_set[0] == tile_set[1] == tile_set[2]


def get_atamahane_winner(discard_pos: int, winners: List[int]):
    """This function determines the actual winner according to order of
    seating closest to discarder.
    Return:
        winner_pos: List[int]
    """
    if not discard_pos:
        return [winners[0]]
    seats = [x + 4 for x in winners]
    winner_pos = min[seats]
    if winner_pos >= 4:
        winner_pos -= 4
    return [winner_pos]
