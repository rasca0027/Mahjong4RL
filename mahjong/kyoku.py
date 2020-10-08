from typing import List, Tuple, Optional

from .player import Player
from .components import Stack, Tile, Action, Huro, Naki, Jihai


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
        atamahane=True
    ) -> None:
        # TODO: make sure players are sorted by seating position
        self.players = players
        self.stack = stack
        self.atamahane = atamahane
        self.winner = None

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

        player_pos, action = self.ensemble_actions(discard_tile, discard_pos)
        if action == Action.NOACT:
            discarder = self.players[discard_pos]
            state, discard_tile = self.draw_flow(
                self.players[discarder.get_shimocha()])
        else:
            state, discard_tile = self.naki_flow(action)

        if state > 0:
            self.winner = [state]
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

        # TODO: add test when finish action_with_naki()
        player.action_with_naki(action)
        if action == Action.DAMINKAN:
            if self.check_suukaikan(player.kabe):
                return -1, None
            state, discard_tile = self.draw_flow(player, from_rinshan=True)
        elif action in (Action.CHII, Action.PON):
            # TODO: add test when finish discard_after_naki()
            discard_tile = player.discard_after_naki()
        else:
            # TODO: invalid action, raise error
            pass
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
        naki_actions = [
            (i, self.players[i - 1].action_with_discard_tile(
                discard_tile, discard_pos))
            for i in range(1, 5) if i != discard_pos
        ]
        pos, action = max(naki_actions, key=lambda x: x[1].value)
        if action == Action.RON and not self.atamahane:
            ron_players = [i[0] for i in naki_actions if i[1] == Action.RON]
            if len(ron_players) > 1:
                self.winner = ron_players

        return pos, action

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
        if action == Action.CHAKAN or action == Action.ANKAN:
            player.action_with_naki(action)
            if self.check_suukaikan(player.kabe):
                return -1, None
            state, discard_tile = self.draw_flow(player, from_rinshan=True)
        elif action == Action.TSUMO:
            state = player.seating_position
        else:
            # TODO: invalid action, raise error
            pass

        if state > 0:
            self.winner = [state]
        else:
            player.add_kawa(discard_tile)

        return state, discard_tile

    def check_suukaikan(self, kabe: List[Huro]) -> bool:
        if len(self.stack.doras) >= 4:  # 場上已經有三或四個槓子
            if len([huro for huro in kabe if huro.naki_type == Naki.KAN]) != 4:
                # Suukaikan: four KAN are called by different player
                return True  # 流局
        self.stack.add_dora_indicator()
        return False


class Kyoku:
    """A portion of the game, starting from the dealing of tiles
    and ends with the declaration of a win, Ryuukyoku, or draw.
    """

    def __init__(
        self,
        players: List[Player],
        honba: int,
        bakaze: Jihai,
        atamahane: Optional[bool] = True,
    ):
        self.winner = None
        self.players = players
        # Assume the players is sorted by seating_position
        self.oya_player = players[0]
        self.honba = honba
        self.kyotaku = 0  # 供託
        self.bakaze = bakaze
        self.tile_stack = Stack()

        # Atamahane 「頭跳ね」 is more known as the "head bump" rule.
        # http://arcturus.su/wiki/Atamahane
        self.atamahane = atamahane

        # deal tiles to each player to produce their starting hands

        pass

    @property
    def honba(self):
        return self._honba

    @honba.setter
    def honba(self, honba: int):
        self._honba = honba

    @property
    def bakaze(self):
        return self._bakaze

    @bakaze.setter
    def bakaze(self, value: Jihai) -> None:
        if not 1 <= value <= 2:
            raise ValueError(
                "Bakaze should be 1 in Tonpuusen, should be 1 or 2 in Hanchan")
        self._bakaze = value

    def deal(self) -> None:
        for player in self.players:
            player.hand([self.tile_stack.draw() for _ in range(13)])
        return

    def start(self):
        """
        Return:
          state: -1 as Ryuukyoku, others as winning player
        """
        # initialize players' hand
        self.deal()

        # 莊家 oya draw flow
        turn = Turn(self.players, self.tile_stack)
        state, discard_tile, discard_pos = turn.draw_flow(self.oya_player)
        # Tenhoo
        while state == 0:
            state, distard_tile, discard_pos = turn.discard_flow(
                discard_tile, discard_pos)

        if state == -1:
            # TODO: deal with Ryuukyoku
            # nagashi mangan 流局滿貫
            # if check_nagashi():
            # return self.oya_player, 1
            # Ryuukyoku 流局
            # else:
            return self.oya_player.get_shimocha()
        else:
            # TODO: Check Yaku and calculate the amount.
            return next_player
            # TODO: setup next oya
        return state


class Game:
    def __init__(self):

        return
