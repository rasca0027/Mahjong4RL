from .mahjong import Tile


def check_ron(player, new_tile):
    """Helper function to check if new tile is a winning hand
    The hand must have a valid yaku and it's not furiten 振聴

    Args:
        player (Player): Current player, 手牌 副露 棄牌
        new_tile (Tile object): The potential winning hand 

    Returns:
        bool: True for Ron, False otherwise.

    ref: https://colab.research.google.com/drive/1ih1hU_EDRQ8z-NI0KJ7lVeORxJa7HmNf?usp=sharing:
    """
    ...

def check_tsumo(player, new_tile):
    pass

def check_yaku():
    pass

def check_furiten():
    pass

def check_kan(player, new_tile):
    """Helper function to check if new tile can form a tile grouping of four identical tiles with current hand
    明槓 暗槓 加槓

    Args:
        player (Player): Current player, 手牌 副露 棄牌
        new_tile (Tile object): The potential Kan tile

    Returns:
        bool: True for opportunity to call Kan, False otherwise.
    """
    ...

def check_pon(player, new_tile):
    """Helper function to check if new tile can form a tile grouping of three identical tiles with current hand

    Args:
        player (Player): Current player, 手牌 副露 棄牌
        new_tile (Tile object): The potential Pon tile

    Returns:
        bool: True for opportunity to call Pon, False otherwise.
    """
    ...


def check_chii(player, new_tile):
    """Helper function to check if new tile can form a tile grouping of three sequential tiles with current hand
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

    if player.hand[new_tile.index - 1] > 0:
        if player.hand[new_tile.index - 2] > 0:
            possible_sets.append([Tile.get_tile_by_index(new_tile.index - 1),
                                  Tile.get_tile_by_index(new_tile.index - 2),
                                  new_tile])
        if player.hand[new_tile.index + 1] > 0:
            possible_sets.append([Tile.get_tile_by_index(new_tile.index - 1),
                                  new_tile,
                                  Tile.get_tile_by_index(new_tile.index + 1)])

    if player.hand[new_tile.index + 1] > 0:
        if player.hand[new_tile.index + 2] > 0:
            possible_sets.append([new_tile,
                                  Tile.get_tile_by_index(new_tile.index + 1),
                                  Tile.get_tile_by_index(new_tile.index + 2)])

    return possible_sets


def check_riichi(tiles_in_hand, tile_to_dicard):
     """Helper function to check if player can declare riichi

    Args:
        tiles_in_hand (List of Tile objects): The player's current hand of 14 tiles 
        tile_to_dicard (Tile object): Tile selected by player to discard

    Returns:
        bool: True for opportunity to declare riichi, False otherwise.
    """
    # check 副露
    # check 聽牌
    ...

def check_tenpai():
    """
    Return possible tenpai discard tile
    """
    pass
