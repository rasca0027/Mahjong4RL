from typing import List

from .player import Player
from .components import Stack, Tile, Action
from .utils import next_player


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
    def __init__(
        self, players: List[Player],
        stack: Stack,
    ) -> None:
        self.players = players
        self.stack = stack

    def discard_flow(self, discard_tile: Tile, discard_pos: int):
        call_naki, player_pos, action = self.ensemble_actions(
            discard_tile, discard_pos)
        if call_naki:
            state, discarded_tile = self.naki_flow(action)
        else:
            state, discarded_tile = self.draw_flow(
                self.players[next_player(discard_pos)])
        return state, discarded_tile

    def naki_flow(self, player: Player, action: Action):
        # different naki: CHII, PON, DAMINKAN, RON
        is_end = False
        if action == Action.RON:
            return True, None

        player.action_with_naki(action)
        if action == Action.DAMINKAN:
            if not self.stack.can_add_dora_indicator():
                return True, None
            self.stack.add_dora_indicator()
            is_end, discard_tile = self.draw_flow(player, from_rinshan=True)
        else:
            discard_tile = player.discard_after_naki()
        return is_end, discard_tile

    def ensemble_actions(self, discard_tile: Tile, discard_pos: int):
        # actions from each player
        naki_actions = [
            (i, zip(**self.players[i].action_with_discard_tile(
                discard_tile, discard_pos)))
            for i in range(4) if i != discard_pos
        ]
        pos, action = max(naki_actions, key=lambda x: x[1].value)
        if action == Action.NOACT:
            is_naki = False
        else:
            is_naki = True
        return is_naki, pos, action

    def draw_flow(self, player, from_rinshan: bool = False):
        # Give the player a new Tile and action with that
        new_tile = self.stack.draw(from_rinshan)
        action, discard_tile = player.action_with_new_tile(new_tile)
        is_end = False
        if 3 <= action.value <= 5:
            if not self.stack.can_add_dora_indicator():
                return True, None
            self.stack.add_dora_indicator()
            is_end, discard_tile = self.draw_flow(player, from_rinshan=True)
        elif action == Action.TSUMO or action == Action.RON:
            is_end = True
        else:
            pass
        return is_end, discard_tile


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
