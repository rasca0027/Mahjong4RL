import unittest
from collections import defaultdict
from unittest.mock import Mock, MagicMock, PropertyMock

from mahjong.player import Player
from mahjong.components import Stack, Tile, Action, Suit, Jihai, Naki, Huro
from mahjong.kyoku import Turn
from mahjong.event_logger import KyokuLogger


class TestTurnDrawFlow(unittest.TestCase):

    def setUp(self):
        self.player_1 = Player('player 1', 0)
        self.player_2 = Player('player 2', 1)
        self.player_3 = Player('player 3', 2)
        self.player_4 = Player('player 4', 3)
        self.players = [self.player_1, self.player_2,
                        self.player_3, self.player_4]
        self.tile_stack = Stack()
        self.logger = KyokuLogger()
        for player in self.players:
            for i in range(13):
                player.hand[self.tile_stack.draw().index] += 1

        self.turn = Turn(self.players, self.tile_stack, Jihai.TON, self.logger)

    def test_riichi(self):
        self.player_1.action_with_new_tile = MagicMock(
            return_value=((Action.RIICHI, Naki.NONE), None))
        self.assertEqual(
            self.turn.draw_flow(self.player_1),
            (0, None, 0, Action.RIICHI)
        )

    def test_tsumo(self):
        self.player_1.action_with_new_tile = MagicMock(
            return_value=((Action.TSUMO, Naki.NONE), None))
        self.assertEqual(
            self.turn.draw_flow(self.player_1),
            (1, None, None, Action.TSUMO)
        )

    def test_ankan(self):
        naki_tile = Tile(Suit.SOUZU.value, 5)
        naki_tile.owner = self.player_1.seating_position
        kan = Huro(Naki.ANKAN,
                   naki_tile,
                   [Tile(Suit.SOUZU.value, 5) for i in range(4)])

        self.player_1.tmp_huro = kan

        self.player_1.action_with_new_tile = MagicMock()
        self.player_1.action_with_new_tile.side_effect = [
            ((Action.NAKI, Naki.CHAKAN), None),
            ((Action.NOACT, Naki.NONE), Tile(0, 1))]
        self.turn.kan_flow = MagicMock(return_value=0)

        state, discard_tile, discard_pos, act = self.turn.draw_flow(
            self.player_1)
        self.assertEqual(state, 0)
        self.assertEqual(discard_tile, Tile(0, 1))
        self.assertEqual(discard_pos, 0)
        self.assertEqual(self.player_1.kawa[0], Tile(0, 1))
        self.assertEqual(len(self.tile_stack.doras), 2)

    def test_chakan(self):
        # change type from PON to KAN, what's tmp_huro in this case?
        naki_tile = Tile(Suit.SOUZU.value, 5)
        naki_tile.owner = self.player_1.seating_position
        kan = Huro(Naki.ANKAN,
                   naki_tile,
                   [Tile(Suit.SOUZU.value, 5) for i in range(4)])

        self.player_1.tmp_huro = kan

        self.player_1.action_with_new_tile = MagicMock()
        self.player_1.action_with_new_tile.side_effect = [
            ((Action.NAKI, Naki.CHAKAN), None),
            ((Action.NOACT, Naki.NONE), Tile(0, 1))]
        self.turn.kan_flow = MagicMock(return_value=0)
        state, discard_tile, discard_pos, act = self.turn.draw_flow(
            self.player_1)
        self.assertEqual(state, 0)
        self.assertEqual(discard_tile, Tile(0, 1))
        self.assertEqual(discard_pos, 0)
        self.assertEqual(self.player_1.kawa[0], Tile(0, 1))
        self.assertEqual(len(self.tile_stack.doras), 2)

    def test_chakan_chankan(self):
        naki_tile = Tile(Suit.SOUZU.value, 5)
        naki_tile.owner = self.player_1.seating_position
        kan = Huro(Naki.ANKAN,
                   naki_tile,
                   [Tile(Suit.SOUZU.value, 5) for i in range(4)])

        self.player_1.tmp_huro = kan

        self.player_1.action_with_new_tile = MagicMock()
        self.player_1.action_with_new_tile.side_effect = [
            ((Action.NAKI, Naki.CHAKAN), None),
            ((Action.NOACT, Naki.NONE), Tile(0, 1))]
        self.turn.kan_flow = MagicMock(return_value=1)
        state, discard_tile, discard_pos = self.turn.draw_flow(self.player_1)
        self.assertEqual(state, 1)
        self.assertEqual(discard_tile, None)
        self.assertEqual(discard_pos, None)

    def test_ankan_twice(self):
        naki_tile_1 = Tile(Suit.SOUZU.value, 5)
        naki_tile_1.owner = self.player_1.seating_position
        naki_tile_2 = Tile(Suit.SOUZU.value, 6)
        naki_tile_2.owner = self.player_1.seating_position
        kan_1 = Huro(Naki.ANKAN,
                     naki_tile_1,
                     [Tile(Suit.SOUZU.value, 5) for i in range(4)])
        kan_2 = Huro(Naki.ANKAN,
                     naki_tile_2,
                     [Tile(Suit.SOUZU.value, 6) for i in range(4)])

        self.player_1 = Mock()
        self.player_1.seating_position = 0
        self.player_1.get_shimocha = lambda: 1 % 4
        self.player_1.hand = defaultdict(int)
        self.player_1.kawa = []
        self.player_1.add_kawa = lambda tile: self.player_1.kawa.append(tile)
        p = PropertyMock(side_effect=[kan_1, kan_2])
        type(self.player_1).tmp_huro = p

        self.player_1.action_with_new_tile = MagicMock()
        self.player_1.action_with_new_tile.side_effect = [
            ((Action.NAKI, Naki.ANKAN), None),
            ((Action.NAKI, Naki.ANKAN), None),
            ((Action.NOACT, Naki.NONE), Tile(0, 1))]
        state, discard_tile, discard_pos, act = self.turn.draw_flow(
            self.player_1)
        self.assertEqual(state, 0)
        self.assertEqual(discard_tile, Tile(0, 1))
        self.assertEqual(discard_pos, 0)
        self.assertEqual(self.player_1.kawa[0], Tile(0, 1))
        self.assertEqual(len(self.tile_stack.doras), 3)

    def test_draw_flow_suukaikan(self):
        # is declared when four quads are formed by different players.
        for _ in range(3):
            self.tile_stack.add_dora_indicator()
        naki_tile = Tile(Suit.SOUZU.value, 5)
        naki_tile.owner = self.player_1.seating_position

        kan = Huro(Naki.ANKAN,
                   naki_tile,
                   [Tile(Suit.SOUZU.value, 5) for i in range(4)])
        self.player_1.action_with_new_tile = MagicMock()
        self.player_1.action_with_new_tile.side_effect = [
            ((Action.NAKI, Naki.ANKAN), None),
            ((Action.NOACT, Naki.NONE), Tile(0, 1))]
        self.player_1.action_with_naki = MagicMock(
            self.player_1.kabe.append(kan)
        )
        state, discard_tile, discard_pos, _ = self.turn.draw_flow(
            self.player_1)
        self.assertEqual(state, 0)
        self.assertEqual(discard_tile, Tile(0, 1))
        self.assertEqual(discard_pos, self.player_1.seating_position)
        self.assertEqual(len(self.tile_stack.doras), 5)
        self.assertEqual(self.turn.suukaikan, True)

    def test_draw_flow_suukantsu(self):
        for _ in range(3):
            self.tile_stack.add_dora_indicator()
        naki_tile_1 = Tile(Suit.SOUZU.value, 5)
        naki_tile_1.owner = self.player_1.seating_position
        naki_tile_2 = Tile(Suit.SOUZU.value, 6)
        naki_tile_2.owner = self.player_1.seating_position
        naki_tile_3 = Tile(Suit.SOUZU.value, 7)
        naki_tile_3.owner = self.player_1.seating_position
        naki_tile_4 = Tile(Suit.SOUZU.value, 8)
        naki_tile_4.owner = self.player_1.seating_position
        kan_1 = Huro(Naki.ANKAN,
                     naki_tile_1,
                     [Tile(Suit.SOUZU.value, 5) for i in range(4)])
        kan_2 = Huro(Naki.ANKAN,
                     naki_tile_2,
                     [Tile(Suit.SOUZU.value, 6) for i in range(4)])
        kan_3 = Huro(Naki.ANKAN,
                     naki_tile_3,
                     [Tile(Suit.SOUZU.value, 7) for i in range(4)])
        kan_4 = Huro(Naki.ANKAN,
                     naki_tile_4,
                     [Tile(Suit.SOUZU.value, 8) for i in range(4)])
        self.player_1.kabe.append(kan_1)
        self.player_1.kabe.append(kan_2)
        self.player_1.kabe.append(kan_3)
        self.player_1.action_with_new_tile = MagicMock()
        self.player_1.action_with_new_tile.side_effect = [
            ((Action.NAKI, Naki.ANKAN), None),
            ((Action.NOACT, Naki.NONE), Tile(0, 1))]
        self.player_1.action_with_naki = MagicMock()

        def m(_):
            self.player_1.kabe.append(kan_4)
        self.player_1.action_with_naki.side_effect = m
        state, discard_tile, discard_pos, act = self.turn.draw_flow(
            self.player_1)
        self.assertEqual(state, 0)
        self.assertEqual(discard_tile, Tile(0, 1))
        self.assertEqual(discard_pos, 0)
        self.assertEqual(len(self.tile_stack.doras), 5)

    def test_suukantsu_other_player(self):
        for _ in range(3):
            self.tile_stack.add_dora_indicator()
        naki_tile = Tile(Suit.SOUZU.value, 5)
        naki_tile.owner = self.player_1.seating_position
        kan = Huro(Naki.DAMINKAN,
                   naki_tile,
                   [Tile(Suit.SOUZU.value, 5) for i in range(4)])
        kabe = [kan]
        self.turn.check_suukaikan(kabe)
        self.assertEqual(len(self.tile_stack.doras), 5)
        self.assertEqual(self.turn.suukaikan, True)

    def test_suukaikan(self):
        for _ in range(3):
            self.tile_stack.add_dora_indicator()
        naki_tile = Tile(Suit.SOUZU.value, 5)
        naki_tile.owner = self.player_1.seating_position
        kan = Huro(Naki.DAMINKAN,
                   naki_tile,
                   [Tile(Suit.SOUZU.value, 5) for i in range(4)])
        kabe = [kan]
        self.turn.check_suukaikan(kabe)
        self.assertEqual(len(self.tile_stack.doras), 5)
        self.assertEqual(self.turn.suukaikan, True)

    def test_suukantsu(self):
        for _ in range(3):
            self.tile_stack.add_dora_indicator()
        naki_tile_1 = Tile(Suit.SOUZU.value, 5)
        naki_tile_1.owner = self.player_1.seating_position
        naki_tile_2 = Tile(Suit.SOUZU.value, 6)
        naki_tile_2.owner = self.player_1.seating_position
        naki_tile_3 = Tile(Suit.SOUZU.value, 7)
        naki_tile_3.owner = self.player_1.seating_position
        naki_tile_4 = Tile(Suit.SOUZU.value, 8)
        naki_tile_4.owner = self.player_1.seating_position
        kan_1 = Huro(Naki.ANKAN,
                     naki_tile_1,
                     [Tile(Suit.SOUZU.value, 5) for i in range(4)])
        kan_2 = Huro(Naki.ANKAN,
                     naki_tile_2,
                     [Tile(Suit.SOUZU.value, 6) for i in range(4)])
        kan_3 = Huro(Naki.ANKAN,
                     naki_tile_3,
                     [Tile(Suit.SOUZU.value, 7) for i in range(4)])
        kan_4 = Huro(Naki.ANKAN,
                     naki_tile_4,
                     [Tile(Suit.SOUZU.value, 8) for i in range(4)])
        kabe = [kan_1, kan_2, kan_3, kan_4]
        self.turn.check_suukaikan(kabe)
        self.assertEqual(len(self.tile_stack.doras), 5)
        self.assertEqual(self.turn.suukaikan, False)

    def test_no_suukaikan(self):
        self.tile_stack.add_dora_indicator()
        naki_tile = Tile(Suit.SOUZU.value, 5)
        naki_tile.owner = self.player_1.seating_position
        kan = Huro(Naki.ANKAN,
                   naki_tile,
                   [Tile(Suit.SOUZU.value, 5) for i in range(4)])
        kabe = [kan]
        self.turn.check_suukaikan(kabe)
        self.assertEqual(self.turn.suukaikan, False)

    def test_rinshan_kaihou(self):
        naki_tile = Tile(Suit.SOUZU.value, 5)
        naki_tile.owner = self.player_1.seating_position
        kan = Huro(Naki.ANKAN,
                   naki_tile,
                   [Tile(Suit.SOUZU.value, 5) for i in range(4)])

        self.player_1.tmp_huro = kan
        self.player_1.action_with_new_tile = MagicMock()
        self.player_1.action_with_new_tile.side_effect = [
            ((Action.NAKI, Naki.ANKAN), None),
            ((Action.TSUMO, Naki.NONE), None)]
        state, discard_tile, discard_pos, act = self.turn.draw_flow(
            self.player_1)
        self.assertEqual(state, 1)
        self.assertEqual(discard_tile, None)
        self.assertEqual(discard_pos, None)

    def test_suufon_renda(self):
        tile_ton = Tile(Suit.JIHAI.value, Jihai.TON.value)
        self.player_1.add_kawa(tile_ton)
        self.player_2.add_kawa(tile_ton)
        self.player_3.add_kawa(tile_ton)
        self.player_4.add_kawa(tile_ton)

        self.assertEqual(self.turn.check_suufon_renda(), True)

    def test_suufon_renda_counter_example(self):
        tile_ton = Tile(Suit.JIHAI.value, Jihai.TON.value)
        tile_nan = Tile(Suit.JIHAI.value, Jihai.NAN.value)
        self.player_1.add_kawa(tile_nan)
        self.player_2.add_kawa(tile_ton)
        self.player_3.add_kawa(tile_ton)
        self.player_4.add_kawa(tile_ton)

        self.assertEqual(self.turn.check_suufon_renda(), False)


class TestTurnEnsembleActions(unittest.TestCase):

    def setUp(self):
        self.player_1 = Player('player 1', 0)
        self.player_2 = Player('player 2', 1)
        self.player_3 = Player('player 3', 2)
        self.player_4 = Player('player 4', 3)
        self.players = [self.player_1, self.player_2,
                        self.player_3, self.player_4]
        self.tile_stack = Stack()
        self.logger = KyokuLogger()
        for player in self.players:
            for i in range(13):
                player.hand[self.tile_stack.draw().index] += 1

        self.turn = Turn(self.players, self.tile_stack, Jihai.TON, self.logger)

    def test_all_noact(self):
        discard_player = self.player_1
        discard_tile = Tile(0, 1)
        self.player_2.action_with_discard_tile = MagicMock(
            return_value=(Action.NOACT, Naki.NONE))
        self.player_3.action_with_discard_tile = MagicMock(
            return_value=(Action.NOACT, Naki.NONE))
        self.player_4.action_with_discard_tile = MagicMock(
            return_value=(Action.NOACT, Naki.NONE))
        pos, (action, naki) = self.turn.ensemble_actions(
            discard_tile,
            discard_player.seating_position)
        self.assertEqual(pos, 1)
        self.assertEqual(action, Action.NOACT)
        self.assertEqual(naki, Naki.NONE)

    def test_shimocha_chii(self):
        discard_player = self.player_1
        discard_tile = Tile(0, 1)
        self.player_2.action_with_discard_tile = MagicMock(
            return_value=(Action.NAKI, Naki.CHII))
        self.player_3.action_with_discard_tile = MagicMock(
            return_value=(Action.NOACT, Naki.NONE))
        self.player_4.action_with_discard_tile = MagicMock(
            return_value=(Action.NOACT, Naki.NONE))
        pos, (action, naki) = self.turn.ensemble_actions(
            discard_tile,
            discard_player.seating_position)
        self.assertEqual(pos, 1)
        self.assertEqual(action, Action.NAKI)
        self.assertEqual(naki, Naki.CHII)

    def test_toimen_pon(self):
        discard_player = self.player_1
        discard_tile = Tile(0, 1)
        self.player_2.action_with_discard_tile = MagicMock(
            return_value=(Action.NAKI, Naki.CHII))
        self.player_3.action_with_discard_tile = MagicMock(
            return_value=(Action.NAKI, Naki.PON))
        self.player_4.action_with_discard_tile = MagicMock(
            return_value=(Action.NOACT, Naki.NONE))
        pos, (action, naki) = self.turn.ensemble_actions(
            discard_tile,
            discard_player.seating_position)
        self.assertEqual(pos, 2)
        self.assertEqual(action, Action.NAKI)
        self.assertEqual(naki, Naki.PON)

    def test_kamicha_pon(self):
        discard_player = self.player_1
        discard_tile = Tile(0, 1)
        self.player_2.action_with_discard_tile = MagicMock(
            return_value=(Action.NOACT, Naki.NONE))
        self.player_3.action_with_discard_tile = MagicMock(
            return_value=(Action.NOACT, Naki.NONE))
        self.player_4.action_with_discard_tile = MagicMock(
            return_value=(Action.NAKI, Naki.PON))
        pos, (action, naki) = self.turn.ensemble_actions(
            discard_tile,
            discard_player.seating_position)
        self.assertEqual(pos, 3)
        self.assertEqual(action, Action.NAKI)
        self.assertEqual(naki, Naki.PON)

    def test_shimocha_ron(self):
        discard_player = self.player_1
        discard_tile = Tile(0, 1)
        self.player_2.action_with_discard_tile = MagicMock(
            return_value=(Action.RON, Naki.NONE))
        self.player_3.action_with_discard_tile = MagicMock(
            return_value=(Action.NOACT, Naki.NONE))
        self.player_4.action_with_discard_tile = MagicMock(
            return_value=(Action.NOACT, Naki.DAMINKAN))
        pos, (action, naki) = self.turn.ensemble_actions(
            discard_tile,
            discard_player.seating_position)
        self.assertEqual(pos, 1)
        self.assertEqual(action, Action.RON)
        self.assertEqual(naki, Naki.NONE)

    def test_kamicha_ron(self):
        discard_player = self.player_1
        discard_tile = Tile(0, 1)
        self.player_2.action_with_discard_tile = MagicMock(
            return_value=(Action.NAKI, Naki.CHII))
        self.player_3.action_with_discard_tile = MagicMock(
            return_value=(Action.NAKI, Naki.PON))
        self.player_4.action_with_discard_tile = MagicMock(
            return_value=(Action.RON, Naki.NONE))
        pos, (action, naki) = self.turn.ensemble_actions(
            discard_tile,
            discard_player.seating_position)
        self.assertEqual(pos, 3)
        self.assertEqual(action, Action.RON)
        self.assertEqual(naki, Naki.NONE)

    def test_multiple_winners(self):
        discard_player = self.player_1
        discard_tile = Tile(0, 1)
        self.turn.atamahane = False
        self.player_2.action_with_discard_tile = MagicMock(
            return_value=(Action.NOACT, Naki.NONE))
        self.player_3.action_with_discard_tile = MagicMock(
            return_value=(Action.RON, Naki.NONE))
        self.player_4.action_with_discard_tile = MagicMock(
            return_value=(Action.RON, Naki.NONE))

        pos, (action, naki) = self.turn.ensemble_actions(
            discard_tile,
            discard_player.seating_position)
        self.assertEqual(pos, 2)
        self.assertEqual(action, Action.RON)
        self.assertEqual(naki, Naki.NONE)
        self.assertEqual(self.turn.winners_pos, [2, 3])


class TestTurnKanFlow(unittest.TestCase):

    def setUp(self):
        self.player_1 = Player('player 1', 0)
        self.player_2 = Player('player 2', 1)
        self.player_3 = Player('player 3', 2)
        self.player_4 = Player('player 4', 3)
        self.players = [self.player_1, self.player_2,
                        self.player_3, self.player_4]
        self.tile_stack = Stack()
        self.logger = KyokuLogger()

        for player in self.players:
            for i in range(13):
                player.hand[self.tile_stack.draw().index] += 1

        self.turn = Turn(self.players, self.tile_stack, Jihai.TON, self.logger)

    def test_kan_flow_no_act(self):
        kan_player = self.player_1
        kan_tile = Tile(0, 1)
        kan_type = Naki.CHAKAN
        self.player_2.action_with_chakan = MagicMock(return_value=Action.NOACT)
        self.player_3.action_with_chakan = MagicMock(return_value=Action.NOACT)
        self.player_4.action_with_chakan = MagicMock(return_value=Action.NOACT)

        state = self.turn.kan_flow(kan_player, kan_tile, kan_type)
        self.assertEqual(state, 0)

    def test_kan_flow_chakan(self):
        kan_player = self.player_1
        kan_tile = Tile(0, 1)
        kan_type = Naki.CHAKAN
        self.player_2.action_with_chakan = MagicMock(return_value=Action.RON)
        self.player_3.action_with_chakan = MagicMock(return_value=Action.NOACT)
        self.player_4.action_with_chakan = MagicMock(return_value=Action.RON)

        state, t, pos, act = self.turn.kan_flow(kan_player, kan_tile, kan_type)
        self.assertEqual(state, 1)
        self.assertEqual(self.turn.winners_pos, [1, 3])


class TestTurnNakiFlow(unittest.TestCase):

    def setUp(self):
        self.player_1 = Player('player 1', 0)
        self.player_2 = Player('player 2', 1)
        self.player_3 = Player('player 3', 2)
        self.player_4 = Player('player 4', 3)
        self.players = [self.player_1, self.player_2,
                        self.player_3, self.player_4]
        self.tile_stack = Stack()
        self.logger = KyokuLogger()
        for player in self.players:
            for i in range(13):
                player.hand[self.tile_stack.draw().index] += 1

        self.turn = Turn(self.players, self.tile_stack, Jihai.TON, self.logger)

    def test_daminkan(self):
        self.player_1.action_with_naki = MagicMock(return_value=None)
        self.turn.draw_flow = MagicMock(return_value=(0, Tile(0, 1),
                                        0,
                                        Action.NAKI))
        state, discard_tile, discard_pos, act = self.turn.naki_flow(
            self.player_1, Naki.DAMINKAN)
        self.assertEqual(state, 0)
        self.assertEqual(discard_tile, Tile(0, 1))
        self.assertEqual(discard_pos, 0)
        self.assertEqual(len(self.tile_stack.doras), 2)

    def test_suukaikan(self):
        for _ in range(3):
            self.tile_stack.add_dora_indicator()
        self.player_1.action_with_naki = MagicMock(return_value=None)
        self.turn.draw_flow = MagicMock(
            return_value=(0, Tile(0, 1), 0, Action.NOACT))
        state, discard_tile, pos, act = self.turn.naki_flow(
            self.player_1, Naki.DAMINKAN)

        self.assertEqual(state, 0)
        self.assertEqual(discard_tile, Tile(0, 1))
        self.assertEqual(self.turn.suukaikan, True)
        self.assertEqual(len(self.tile_stack.doras), 5)

    def test_suukantsu(self):
        for _ in range(3):
            self.tile_stack.add_dora_indicator()
        naki_tile_1 = Tile(Suit.SOUZU.value, 5)
        naki_tile_1.owner = self.player_1.seating_position
        naki_tile_2 = Tile(Suit.SOUZU.value, 6)
        naki_tile_2.owner = self.player_1.seating_position
        naki_tile_3 = Tile(Suit.SOUZU.value, 7)
        naki_tile_3.owner = self.player_1.seating_position
        naki_tile_4 = Tile(Suit.SOUZU.value, 8)
        naki_tile_4.owner = self.player_1.seating_position
        kan_1 = Huro(Naki.ANKAN,
                     naki_tile_1,
                     [Tile(Suit.SOUZU.value, 5) for i in range(4)])
        kan_2 = Huro(Naki.ANKAN,
                     naki_tile_2,
                     [Tile(Suit.SOUZU.value, 6) for i in range(4)])
        kan_3 = Huro(Naki.ANKAN,
                     naki_tile_3,
                     [Tile(Suit.SOUZU.value, 7) for i in range(4)])
        kan_4 = Huro(Naki.ANKAN,
                     naki_tile_4,
                     [Tile(Suit.SOUZU.value, 8) for i in range(4)])
        self.player_1.kabe.append(kan_1)
        self.player_1.kabe.append(kan_2)
        self.player_1.kabe.append(kan_3)
        self.player_1.action_with_naki = MagicMock(
            self.player_1.kabe.append(kan_4))
        self.turn.draw_flow = MagicMock(return_value=(0, Tile(0, 1),
                                        0,
                                        Action.NAKI))
        state, discard_tile, discard_pos, act = self.turn.naki_flow(
            self.player_1, Naki.DAMINKAN)
        self.assertEqual(state, 0)
        self.assertEqual(discard_tile, Tile(0, 1))
        self.assertEqual(discard_pos, 0)
        self.assertEqual(len(self.tile_stack.doras), 5)

    def test_chii(self):
        self.player_1.action_with_naki = MagicMock(return_value=None)
        self.player_1.discard_after_naki = MagicMock(return_value=Tile(0, 1))
        state, discard_tile, discard_pos, act = self.turn.naki_flow(
            self.player_1, Naki.CHII)
        self.assertEqual(state, 0)
        self.assertEqual(discard_tile, Tile(0, 1))
        self.assertEqual(discard_pos, 0)


class TestTurnDiscardFlow(unittest.TestCase):

    def setUp(self):
        self.player_1 = Player('player 1', 0)
        self.player_2 = Player('player 2', 1)
        self.player_3 = Player('player 3', 2)
        self.player_4 = Player('player 4', 3)
        self.players = [self.player_1, self.player_2,
                        self.player_3, self.player_4]
        self.tile_stack = Stack()
        self.logger = KyokuLogger()

        for player in self.players:
            for i in range(13):
                player.hand[self.tile_stack.draw().index] += 1

        self.turn = Turn(self.players, self.tile_stack, Jihai.TON, self.logger)

    def test_all_noact(self):
        self.turn.ensemble_actions = MagicMock(
            return_value=(2, (Action.NOACT, Naki.NONE)))
        self.turn.draw_flow = MagicMock(return_value=(
            0, Tile(0, 1), 0, Action.NOACT))
        state, discard_tile, discard_pos, act = self.turn.discard_flow(
            Tile(0, 2),
            self.player_1.seating_position)
        self.assertEqual(state, 0)
        self.assertEqual(discard_tile, Tile(0, 1))
        self.assertEqual(discard_pos, 0)

    def test_all_noact_then_tsumo(self):
        self.turn.ensemble_actions = MagicMock(
            return_value=(2, (Action.NOACT, Naki.NONE)))
        self.turn.draw_flow = MagicMock(return_value=(
            1, None, None, Action.TSUMO))
        state, discard_tile, discard_pos, act = self.turn.discard_flow(
            Tile(0, 2),
            self.player_1.seating_position)
        self.assertEqual(state, 1)
        self.assertEqual(discard_tile, None)
        self.assertEqual(discard_pos, None)

    def test_call_naki(self):
        self.turn.ensemble_actions = MagicMock(
            return_value=(2, (Action.NAKI, Naki.CHII)))
        self.turn.naki_flow = MagicMock(return_value=(
            0, Tile(0, 1), 2, Action.NAKI))
        state, discard_tile, discard_pos, act = self.turn.discard_flow(
            Tile(1, 1),
            self.player_1.seating_position)
        self.assertEqual(state, 0)
        self.assertEqual(discard_tile, Tile(0, 1))
        self.assertEqual(discard_pos, 2)

    def test_ron(self):
        self.turn.ensemble_actions = MagicMock(
            return_value=(2, (Action.RON, Naki.NONE)))
        state, discard_tile, discard_pos, act = self.turn.discard_flow(
            Tile(1, 1),
            self.player_1.seating_position)
        self.assertEqual(state, 1)
        self.assertEqual(discard_tile, None)
        self.assertEqual(discard_pos, 0)

    def test_normal_ryuukyoku(self):
        self.tile_stack.playing_wall = self.tile_stack.playing_wall[-1:]
        self.player_1.action_with_new_tile = MagicMock(
            return_value=((Action.NOACT, Naki.NONE), Tile(0, 1)))
        _, action_tile, discard_pos, _ = self.turn.draw_flow(self.player_1)
        self.assertEqual(
            self.turn.discard_flow(action_tile, discard_pos),
            (-1, action_tile, discard_pos, Action.NOACT)
        )
