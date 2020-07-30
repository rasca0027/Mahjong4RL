
def check_ron(tiles_in_hand, new_tile):
    """Helper function to check if new tile is a winning hand
    The hand must have a valid yaku and it's not furiten 振聴

    Args:
        tiles_in_hand (List of Tile objects): The player's current hand
        new_tile (Tile object): The potential winning hand 

    Returns:
        bool: True for Ron, False otherwise.

    ref: https://colab.research.google.com/drive/1ih1hU_EDRQ8z-NI0KJ7lVeORxJa7HmNf?usp=sharing:
    """
    ...


def check_kan(tiles_in_hand, new_tile):
    """Helper function to check if new tile can form a tile grouping of four identical tiles with current hand

    Args:
        tiles_in_hand (List of Tile objects): The player's current hand
        new_tile (Tile object): The potential Kan tile

    Returns:
        bool: True for opportunity to call Kan, False otherwise.

    TODO: distinguish ankan and shouminkan?
    """
    ...


def check_pon(tiles_in_hand, new_tile):
    """Helper function to check if new tile can form a tile grouping of three identical tiles with current hand

    Args:
        tiles_in_hand (List of Tile objects): The player's current hand
        new_tile (Tile object): The potential Pon tile

    Returns:
        bool: True for opportunity to call Pon, False otherwise.
    """
    ...


def check_chii(tiles_in_hand, new_tile):
    """Helper function to check if new tile can form a tile grouping of three sequential tiles with current hand

    Args:
        tiles_in_hand (List of Tile objects): The player's current hand
        new_tile (Tile object): The potential Chii tile

    Returns:
        bool: True for opportunity to call Chii, False otherwise.
    """
    ...


def check_riichi(tiles_in_hand, tile_to_dicard):
     """Helper function to check if player can declare riichi

    Args:
        tiles_in_hand (List of Tile objects): The player's current hand of 14 tiles 
        tile_to_dicard (Tile object): Tile selected by player to discard

    Returns:
        bool: True for opportunity to declare riichi, False otherwise.
    """
    ...

