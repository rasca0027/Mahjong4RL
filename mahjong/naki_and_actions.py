from typing import List

from .components import Tile, Naki
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
      https://colab.research.google.com/drive/1ih1hU_EDRQ8z-NI0KJ7lVeORxJa7HmNf?usp=sharing:
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
            possible_list.append(Tile.from_index(value))
        elif value == 3 and new_tile.index == index:
            possible_list.append(Tile.from_index(value))
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
        tile_1 = Tile.from_index(new_tile.index - 1)
        tile_2 = Tile.from_index(new_tile.index - 2)
        if player.hand[tile_1.index] > 0 and player.hand[tile_2.index] > 0:
            possible_sets.append([tile_1, tile_2, new_tile])

    if new_tile.rank >= 2 and new_tile.rank <= 8:
        tile_1 = Tile.from_index(new_tile.index - 1)
        tile_3 = Tile.from_index(new_tile.index + 1)
        if player.hand[tile_1.index] > 0 and player.hand[tile_3.index] > 0:
            possible_sets.append([tile_1, new_tile, tile_3])

    if new_tile.rank <= 7:
        tile_2 = Tile.from_index(new_tile.index + 1)
        tile_3 = Tile.from_index(new_tile.index + 2)
        if player.hand[tile_2.index] > 0 and player.hand[tile_3.index] > 0:
            possible_sets.append([new_tile, tile_2, tile_3])

    return possible_sets


def check_riichi(tiles_in_hand, tile_to_dicard):
    """Helper function to check if player can declare riichi

    Args:
        tiles_in_hand (List of Tile objects):
            The player's current hand of 14 tiles
        tile_to_dicard (Tile object):
            Tile selected by player to discard

    Returns:
        bool: True for opportunity to declare riichi, False otherwise.
    """
    # check 副露
    # check 聽牌
    pass


def check_tenpai():
    """
    Return possible tenpai discard tile
    """
    pass
