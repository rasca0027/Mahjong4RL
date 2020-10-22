import copy
from typing import List, DefaultDict, TYPE_CHECKING
from itertools import groupby

from .components import Tile, Suit, Naki, Huro
if TYPE_CHECKING:
    from .player import Player


def check_ron(player: 'Player', discarded_tile: Tile):
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
    if discarded_tile in check_tenpai(player.hand, player.kabe):
        if not check_furiten(player):
            if check_yaku(player):
                return True

    return False


def check_tsumo(player: 'Player', new_tile: Tile):
    """Helper function to check if new tile can form a winning hand
    The hand must have a valid yaku

    Args:
        player (Player): Current player, 手牌 副露 棄牌
        new_tile (Tile object): The potential winning hand

    Returns:
        bool: True for Ron, False otherwise.
    """
    if new_tile in check_tenpai(player.hand, player.kabe):
        return check_yaku(player.hand)
    else:
        return False


def check_yaku(hand: DefaultDict[int, int]):
    """Helper function to check if a winning hand had more than 1 yaku
    Args:
        player (Player): Current player, 手牌 副露 棄牌

    Returns:
        bool: True for Yaku >= 1, False otherwise.
    """
    return True


def check_furiten(player: 'Player') -> bool:
    """Check if the player is in any of the three kinds of furiten
    """
    # TODO: add test when finish tmp_furiten and permanent_furiten
    return (check_own_discard_furiten(player)
            or player.tmp_furiten
            or player.permanent_furiten)


def check_own_discard_furiten(player: 'Player') -> bool:
    """Helper function to check if the hand in tenpai is furiten
    If any of that player's winning tiles are present in one's own discard
    pile which includes Naki

    Args:
        player (Player): Current player, 手牌 副露 棄牌

    Returns:
        bool: True for Furiten, False otherwise.
    """
    return any(tile in player.kawa for
               tile in check_tenpai(player.hand, player.kabe))


def check_ankan(hand: DefaultDict[int, int], new_tile: Tile) -> List[Tile]:
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
    for index, value in hand.items():
        if value == 4:
            possible_list.append(Tile.from_index(index))
        elif value == 3 and new_tile.index == index:
            possible_list.append(Tile.from_index(index))
        else:
            pass
    return sorted(possible_list)


def check_chakan(hand: DefaultDict[int, int], kabe: List[Huro], new_tile: Tile
                 ) -> List[Tile]:
    """Helper function to check if new tile can form
      a tile grouping of four identical tiles with current
      Huros / 加槓
    Args:
        hand (DefaultDict): Player's hand
        kabe (List[Huro]): Player's kabe
        new_tile (Tile): The potential Kan tile

    Returns:
        possible_list: True for opportunity to call Kan, False otherwise.
    """
    pons = [
        huro.tiles[0] for huro in kabe if huro.naki_type == Naki.PON
    ]
    possible_list = []
    for pon_tile in pons:
        if hand[pon_tile.index] == 1:
            possible_list.append(pon_tile)
        elif new_tile == pon_tile:
            possible_list.append(pon_tile)
        else:
            pass
    return sorted(possible_list)


def check_daminkan(hand: DefaultDict[int, int], discarded_tile: Tile) -> bool:
    """Helper function to check if discarded tile can
       form a tile grouping of four identical tiles with
       current hand
       大明槓

    Args:
        hand (DefaultDict): Player's hand
        new_tile (Tile object): The potential Kan tile

    Returns:
        bool: True for opportunity to call Kan, False otherwise.
    """
    return hand[discarded_tile.index] == 3


def check_pon(hand: DefaultDict[int, int], discarded_tile: Tile) -> bool:
    """Helper function to check if new tile can form a tile grouping of three
       identical tiles with current hand

    Args:
        hand (DefaultDict): Player's hand
        new_tile (Tile object): The potential Pon tile

    Returns:
        bool: True for opportunity to call Pon, False otherwise.
    """
    return hand[discarded_tile.index] >= 2


def check_chii(hand: DefaultDict[int, int],
               new_tile: Tile) -> List[List[Tile]]:
    """Helper function to check if new tile can form a tile grouping of three
       sequential tiles with current hand
    上家（Kamicha）棄牌才能call

    Args:
        hand (DefaultDict): Player's hand
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
        if hand[tile_1.index] > 0 and hand[tile_2.index] > 0:
            possible_sets.append([tile_1, tile_2, new_tile])

    if new_tile.rank >= 2 and new_tile.rank <= 8:
        tile_1 = Tile.from_index(new_tile.index - 1)
        tile_3 = Tile.from_index(new_tile.index + 1)
        if hand[tile_1.index] > 0 and hand[tile_3.index] > 0:
            possible_sets.append([tile_1, new_tile, tile_3])

    if new_tile.rank <= 7:
        tile_2 = Tile.from_index(new_tile.index + 1)
        tile_3 = Tile.from_index(new_tile.index + 2)
        if hand[tile_2.index] > 0 and hand[tile_3.index] > 0:
            possible_sets.append([new_tile, tile_2, tile_3])

    return possible_sets


def check_riichi(kabe: List[Huro], machi: List[Tile]) -> bool:
    """Helper function to check if player can declare riichi

    Args:
        player (Player): Current player, 手牌 副露 棄牌
        machi (List of Tile): Every possible tile that could complete the hand

    Returns:
        bool: True for opportunity to declare riichi, False otherwise.
    """
    return not kabe and len(machi) > 0


def check_tenpai(hand: DefaultDict, kabe: List[Huro]) -> List[Tile]:
    """Helper function to check if player can declare tenpai with current
    tiles in hand. If so, return Machi tile(s) (waiting patterns)

    Args:
        hand: 手牌
        kabe: 副露

    Returns:
        possible_tiles:
            every possible tiles that could complete the hand
    """
    possible_tiles = []
    huro_count = len(kabe)

    def check_chiitoitsu(current_hand: DefaultDict) -> Tile:
        machi_tile = None
        if len([k for k, v in current_hand.items() if v == 2]) == 6:
            machi_idx = [k for k, v in current_hand.items() if v == 1][0]
            machi_tile = Tile.from_index(machi_idx)
            possible_tiles.append(machi_tile)

    def check_kokushi_musou(current_hand: DefaultDict) -> List[Tile]:
        honor_tiles, terminal_tiles = Tile.get_yaochuuhai()
        yaochuuhai = honor_tiles + terminal_tiles
        machi_tiles = []

        yaochuu_in_hand = {k: v for (k, v) in current_hand.items()
                           if Tile.from_index(k) in yaochuuhai}
        single_yaochuu_n = sum(v == 1 for v in yaochuu_in_hand.values())
        if single_yaochuu_n == 13:  # 13-way wait
            machi_tiles = yaochuuhai
        elif single_yaochuu_n == 11:  # single wait
            if len([v for v in yaochuu_in_hand.values() if v == 2]) == 1:
                machi_tiles = [i for i in yaochuuhai
                               if i.index not in yaochuu_in_hand.keys()]

        return machi_tiles

    def check_machi(machi_tile: Tile, current_hand: DefaultDict) -> bool:
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
            if check_machi(machi_tile, hand):
                possible_tiles.append(machi_tile)

    if huro_count == 0:
        check_chiitoitsu(hand)
        if machi_tiles := check_kokushi_musou(hand):
            possible_tiles += machi_tiles

    return [k for k, v in groupby(sorted(possible_tiles))]


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
