from typing import List

from .player import Player
from .components import Stack


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
    def __init__(self):
        # Honcha 「本家」, player who discarded tile (好像沒有這個詞，我發明的)
        # Shimocha 「下家」, or player to the right of discard tile player
        # Toimen 「対面」, or player across discard tile player
        # Kamicha 「上家」, or player to the left of discard tile player
        # discard tile
        pass

    def discard_tile_handle(self):
        # any player can Ron? if yes, end of Kyoku
        # any palyer can Kan? if yes, draw a tile from rinshanpai
        # any palyer can Pon? if yes, choose_discard_tile()
        # can Shimocha Chii? if yes, choose_discard_tile()
        # Otherwise, Shimocha draw a tile from playling_wall
        pass

    def tile_in_handle(self):
        # can player tsumo? if yes, end of Kyoku
        # can player Kan? if yes, draw a tile from rinshanpai
        # Otherwise, choose_discard_tile()
        pass

    def choose_discard_tile(self):
        # can riichi?
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
