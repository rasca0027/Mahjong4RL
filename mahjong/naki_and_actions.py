import copy
from typing import List, DefaultDict

from .mahjong import Tile, Suit, Naki
from .player import Player


def check_ron(player, new_tile):
    """Helper function to check if new tile is a winning hand
    The hand must have a valid yaku and it's not furiten 振聴

    Args:
        player (Player): Current player, 手牌 副露 棄牌
        new_tile (Tile object): The potential winning hand

    Returns:
        bool: True for Ron, False otherwise.

    ref:
      https://colab.research.google.com/drive/1ih1hU_EDRQ8z-NI0KJ7lVeORxJa7HmNf?usp=sharing
    """
    ...


def check_tsumo(player, new_tile):
    pass


def check_yaku():
    pass


def check_furiten():
    pass


def check_ankan(player: Player, new_tile: Tile) -> List[Tile]:
    """Helper function to check if new hand tile
      can form a tile grouping of four identical tiles
      with current hand / 暗槓

    Args:
      player (Player): Current player, 手牌 副露 棄牌
      new_tile (Tile): The potential Kan tile

    Returns:
      possible_list (List[Tile]):
        every possible tile that could result in an ankan
    """
    possible_list = []
    for index, value in player.hand.items():
        if value == 4:
            possible_list.append(Tile.get_tile_by_index(value))
        elif value == 3 and new_tile.index == index:
            possible_list.append(Tile.get_tile_by_index(value))
        else:
            pass
    return sorted(possible_list)


def check_chakan(player: Player, new_tile: Tile) -> List[Tile]:
    """Helper function to check if new tile can form
      a tile grouping of four identical tiles with current
      Huros / 加槓
    Args:
        player (Player): Current player, 手牌 副露 棄牌
        new_tile (Tile): The potential Kan tile

    Returns:
        possible_list: True for opportunity to call Kan, False otherwise.
    """
    pons = [
        huro.tiles[0] for huro in player.kabe if huro.naki_type == Naki.PON
    ]
    possible_list = []
    for pon_tile in pons:
        if player.hand[pon_tile.index] == 1:
            possible_list.append(pon_tile)
        elif new_tile == pon_tile:
            possible_list.append(pon_tile)
        else:
            pass
    return sorted(possible_list)


def check_daminkan(player: Player, discarded_tile: Tile) -> bool:
    """Helper function to check if discarded tile can
       form a tile grouping of four identical tiles with
       current hand
       大明槓

    Args:
        player (Player): Current player, 手牌 副露 棄牌
        new_tile (Tile object): The potential Kan tile

    Returns:
        bool: True for opportunity to call Kan, False otherwise.
    """
    return player.hand[discarded_tile.index] == 3


def check_pon(player: Player, discarded_tile: Tile) -> bool:
    """Helper function to check if new tile can form a tile grouping of three
       identical tiles with current hand

    Args:
        player (Player): Current player, 手牌 副露 棄牌
        new_tile (Tile object): The potential Pon tile

    Returns:
        bool: True for opportunity to call Pon, False otherwise.
    """
    return player.hand[discarded_tile.index] >= 2


def check_chii(player: Player, new_tile: Tile) -> List[List[Tile]]:
    """Helper function to check if new tile can form a tile grouping of three
       sequential tiles with current hand
    上家（Kamicha）棄牌才能call

    Args:
        player (Player): Current player, 手牌 副露 棄牌
        new_tile (Tile object): The potential Chii tile

    Returns:
        empty list, or list of possible combinations.
    """
    possible_sets = []

    if new_tile.suit == 0:
        return possible_sets

    if new_tile.rank >= 3:
        prev_tile = Tile.get_tile_by_index(new_tile.index - 1)
        prev_prev_tile = Tile.get_tile_by_index(new_tile.index - 2)
        if (player.hand[prev_tile.index] > 0 and 
                player.hand[prev_prev_tile.index] > 0):
            possible_sets.append([prev_prev_tile, prev_tile, new_tile])

    if new_tile.rank >= 2 and new_tile.rank <= 8:
        prev_tile = Tile.get_tile_by_index(new_tile.index - 1)
        next_tile = Tile.get_tile_by_index(new_tile.index + 1)
        if (player.hand[prev_tile.index] > 0 and 
                player.hand[next_tile.index] > 0):
            possible_sets.append([prev_tile, new_tile, next_tile])

    if new_tile.rank <= 7:
        next_tile = Tile.get_tile_by_index(new_tile.index + 1)
        next_next_tile = Tile.get_tile_by_index(new_tile.index + 2)
        if (player.hand[next_tile.index] > 0 and 
                player.hand[next_next_tile.index] > 0):
            possible_sets.append([new_tile, next_tile, next_next_tile])

    return possible_sets


def check_riichi(player: Player, machi: List[Tile]) -> bool:
    """Helper function to check if player can declare riichi

    Args:
        player (Player): Current player, 手牌 副露 棄牌
        machi (List of Tile): Every possible tile that could complete the hand

    Returns:
        bool: True for opportunity to declare riichi, False otherwise.
    """
    return not player.kabe and len(machi) > 0


def check_tenpai(player: Player) -> List[Tile]:
    """Helper function to check if player can declare is tenpai
    and what Machi is (waiting patterns)

    Args:
        player (Player): Current player, 手牌 副露 棄牌

    Returns:
        possible_list (List[Tile]):
            every possible tile that could complete the hand (Ron or Tsumo)
    """
    possible_list = []

    def check_machi(machi_tile, current_hand):
        machi_found = False
        for tile_index in sorted(current_hand.keys()):
            new_hand = copy.deepcopy(current_hand)
            new_hand[machi_tile.index] += 1
            if new_hand[tile_index] >= 2:
                new_hand[tile_index] -= 2
                if check_remains_are_sets(new_hand):
                    machi_found = True
        return machi_found

    for suit in Suit:
        max_rank = 8 if suit == Suit.JIHAI else 10
        for rank in range(1, max_rank):
            machi_tile = Tile(suit.value, rank)
            current_hand = copy.deepcopy(player.hand)
            if current_hand[machi_tile.index] != 4:
                if check_machi(machi_tile, current_hand):
                    possible_list.append(machi_tile)

    return possible_list


def check_remains_are_sets(remain_tiles: DefaultDict[int, int]) -> bool:
    """Helper function to check all tiles in remain_tiles can form into sets

    Args:
        remain_tiles (DefaultDict):
            tiles in hands after taking out Jantou (雀頭/眼)

    Returns:
        bool: True for tiles can form sets, False otherwise.
    """
    remain_tiles_n = sum(remain_tiles.values())
    if remain_tiles_n % 3 > 0:
        raise ValueError(f"Remain tiles should be multiples of 3,"
                         f"got { remain_tiles_n } instead.")

    sets_to_find = int(remain_tiles_n / 3)

    for tile_index in sorted(remain_tiles.keys()):
        if tile_index < Tile(Suit.MANZU.value, 1).index:  # 字牌檢查碰
            if remain_tiles[tile_index] == 3:
                sets_to_find -= 1
        else:  # 萬索餅牌
            if remain_tiles[tile_index] >= 3:  # check for pung
                remain_tiles[tile_index] -= 3
                sets_to_find -= 1
            if remain_tiles[tile_index + 2] > 0:  # check for chii
                chii_n = min(remain_tiles[tile_index],
                             remain_tiles[tile_index + 1],
                             remain_tiles[tile_index + 2])
                if chii_n > 0:
                    remain_tiles[tile_index] -= chii_n
                    remain_tiles[tile_index + 1] -= chii_n
                    remain_tiles[tile_index + 2] -= chii_n
                    sets_to_find -= chii_n

    return sets_to_find == 0
