from typing import List

from .player import Player
from .components import Tile, Stack
from .naki_and_actions import (
    check_ron, check_daminkan, check_pon, check_chii,
    check_tsumo, check_riichi, check_ankan, check_chakan)


class Action(Enum):
    RON = 0
    TSUMO = 1
    CHII = 2
    PON = 3
    DAMINKAN = 4
    ANKAN = 5
    CHAKAN = 6


class Turn:
    """ A portion of the kyoku, starting from one player discarding tile and
    ends with the next palyer selecting tile to discard.
    From dealer's initial discard onward, each player gets a turn to draw
    a tile from the wall, all players, except the discarder,
    has the option of claiming a discarded tile by chii, pon, kan, or ron.
    If no claims of the discard are made, then the next player draws from
    the wall and makes a discard, unless the hand is a winning hand with
    the declaration of tsumo. see flowchart in README
    """
    def __init__(self, discarded_tile: Tile, discarder: Player, player: Player):
        self.discarded_tile = discarded_tile
        self.player = player
        if (discarder.seating_position + 1) % 4 == player.seating_position:
            self.is_kamicha = True
        else:
            self.is_kamicha = False
        self.check_available_actions()

    def check_available_actions():
        actions = []
        if check_ron(self.player, self.discarded_tile):
            actions.push(Action.RON.value)
        if check_daminkan(self.player, self.discarded_tile):
            actions.push(Action.DAMINKAN.value)
        if check_pon(self.player, self.discarded_tile):
            actions.push(Action.PON.value)
        if self.is_kamicha and check_chii(self.player, self.discarded_tile):
            actions.push(Action.CHII.value)
        return actions
        
    def hand_process(new_tile: Tile):
        if check_tsumo(self.player, new_tile):
            pass
        pass

class Kyoku:
    """A portion of the game, starting from the dealing of tiles
    and ends with the declaration of a win, aborted hand, or draw.
    """
    def __init__(self, players: List[Player]):
        self.winner = None
        self.players = players
        # initiate tile stack
        self.tile_stack = Stack()

        # deal tiles to each player to produce their starting hands
        pass

    # The game begins with the dealer's initial discard.
    # while self.winner, repeat Turn
