import unittest
from unittest.mock import MagicMock

from mahjong.player import Player, Position
from mahjong.components import Stack, Tile, Action
from mahjong.kyoku import Turn


class TestTurnDrawFlow(unittest.TestCase):

    def setUp(self):
        self.player_1 = Player('player 1', Position.TON.value)
        self.player_2 = Player('player 2', Position.NAN.value)
        self.player_3 = Player('player 3', Position.SHAA.value)
        self.player_4 = Player('player 4', Position.PEI.value)
        self.players = [self.player_1, self.player_2,
                        self.player_3, self.player_4]
        self.tile_stack = Stack()

        for player in self.players:
            for i in range(13):
                player.hand[self.tile_stack.draw().index] += 1

        self.turn = Turn(self.players, self.tile_stack)

    def test_tsumo(self):
        self.player_1.action_with_new_tile = MagicMock(
            return_value=(Action.TSUMO, None))
        self.assertEqual(self.turn.draw_flow(self.player_1),
                         (self.player_1.seating_position, None))

    def test_ankan(self):
        self.player_1.action_with_new_tile = MagicMock()
        self.player_1.action_with_new_tile.side_effect = [
            (Action.ANKAN, None), (Action.NOACT, Tile(0, 1))]
        state, discard_tile = self.turn.draw_flow(self.player_1)
        self.assertEqual(state, 0)
        self.assertEqual(discard_tile, Tile(0, 1))
        self.assertEqual(self.player_1.kawa[0], Tile(0, 1))
        self.assertEqual(len(self.tile_stack.dora), 2)

    def test_chakan(self):
        self.player_1.action_with_new_tile = MagicMock()
        self.player_1.action_with_new_tile.side_effect = [
            (Action.CHAKAN, None), (Action.NOACT, Tile(0, 1))]
        state, discard_tile = self.turn.draw_flow(self.player_1)
        self.assertEqual(state, 0)
        self.assertEqual(discard_tile, Tile(0, 1))
        self.assertEqual(self.player_1.kawa[0], Tile(0, 1))
        self.assertEqual(len(self.tile_stack.dora), 2)

    def test_ankan_twice(self):
        self.player_1.action_with_new_tile = MagicMock()
        self.player_1.action_with_new_tile.side_effect = [
            (Action.ANKAN, None),
            (Action.ANKAN, None),
            (Action.NOACT, Tile(0, 1))]
        state, discard_tile = self.turn.draw_flow(self.player_1)
        self.assertEqual(state, 0)
        self.assertEqual(discard_tile, Tile(0, 1))
        self.assertEqual(self.player_1.kawa[0], Tile(0, 1))
        self.assertEqual(len(self.tile_stack.dora), 3)

    def test_suukaikan(self):
        # is declared when four quads are formed by different players.
        for _ in range(3):
            self.tile_stack.add_dora_indicator()
        self.player_1.action_with_new_tile = MagicMock()
        self.player_1.action_with_new_tile.side_effect = [
            (Action.ANKAN, None), (Action.NOACT, Tile(0, 1))]
        state, discard_tile = self.turn.draw_flow(self.player_1)
        self.assertEqual(state, -1)
        self.assertEqual(discard_tile, None)
        self.assertEqual(len(self.tile_stack.dora), 4)

    def test_suukantsu(self):
        ...

    def test_rinshan_kaihou(self):
        self.player_1.action_with_new_tile = MagicMock()
        self.player_1.action_with_new_tile.side_effect = [
            (Action.ANKAN, None),
            (Action.TSUMO, None)]
        state, discard_tile = self.turn.draw_flow(self.player_1)
        self.assertEqual(state, self.player_1.seating_position)
        self.assertEqual(discard_tile, None)


class TestTurnEnsembleActions(unittest.TestCase):

    def setUp(self):
        self.player_1 = Player('player 1', Position.TON.value)
        self.player_2 = Player('player 2', Position.NAN.value)
        self.player_3 = Player('player 3', Position.SHAA.value)
        self.player_4 = Player('player 4', Position.PEI.value)
        self.players = [self.player_1, self.player_2,
                        self.player_3, self.player_4]
        self.tile_stack = Stack()

        for player in self.players:
            for i in range(13):
                player.hand[self.tile_stack.draw().index] += 1

        self.turn = Turn(self.players, self.tile_stack)

    def test_all_noact(self):
        discard_player = self.player_1
        discard_tile = Tile(0, 1)
        self.player_2.action_with_discard_tile = MagicMock(
            return_value=Action.NOACT)
        self.player_3.action_with_discard_tile = MagicMock(
            return_value=Action.NOACT)
        self.player_4.action_with_discard_tile = MagicMock(
            return_value=Action.NOACT)
        pos, action = self.turn.ensemble_actions(
            discard_tile,
            discard_player.seating_position)
        self.assertEqual(pos, 2)
        self.assertEqual(action, Action.NOACT)

    def test_shimocha_chii(self):
        discard_player = self.player_1
        discard_tile = Tile(0, 1)
        self.player_2.action_with_discard_tile = MagicMock(
            return_value=Action.CHII)
        self.player_3.action_with_discard_tile = MagicMock(
            return_value=Action.NOACT)
        self.player_4.action_with_discard_tile = MagicMock(
            return_value=Action.NOACT)
        pos, action = self.turn.ensemble_actions(
            discard_tile,
            discard_player.seating_position)
        self.assertEqual(pos, 2)
        self.assertEqual(action, Action.CHII)

    def test_toimen_pon(self):
        discard_player = self.player_1
        discard_tile = Tile(0, 1)
        self.player_2.action_with_discard_tile = MagicMock(
            return_value=Action.CHII)
        self.player_3.action_with_discard_tile = MagicMock(
            return_value=Action.PON)
        self.player_4.action_with_discard_tile = MagicMock(
            return_value=Action.NOACT)
        pos, action = self.turn.ensemble_actions(
            discard_tile,
            discard_player.seating_position)
        self.assertEqual(pos, 3)
        self.assertEqual(action, Action.PON)

    def test_kamicha_pon(self):
        discard_player = self.player_1
        discard_tile = Tile(0, 1)
        self.player_2.action_with_discard_tile = MagicMock(
            return_value=Action.NOACT)
        self.player_3.action_with_discard_tile = MagicMock(
            return_value=Action.NOACT)
        self.player_4.action_with_discard_tile = MagicMock(
            return_value=Action.PON)
        pos, action = self.turn.ensemble_actions(
            discard_tile,
            discard_player.seating_position)
        self.assertEqual(pos, 4)
        self.assertEqual(action, Action.PON)

    def test_shimocha_ron(self):
        discard_player = self.player_1
        discard_tile = Tile(0, 1)
        self.player_2.action_with_discard_tile = MagicMock(
            return_value=Action.RON)
        self.player_3.action_with_discard_tile = MagicMock(
            return_value=Action.NOACT)
        self.player_4.action_with_discard_tile = MagicMock(
            return_value=Action.DAMINKAN)
        pos, action = self.turn.ensemble_actions(
            discard_tile,
            discard_player.seating_position)
        self.assertEqual(pos, 2)
        self.assertEqual(action, Action.RON)

    def test_kamicha_ron(self):
        discard_player = self.player_1
        discard_tile = Tile(0, 1)
        self.player_2.action_with_discard_tile = MagicMock(
            return_value=Action.CHII)
        self.player_3.action_with_discard_tile = MagicMock(
            return_value=Action.PON)
        self.player_4.action_with_discard_tile = MagicMock(
            return_value=Action.RON)
        pos, action = self.turn.ensemble_actions(
            discard_tile,
            discard_player.seating_position)
        self.assertEqual(pos, 4)
        self.assertEqual(action, Action.RON)


class TestTurnNakiFlow(unittest.TestCase):

    def setUp(self):
        self.player_1 = Player('player 1', Position.TON.value)
        self.player_2 = Player('player 2', Position.NAN.value)
        self.player_3 = Player('player 3', Position.SHAA.value)
        self.player_4 = Player('player 4', Position.PEI.value)
        self.players = [self.player_1, self.player_2,
                        self.player_3, self.player_4]
        self.tile_stack = Stack()

        for player in self.players:
            for i in range(13):
                player.hand[self.tile_stack.draw().index] += 1

        self.turn = Turn(self.players, self.tile_stack)

    def test_ron(self):
        state, discard_tile = self.turn.naki_flow(self.player_1, Action.RON)
        self.assertEqual(state, self.player_1.seating_position)
        self.assertEqual(discard_tile, None)

    def test_daminkan(self):
        self.player_1.action_with_naki = MagicMock(return_value=None)
        self.turn.draw_flow = MagicMock(return_value=(0, Tile(0, 1)))
        state, discard_tile = self.turn.naki_flow(
            self.player_1, Action.DAMINKAN)
        self.assertEqual(state, 0)
        self.assertEqual(discard_tile, Tile(0, 1))
        self.assertEqual(len(self.tile_stack.dora), 2)
        self.assertEqual(self.player_1.kawa[0], Tile(0, 1))

    def test_suukaikan(self):
        for _ in range(3):
            self.tile_stack.add_dora_indicator()
        self.player_1.action_with_naki = MagicMock(return_value=None)
        state, discard_tile = self.turn.naki_flow(
            self.player_1, Action.DAMINKAN)

        self.assertEqual(state, -1)
        self.assertEqual(discard_tile, None)
        self.assertEqual(len(self.tile_stack.dora), 4)

    def test_suukantsu(self):
        ...

    def test_chii(self):
        self.player_1.action_with_naki = MagicMock(return_value=None)
        self.player_1.discard_after_naki = MagicMock(return_value=Tile(0, 1))
        state, discard_tile = self.turn.naki_flow(
            self.player_1, Action.CHII)
        self.assertEqual(state, 0)
        self.assertEqual(discard_tile, Tile(0, 1))
        self.assertEqual(self.player_1.kawa[0], Tile(0, 1))


class TestTurnDiscardFlow(unittest.TestCase):

    def setUp(self):
        self.player_1 = Player('player 1', Position.TON.value)
        self.player_2 = Player('player 2', Position.NAN.value)
        self.player_3 = Player('player 3', Position.SHAA.value)
        self.player_4 = Player('player 4', Position.PEI.value)
        self.players = [self.player_1, self.player_2,
                        self.player_3, self.player_4]
        self.tile_stack = Stack()

        for player in self.players:
            for i in range(13):
                player.hand[self.tile_stack.draw().index] += 1

        self.turn = Turn(self.players, self.tile_stack)

    def test_all_noact(self):
        self.turn.ensemble_actions = MagicMock(return_value=(2, Action.NOACT))
        self.turn.draw_flow = MagicMock(return_value=(0, Tile(0, 1)))
        state, discard_tile = self.turn.discard_flow(
            Tile(0, 2),
            self.player_1.seating_position)
        self.assertEqual(state, 0)
        self.assertEqual(discard_tile, Tile(0, 1))

    def test_all_noact_then_tsumo(self):
        self.turn.ensemble_actions = MagicMock(return_value=(2, Action.NOACT))
        self.turn.draw_flow = MagicMock(return_value=(2, None))
        state, discard_tile = self.turn.discard_flow(
            Tile(0, 2),
            self.player_1.seating_position)
        self.assertEqual(state, 2)
        self.assertEqual(discard_tile, None)

    def test_call_naki(self):
        self.turn.ensemble_actions = MagicMock(return_value=(2, Action.CHII))
        self.turn.naki_flow = MagicMock(return_value=(0, Tile(0, 1)))
        state, discard_tile = self.turn.discard_flow(
            Tile(1, 1),
            self.player_1.seating_position)
        self.assertEqual(state, 0)
        self.assertEqual(discard_tile, Tile(0, 1))