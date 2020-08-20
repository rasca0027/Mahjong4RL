import copy
from typing import List, DefaultDict

from .components import Tile, Suit, Naki
from .player import Player


def check_ron(player: Player, discarded_tile: Tile):
    """Helper function to check if discarded tile can form a winning hand
    The hand must have a valid yaku and it's not furiten 振聴

    Args:
        player (Player): Current player, 手牌 副露 棄牌
        discarded_tile (Tile object): The potential winning hand

    Returns:
        bool: True for Ron, False otherwise.

    ref:
      https://colab.research.google.com/drive/1ih1hU_EDRQ8z-NI0KJ7lVeORxJa7HmNf?usp=sharing
    """
    ron = False
    if discarded_tile in check_tenpai(player):
        if not check_own_discard_furiten(player):
            if check_yaku(player):
                ron = True

    return ron


def check_tsumo(player: Player, new_tile: Tile):
    """Helper function to check if new tile can form a winning hand
    The hand must have a valid yaku

    Args:
        player (Player): Current player, 手牌 副露 棄牌
        new_tile (Tile object): The potential winning hand

    Returns:
        bool: True for Ron, False otherwise.
    """
    if new_tile in check_tenpai(player):
        return check_yaku(player)
    else:
        return False


def check_yaku(player: Player):
    """Helper function to check if a winning hand had more than 1 yaku
    Args:
        player (Player): Current player, 手牌 副露 棄牌

    Returns:
        bool: True for Yaku >= 1, False otherwise.
    """
    return True


def check_own_discard_furiten(player: Player) -> bool:
    """Helper function to check if the hand in tenpai is furiten
    If any of that player's winning tiles are present in one's own discard
    pile which includes Naki

    Args:
        player (Player): Current player, 手牌 副露 棄牌

    Returns:
        bool: True for Furiten, False otherwise.
    """
    return any(tile in player.kawa for tile in check_tenpai(player))


def temporary_furiten():
    """Any player in tenpai has the option to ignore a winning tile.
    By declining a call for ron, the player then becomes temporarily furiten
    until their next discard.

    """
    ...


def permanent_furiten():
    """When a player has declared riichi, the state of temporary furiten does
    not expire.

    """
    ...


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
            possible_list.append(Tile.from_index(index))
        elif value == 3 and new_tile.index == index:
            possible_list.append(Tile.from_index(index))
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
        tile_1 = Tile.from_index(new_tile.index - 2)
        tile_2 = Tile.from_index(new_tile.index - 1)
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
    """Helper function to check if player can declare tenpai with current
    tiles in hand. If so, return Machi tile(s) (waiting patterns)

    Args:
        player (Player): Current player, 手牌 副露 棄牌

    Returns:
        possible_list (List[Tile]):
            every possible tile that could complete the hand (Ron or Tsumo)
    """
    possible_list = []
    huro_count = len(player.kabe)

    def check_machi(machi_tile, current_hand):
        machi_found = False
        for tile_index in current_hand.keys():
            new_hand = copy.deepcopy(current_hand)
            new_hand[machi_tile.index] += 1
            if new_hand[tile_index] >= 2:
                new_hand[tile_index] -= 2
                if check_remains_are_sets(new_hand, huro_count):
                    machi_found = True
                    break
        return machi_found

    for suit in Suit:
        max_rank = 8 if suit == Suit.JIHAI else 10
        for rank in range(1, max_rank):
            machi_tile = Tile(suit.value, rank)
            if check_machi(machi_tile, player.hand):
                possible_list.append(machi_tile)

    return possible_list


def check_remains_are_sets(remain_tiles: DefaultDict[int, int],
                           huro_count: int) -> bool:
    """Helper function to check all tiles in remain_tiles can form into sets
    Set is defined as:
      1. Shuntsu 「順子」 is a tile group with three sequential numbered tiles
      2. Koutsu 「刻子」 is a tile group with three of the same type of tiles

    Args:
        remain_tiles (DefaultDict):
            tiles in hand after taking out Jantou (雀頭/眼) and Kabe
        huro_count:
            how many huro in player's kabe

    Returns:
        bool: True for tiles can form sets, False otherwise.
    """
    sets_to_find = 4 - huro_count

    for tile_index in sorted(remain_tiles.keys()):
        if tile_index < Tile(Suit.MANZU.value, 1).index:  # only check Koutsu
            if remain_tiles[tile_index] == 3:
                sets_to_find -= 1
        else:  # numbered tiles
            if remain_tiles[tile_index] >= 3:  # check for Koutsu
                remain_tiles[tile_index] -= 3
                sets_to_find -= 1
            if remain_tiles[tile_index + 2] > 0:  # check for Shuntsu
                chii_n = min(remain_tiles[tile_index],
                             remain_tiles[tile_index + 1],
                             remain_tiles[tile_index + 2])
                if chii_n > 0:
                    remain_tiles[tile_index] -= chii_n
                    remain_tiles[tile_index + 1] -= chii_n
                    remain_tiles[tile_index + 2] -= chii_n
                    sets_to_find -= chii_n

    return sets_to_find == 0
