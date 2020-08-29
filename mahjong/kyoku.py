from typing import List, Tuple

from .player import Player
from .components import Stack, Tile, Action


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

    def discard_flow(
        self, discard_tile: Tile, discard_pos: int
    ) -> Tuple[int, Tile]:
        """ An event flow starting with a discard tile. It contains two flows,
        Naki and Draw.
        Args:
          discard_tile: the tile discarded in previous turn
          discard_pos: the seating position of the player discarded the tile
        Return:
          state: -1 -> 流局
                  0 -> 繼續
                  pos -> player at pos 胡牌
          discard_tile: the discarded tile in this turn
                if Ron/Tsumo/流局 -> None
        """
        call_naki, player_pos, action = self.ensemble_actions(
            discard_tile, discard_pos)
        if call_naki:
            state, discard_tile = self.naki_flow(action)
        else:
            discarder = self.players[discard_pos]
            state, discard_tile = self.draw_flow(
                self.players[discarder.get_shimocha()])
        return state, discard_tile

    def naki_flow(
        self, player: Player, action: Action
    ) -> Tuple[int, Tile]:
        """An event flow deals with Naki process
        Args:
          player: The player that calls naki
          action: The naki action from that player
        Return:
          state: -1 -> 流局
                  0 -> 繼續
                  pos -> player at pos 胡牌
          discard_tile: the discarded tile in this turn
                if Ron/Tsumo/流局 -> None
        """
        state = 0
        if action == Action.RON:
            return player.seating_position, None

        player.action_with_naki(action)
        if action == Action.DAMINKAN:
            if not self.stack.can_add_dora_indicator():
                return -1, None
            self.stack.add_dora_indicator()
            state, discard_tile = self.draw_flow(player, from_rinshan=True)
        else:
            discard_tile = player.discard_after_naki()
        player.add_kawa(discard_tile)
        return state, discard_tile

    def ensemble_actions(
        self, discard_tile: Tile, discard_pos: int
    ) -> Tuple[bool, int, Action]:
        """This function ensembles the action from each player and return
        the highest priority action.
        Return:
          is_naki: True if there's a naki action from player else False
          pos: the position of the player with highest priority on naki action
          action: the naki action from the player
        """
        # TODO: Make sure the naki action script like this works :P
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

    def draw_flow(
        self, player, from_rinshan: bool = False
    ) -> Tuple[int, Tile]:
        """ An event flow that triggers a player to draw a tile and ends with
        that player discarding a tile.
        Args:
          player: the player to draw a tile
          from_rinshan: indicates this draw is from rinshan or not
        Return:
          state: -1 -> 流局
                  0 -> 繼續
                  pos -> player at pos 胡牌
          discard_tile: the discarded tile in this turn
                if Ron/Tsumo/流局 -> None
        """
        new_tile = self.stack.draw(from_rinshan)
        player.tmp_furiten = False
        action, discard_tile = player.action_with_new_tile(new_tile)
        state = 0
        if 3 <= action.value <= 5:
            if not self.stack.can_add_dora_indicator():
                return True, None
            self.stack.add_dora_indicator()
            state, discard_tile = self.draw_flow(player, from_rinshan=True)
        elif action == Action.TSUMO or action == Action.RON:
            state = player.seating_position
        else:
            pass
        player.add_kawa(discard_tile)
        return state, discard_tile


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
