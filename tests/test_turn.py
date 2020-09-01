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
        self.assertEqual(self.turn.draw_flow(self.player_1), (1, None))

    def test_ankan(self):
        self.player_1.action_with_new_tile = MagicMock()
        self.player_1.action_with_new_tile.side_effect = [
            (Action.ANKAN, None), (Action.NOACT, Tile(0, 1))]
        self.state, self.discard_tile = self.turn.draw_flow(self.player_1)
        self.assertEqual(self.state, 0)
        self.assertEqual(self.discard_tile, Tile(0, 1))
        self.assertEqual(self.player_1.kawa[0], Tile(0, 1))
        self.assertEqual(len(self.tile_stack.dora), 2)

    def test_chakan(self):
        self.player_1.action_with_new_tile = MagicMock()
        self.player_1.action_with_new_tile.side_effect = [
            (Action.CHAKAN, None), (Action.NOACT, Tile(0, 1))]
        self.state, self.discard_tile = self.turn.draw_flow(self.player_1)
        self.assertEqual(self.state, 0)
        self.assertEqual(self.discard_tile, Tile(0, 1))
        self.assertEqual(self.player_1.kawa[0], Tile(0, 1))
        self.assertEqual(len(self.tile_stack.dora), 2)

    def test_ankan_twice(self):
        self.player_1.action_with_new_tile = MagicMock()
        self.player_1.action_with_new_tile.side_effect = [
            (Action.ANKAN, None),
            (Action.ANKAN, None),
            (Action.NOACT, Tile(0, 1))]
        self.state, self.discard_tile = self.turn.draw_flow(self.player_1)
        self.assertEqual(self.state, 0)
        self.assertEqual(self.discard_tile, Tile(0, 1))
        self.assertEqual(self.player_1.kawa[0], Tile(0, 1))
        self.assertEqual(len(self.tile_stack.dora), 3)

    def test_suukaikan(self):
        # is declared when four quads are formed by different players.
        for _ in range(3):
            self.tile_stack.add_dora_indicator()
        self.player_1.action_with_new_tile = MagicMock()
        self.player_1.action_with_new_tile.side_effect = [
            (Action.ANKAN, None), (Action.NOACT, Tile(0, 1))]
        self.state, self.discard_tile = self.turn.draw_flow(self.player_1)
        self.assertEqual(self.state, -1)
        self.assertEqual(self.discard_tile, None)
        self.assertEqual(len(self.tile_stack.dora), 4)
