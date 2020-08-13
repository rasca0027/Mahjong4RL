from typing import List

from .mahjong import Tile, Naki
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
    return player.hand[new_tile.index] >= 2


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


def check_tenpai(player: Player, new_tile: Tile):
    """
    Return possible tenpai discard tile
    """
    def get_all_tiles():
        all_tiles = []
        for suit in range(0, 4):
            max_rank = 7 if suit == 0 else 10
            for rank in range(1, max_rank):
                all_tiles.append(Tile(suit, rank))
        return all_tiles
    # do i need to add huro???
    # temporarily add tile into hand
    hand = player.hand.copy()
    hand[new_tile.index] += 1
    # all possible tiles
    all_tiles = get_all_tiles() 
    possible_winning_tiles = []
    # try discarding each tile:
    possible_discard_tile_id = [k for (k, v) in hand.items() if v > 0]
    for discard_id in possible_discard_tile_id:
        temp_hand = hand.copy()
        temp_hand[discard_id] -= 1
        machi = []
        # try adding each tile
        for tile in all_tiles:
            # temporarily add the possible tile
            temp_hand[tile.index] += 1
            if check_four_sets(temp_hand):
                machi.append(tile)
        if len(machi) > 0: 
            # there is at least one winning possibility if discarding this tile
            # if discard this, listening to machi
            possible_winning_tiles.append((discard_id, machi)) 
    return possible_winning_tiles


def check_four_sets(hand):
    def check_mentsu(remaining):
        found = 0
        for i, v in remaining.items():
            if v >= 3:
                remaining[i] -= 3
                found += 1
            t = Tile.get_tile_by_index(i)
            if t.suit != 0 and t.rank <= 7:
                if i + 1 in remaining and i + 2 in remaining:
                    pairs = min(remaining[i], remaining[i + 1], remaining[i + 2])
                    remaining[i] -= pairs
                    remaining[i + 1] -= pairs
                    remaining[i + 2] -= pairs
                    found += pairs
        return found == 4
    # remove jantou first
    possible_jantous = [k for (k, v) in hand.items() if v >= 2]
    for jantou in possible_jantous:
        temp_hand = hand.copy()
        temp_hand[jantou] -= 2
        if check_mentsu(temp_hand):
            return True
    return False
            

