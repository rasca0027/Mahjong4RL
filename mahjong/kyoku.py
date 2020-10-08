from typing import List, Tuple, Optional

from .player import Player, Position
from .components import Stack, Tile, Action, Huro, Naki
from .utils import roundup
from .naki_and_actions import check_tenpai


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
        self.winner = []

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
                  1 -> somebody RON or TSUMO
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
            self.winner.append(player)
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

    def kan_flow(self, kan_player, kan_tile, kan_type):
        """ An event flow followed by a player ankans or chakans
        Other players could Chankan. There are only two posible actions,
        RON and NOACT.
        Args:
          kan_player: the player who Kans
          kan_tile: the kan tile
          kan_type: two different actions may occur: CHAKAN / ANKAN
        Return:
          state: 0 -> 繼續
                 1 -> somebody CHANKAN, RON
        """
        # walk through 3 other players
        p = kan_player
        for i in range(3):
            p = p.get_shimocha()
            act = p.action_with_chakan(kan_tile, kan_type)
            if act == Action.RON:
                self.winner.append(p.seating_position)
        return 1 if self.winner else 0

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
        action, action_tile = player.action_with_new_tile(new_tile)
        state = 0
        if action == Action.CHAKAN or action == Action.ANKAN:
            state2 = self.kan_flow(player, action_tile, action)
            player.action_with_naki(action)
            if state2:
                return state2, None
            if self.check_suukaikan(player.kabe):
                return -1, None
            state, discard_tile = self.draw_flow(player, from_rinshan=True)
        elif action == Action.TSUMO:
            state = 1
            self.winner.append(player)
        else:
            # TODO: invalid action, raise error
            pass

        if state < 1:
            player.add_kawa(action_tile)

        return state, action_tile

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
        atamahane: Optional[bool]=True,
    ):
        self.winner = []
        self.players = players
        # Assume the player is sorted as TON NAN SHII PEI
        self.oya_player = players[0]
        self.honba = honba
        self.kyotaku = 0 # 供託
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
    def bakaze(self, position: Position):
        self._bakaze = position
        return

    def deal(self) -> None:
        for player in self.players:
            player.hand([self.tile_stack.draw() for _ in range(13)])
        return

    def start(self):
        """
        Return:
            renchan: bool, if the oya is same player or not
            kyotaku: int, how many kyotakus still exist
            honba: int, what's the honba for next Kyoku
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
            # TODO: 檢查流局是否聽牌 
            if check_tenpai(self.oya_player.hand, self.oya_player.kabe):
                return True, self.kyotaku, self.honba + 1
            else:
                return False, self.kyotaku, 0
            
        else:
            # TODO: 三家和流局: if len(sef.winner) == 3
            # TODO: Check Yaku and calculate the amount.

            han, fu = calculate_yaku()
            self.apply_points(han, fu, tsumo, loser)
            if self.oya_player in self.winner:
                # return next oya, kyotaku, honba
                return True, 0, self.honba + 1 
            return False, 0, 0
    
    def calculate_base_points(self, han: int, fu: int) -> int:
        points = fu * 2**(han + 2)
        if points > 2_000:
            if han <= 5: # mangan
                points = 2_000
            elif han == 6 or han == 7:
                points = 3_000
            elif han >= 8 and han <= 10:
                points = 4_000
            elif han == 11 or han == 12:
                points = 6_000
            elif han >= 13:
                points = 8_000 # 還要handle 雙倍役滿?
        return points
       
    def apply_points(self, han: int, fu: int, tsumo: bool, loser: Optional[Player] = None):
        pt = self.calculate_base_points(han, fu)
        # TODO: only handle atamahane for now
        if self.winner == self.oya_player:
            if tsumo:
                self.winner.points += roundup(pt * 2) * 3 + 300 * self.honba
                for i in range(1, 4):
                    self.players[i].points -= roundup(pt * 2) + 100 * self.honba
            else:
                self.winner.points += roundup(pt * 6) + 300 * self.honba
                loser.points -= roundup(pt * 6) + 300 * self.honba
        else: # 子家
            if tsumo:
                self.winner.points += roundup(pt * 2) + roundup(pt) + 100 * self.honba
                self.oya_player.points -= roundup(pt * 2) + 100 * self.honba
                for i in range(1, 4):
                    if self.players[i] != winner:
                        self.players[i].points -= roundup(pt) + 100 * self.honba
            else:
                self.winner.points += roundup(pt * 4) + 300 * self.honba
                loser.points -= roundup(pt * 4) + 300 * self.honba
        if self.kyotaku > 0:
            self.winner.points += self.kyotaku * 1_000
        return


class Game:
    def __init__(self):

        return
