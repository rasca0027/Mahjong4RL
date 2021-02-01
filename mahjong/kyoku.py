from typing import List, Tuple, Optional

from .player import Player
from .components import Stack, Tile, Action, Huro, Naki, Jihai
from .event_logger import KyokuLogger
from .helpers import get_atamahane_winner, get_wind_tiles, check_all_equal
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
        self,
        players: List[Player],
        stack: Stack,
        logger: KyokuLogger,
        atamahane: bool = True,
    ) -> None:
        # TODO: make sure players are sorted by seating position
        self.players = players
        self.stack = stack
        self.first_turn = True  # 開局連打四張內算第一輪，四張後或有人鳴牌則非第一輪
        self.is_haiteihai = False
        self.oya_draws = 0  # temporary
        self.atamahane = atamahane
        self.winners_pos = []
        self.logger = logger

    def discard_flow(
        self, discard_tile: Tile, discard_pos: int
    ) -> Tuple[int, Tile, int, Action]:
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
          discard_pos: the discarder's index
          action: the player's action with discard tile in this turn
        """
        state = 0
        discarder = self.players[discard_pos]

        # TODO: find a better place to check playling_wall, same as line 225
        if len(self.stack.playling_wall) == 0:
            self.is_haiteihai = True

        player_pos, (action, naki) = self.ensemble_actions(
            discard_tile, discard_pos)

        # TODO: check this is_haiteihai logic
        if (action == Action.NOACT) & (not self.is_haiteihai):
            state, discard_tile, discard_pos, action = self.draw_flow(
                self.players[discarder.get_shimocha()])

        elif action == Action.NAKI:
            # log Naki here
            self.logger.log(
                p_pos=player_pos,
                action=action,
                action_tile=discard_tile,
                naki_type=naki,
            )

            discarder.furiten_tiles_idx.add(discard_tile.index)
            state, discard_tile, discard_pos, act = self.naki_flow(
                self.players[player_pos], naki)

        elif action == Action.RON:
            # log Ron here
            self.logger.log(
                p_pos=player_pos,
                action=action,
                action_tile=discard_tile,
            )
            state = 1
            discard_tile = None
            discard_pos = None

        # TODO: invalid action, raise error

        return state, discard_tile, discard_pos, action

    def naki_flow(
        self, player: Player, naki: Naki
    ) -> Tuple[int, Tile, int]:
        """An event flow deals with Naki process
        Args:
          player: The player that calls naki
          naki: The naki action from that player
        Return:
          state: -1 -> 流局
                  0 -> 繼續
                  1 -> somebody RON or TSUMO
          discard_tile: the discarded tile in this turn
                if Ron/Tsumo/流局 -> None
          discard_pos: the discarder's index
        """
        self.first_turn = False

        state = 0
        # TODO: add test when finish action_with_naki()
        kuikae_tiles = player.action_with_naki(naki)
        discard_pos = player.seating_position
        if naki == Naki.DAMINKAN:
            if self.check_suukaikan(player.kabe):
                return -1, None, None, None
            state, discard_tile, discard_pos, _ = self.draw_flow(
                player, from_rinshan=True)
        elif naki in (Naki.CHII, Naki.PON):
            # TODO: add test when finish discard_after_naki()
            discard_tile = player.discard_after_naki(kuikae_tiles)
            # Log discard after naki
            self.logger.log(
                p_pos=discard_pos,
                action=Action.DISCARD,
                action_tile=discard_tile,
            )
        else:
            # TODO: invalid action, raise error
            pass

        return state, discard_tile, discard_pos, Action.NOACT

    def ensemble_actions(
        self, discard_tile: Tile, discard_pos: int
    ) -> Tuple[bool, int, Action]:
        """This function ensembles the action from each player and return
        the highest priority action.
        Return:
          pos: the position of the player with highest priority on naki action
          action: the action from the player
          naki: Naki
        """
        naki_actions = [
            (i, self.players[i].action_with_discard_tile(
                discard_tile, discard_pos, self.is_haiteihai))
            for i in range(0, 4) if i != discard_pos
        ]

        def sort_action(naki_actions):
            (action, naki) = naki_actions[1]
            return (action.value, naki.value if naki else 0)

        pos, (action, naki) = sorted(
            naki_actions,
            key=sort_action,
            reverse=True)[0]

        if action == Action.RON:
            ron_players = [i[0] for i in naki_actions if i[1][0] == Action.RON]
            if self.atamahane:
                self.winners_pos = [
                    get_atamahane_winner(discard_pos, ron_players)]
            else:
                if len(ron_players) >= 3:
                    return -1, (Action.RYUUKYOKU, None)
                self.winners_pos = ron_players
        elif action == Action.TSUMO:
            self.winners_pos = [pos]

        return pos, (action, naki)

    def kan_flow(self, kan_player: Player, kan_tile: Tile, kan_type: Naki):
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
            p = self.players[p.get_shimocha()]
            act = p.action_with_chakan(kan_tile, kan_type)
            if act == Action.RON:
                self.logger.log(
                    p_pos=p.seating_position,
                    action=act,
                    action_tile=kan_tile,
                )
                self.winners_pos.append(p.seating_position)
        if len(self.winners_pos) > 0:
            return 1, kan_tile, kan_player.seating_position, act
        return 0

    def draw_flow(
        self, player, from_rinshan: bool = False
    ) -> Tuple[int, Tile, int, Action]:
        """ An event flow that triggers a player to draw a tile and ends with
        that player discarding a tile.
        Args:
          player: the player to draw a tile
          from_rinshan: indicates this draw is from rinshan or not
        Return:
          state: -1 -> 流局
                  0 -> 繼續
                  1 -> somebody RON or TSUMO
          discard_tile: the discarded tile in this turn
                if Ron/Tsumo/流局 -> None
          discard_pos: the discarder's index
          action: the discarder's action in this turn
        """
        if player.jikaze == Jihai.TON:
            self.oya_draws += 1
        if self.oya_draws >= 2:
            self.first_turn = False

        if len(self.stack.playling_wall) == 0:
            self.is_haiteihai = True

        new_tile = self.stack.draw(from_rinshan)
        # Log Draw
        if from_rinshan:
            action = Action.DRAW_RINSHAN
        else:
            action = Action.DRAW
        self.logger.log(
            p_pos=player.seating_position,
            action=action,
            action_tile=new_tile,
        )

        new_tile.owner = player.seating_position
        player.tmp_furiten = False
        (action, naki), action_tile = player.action_with_new_tile(
            new_tile, self.first_turn, self.is_haiteihai
        )
        state = 0
        discard_pos = None
        if action == Action.NAKI:
            if naki in (Naki.ANKAN, Naki.CHAKAN):
                self.logger.log(

                    p_pos=player.seating_position,
                    action=action,
                    action_tile=new_tile,
                    naki_type=naki,
                    huro=player.tmp_huro,
                )
                player.action_with_naki(action)

                if kan_state := self.kan_flow(player, new_tile, naki):
                    return kan_state, action_tile, discard_pos
                if self.check_suukaikan(player.kabe):
                    return -1, action_tile, discard_pos
            state, action_tile, discard_pos, act = self.draw_flow(
                player, from_rinshan=True)

        elif action == Action.RYUUKYOKU:
            self.logger.log(
                p_pos=player.seating_position,
                action=action,
            )
            return -1, action_tile, discard_pos, action

        elif action == Action.TSUMO:
            self.logger.log(
                p_pos=player.seating_position,
                action=action,
                action_tile=new_tile,
            )
            return 1, action_tile, discard_pos, action

        # Discard the action tile
        if state == 0:
            self.logger.log(
                p_pos=player.seating_position,
                action=Action.DISCARD,
                action_tile=action_tile,
            )
            player.add_kawa(action_tile)
            discard_pos = player.seating_position

            if self.first_turn and player.jikaze == Jihai.PEI:
                if self.check_suufon_renda():
                    state = -1

        return state, action_tile, discard_pos, action

    def check_suukaikan(self, kabe: List[Huro]) -> bool:
        if len(self.stack.doras) >= 4:  # 場上已經有三或四個槓子
            kan_types = [Naki.CHAKAN, Naki.ANKAN, Naki.DAMINKAN]
            if len([huro for huro in kabe
                    if huro.naki_type in kan_types]) != 4:
                # Suukaikan: four KAN are called by different player
                return True  # 流局
        self.stack.add_dora_indicator()
        return False

    def check_suufon_renda(self) -> bool:
        wind_tiles = get_wind_tiles()
        first_discraded_tiles = []
        for p in self.players:
            first_discraded_tiles.append(p.kawa[0])
        all_equal = check_all_equal(first_discraded_tiles)

        if (first_discraded_tiles[0] in wind_tiles) and all_equal:
            return True
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
        kyotaku: int,
        atamahane: Optional[bool] = True,
    ):
        self.winners: List[Player] = []
        self.players: List[Player] = players
        self.oya_player: Player = self.get_oya_player()
        self.honba: int = honba
        self.kyotaku: int = kyotaku  # 供託
        self.bakaze: Jihai = bakaze
        self.tile_stack: Stack = Stack()
        self.logger: KyokuLogger = KyokuLogger()

        # Atamahane 「頭跳ね」 is more known as the "head bump" rule.
        # http://arcturus.su/wiki/Atamahane
        self.atamahane = atamahane

        # deal tiles to each player to produce their starting hands

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
    def bakaze(self, wind: Jihai) -> None:
        if not 4 <= wind.value <= 5:
            raise ValueError(
                "Bakaze should be 4 in Tonpuusen, should be 4 or 5 in Hanchan")
        self._bakaze = wind

    def get_oya_player(self):
        return next(filter(lambda p: p.jikaze == Jihai.TON, self.players))

    def deal(self) -> None:
        for player in self.players:
            player.hand = [self.tile_stack.draw() for _ in range(13)]
        return

    def calculate_yaku():
        ...

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
        turn = Turn(self.players, self.tile_stack, self.logger)
        state, discard_tile, discard_pos, act = turn.draw_flow(self.oya_player)
        # Tenhoo
        while state == 0:
            state, discard_tile, discard_pos, _ = turn.discard_flow(
                discard_tile, discard_pos)

        if state == -1:
            renchen = self.handle_ryuukyoku()
            if renchen:
                return True, self.kyotaku, self.honba + 1
            else:
                return False, self.kyotaku, 0

        else:
            tsumo = act == Action.TSUMO
            loser = None
            if discard_pos:
                loser = self.players[discard_pos]
            self.winners = [self.players[pos] for pos in turn.winners]
            han, fu = self.calculate_yaku()
            self.apply_points(han, fu, tsumo, loser)
            if self.oya_player in self.winners:
                # return next oya, kyotaku, honba
                return True, 0, self.honba + 1
            return False, 0, 0

    def handle_ryuukyoku(self):  # 流局
        tenpai_players = []
        if nagashi_player := self.check_nagashi_mangan():
            # 這裡採用流局滿貫不算和牌的規則，差別在本場和供託
            self.winners = [nagashi_player]
            self.apply_points(5, 20, True, None, True)
            tenpai_players = [nagashi_player]
        else:
            # 檢查流局是否聽牌
            noten_players = []
            for player in self.players:
                if check_tenpai(player.hand, player.kabe):
                    tenpai_players.append(player)
                else:
                    noten_players.append(player)
            self.apply_noten_points(tenpai_players, noten_players)

        return self.oya_player in tenpai_players

    def check_nagashi_mangan(self):  # 流し満貫
        """All the discards are terminals and/or honors.
        In addition, none of these discards were called by other players.
        http://arcturus.su/wiki/Nagashi_mangan
        Return: the nagashi mangan player, or None
        """
        honor_tiles, terminal_tiles = Tile.get_yaochuuhai()
        yaochuuhai = honor_tiles + terminal_tiles

        naki_tile_owners = set()
        for player in self.players:
            for huro in player.kabe:
                naki_tile_owners.add(huro.naki_tile.owner)

        for pos, player in enumerate(self.players):
            if pos not in naki_tile_owners and (all(
                    map(lambda idx: Tile.from_index(idx) in yaochuuhai,
                        player.furiten_tiles_idx))):
                return player
        return None

    def apply_noten_points(tenpai: List[Player], noten: List[Player]):
        if len(tenpai) == 1:
            for player in noten:
                player.points -= 1_000
            tenpai[0].points += 3_000
        elif len(tenpai) == 2:
            for player in noten:
                player.points -= 1_500
            for player in tenpai:
                player.points += 1_500
        elif len(tenpai) == 3:
            for player in tenpai:
                player.points += 1_000
            noten[0].points -= 3_000

    def calculate_base_points(self, han: int, fu: int) -> int:
        points = fu * 2**(han + 2)
        if points > 2_000:
            if han <= 5:  # mangan
                points = 2_000
            elif han == 6 or han == 7:
                points = 3_000
            elif han >= 8 and han <= 10:
                points = 4_000
            elif han == 11 or han == 12:
                points = 6_000
            elif han >= 13:
                points = 8_000  # 還要handle 雙倍役滿?
        return points

    def apply_points(self,
                     han: int,
                     fu: int,
                     tsumo: bool,
                     loser: Optional[Player] = None,
                     ryuukyoku: bool = False) -> None:
        pt = self.calculate_base_points(han, fu)
        discard_pos = loser.seating_position if loser else None
        winners_pos = [p.seating_position for p in self.winners]
        atamahane_winner_pos = get_atamahane_winner(discard_pos, winners_pos)
        atamahane_winner = self.players[atamahane_winner_pos]

        if tsumo:
            winner = self.winners[0]
            ignore = 0 if ryuukyoku else 1
            if winner == self.oya_player:
                winner.points += (
                    roundup(pt * 2) * 3 + 300 * self.honba * ignore)
                for i in range(4):
                    if self.players[i] != self.oya_player:
                        self.players[i].points -= (
                            roundup(pt * 2) + 100 * self.honba * ignore)
            else:  # 子家
                tmp_pt = 0
                for player in self.players:
                    if player == self.oya_player:
                        player.points -= (
                            roundup(pt * 2) + 100 * self.honba * ignore)
                        tmp_pt += (
                            roundup(pt * 2) + 100 * self.honba * ignore)
                    elif player != winner:
                        player.points -= (
                            roundup(pt) + 100 * self.honba * ignore)
                        tmp_pt += (
                            roundup(pt) + 100 * self.honba * ignore)
                winner.points += tmp_pt

        else:  # ron
            for winner in self.winners:
                if winner == self.oya_player:
                    winner.points += roundup(pt * 6)
                    loser.points -= roundup(pt * 6)
                else:  # 子家
                    winner.points += roundup(pt * 4)
                    loser.points -= roundup(pt * 4)
            atamahane_winner.points += 300 * self.honba
            loser.points -= 300 * self.honba

        if not ryuukyoku and self.kyotaku > 0:
            atamahane_winner.points += self.kyotaku * 1_000
        return
