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
    def __init__(self, turn_id, honcha, discard_tile):
        self.turn_id = turn_id
        # Honcha 「本家」, player who discarded tile (好像沒有這個詞，我發明的)
        self.honcha: Player = honcha
        # Shimocha 「下家」, or player to the right of discard tile player
        # Toimen 「対面」, or player across discard tile player
        # Kamicha 「上家」, or player to the left of discard tile player
        self.discard_tile = discard_tile
        self.log = ...

        self.discard_tile_handle(self.discard_tile)

        pass

    def discard_tile_handle(self, discard_tile):
        self.action = None
        self.next_player = self.shimocha
        # while action == None:
        # any player can Ron? if yes, end of Kyoku
        #     for player in players:
        #         if check_ron(player, discard_tile):
        #             self.confirm_action()
        #             self.action = 'Ron'
        #             self.next_player = player
        #      可以雙響、三響砲嗎？
        #
        # any palyer can Kan? if yes, draw_from_rinshanpai()
        #     for player in players:
        #         if check_daminkan(player, discard_tile):
        #             self.confirm_action()
        #             self.action = 'Kan'
        #             self.next_player = player
        # any palyer can Pon? if yes, choose_discard_tile()
        # can Shimocha Chii? if yes, choose_discard_tile()
        # Otherwise, Shimocha draw a tile from playling_wall
        #
        # if action == 'Ron': ...
        # elif action == 'Kan': draw_from_rinshanpai(self.next_player)
        # elif action == 'Pon': choose_discard_tile(self.next_player)
        # elif action == 'Chii': choose_discard_tile(self.next_player)
        # else: draw_from_playling_wall(self.next_player)
        pass

    def tile_in_handle(self, next_player):
        self.action = None
        self.next_player = next_player
        self.next_discard_tile = None
        # while action == None:
        # can player tsumo? if yes, end of Kyoku
        # can player Kan? if yes, draw_from_rinshanpai()
        # Otherwise, choose_discard_tile()
        #
        # if action == 'tsumo': ...
        # elif action in ('ankan', 'chakan'):
        #     draw_from_rinshanpai(self.next_player)
        # else: choose_discard_tile(self.next_player)
        pass

    def draw_from_rinshanpai(self, next_player):
        self.next_player = next_player
        # draw a tile from rinshanpai
        # self.next_player.hand[next(stack.rinshanpai).index] += 1
        # tile_in_handle(self.next_player)
        pass

    def draw_from_playling_wall(self, next_player):
        self.next_player = next_player
        # draw a tile from playing wall
        # self.next_player.hand[next(stack.playling_wall).index] += 1
        # tile_in_handle(self.next_player)
        pass

    def choose_discard_tile(self):
        self.next_discard_tile = None
        self.declear_riichi = False
        # user input discard tile
        # if check_riichi() and confirm_action(): self.declear_riichi = True
        pass

    def confirm_action(self):
        # user input
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
