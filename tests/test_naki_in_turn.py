import unittest
from unittest.mock import MagicMock
from collections import defaultdict

import pyinputplus as pyinput

from mahjong.kyoku import Kyoku, Turn
from mahjong.player import Player
from mahjong.components import Naki, Action, Suit, Tile, Jihai, Huro
from mahjong.event_logger import KyokuLogger


class TestPon(unittest.TestCase):

    def setUp(self):
        player_names = ['Kelly', 'Leo', 'Ball', 'Hao']
        self.bakaze = Jihai.TON
        self.kyoku_num = 1  # e.g.東1局
        self.players = self.get_init_players(player_names)
        self.current_kyoku = Kyoku(self.players)
        self.logger = KyokuLogger()

    def get_init_players(self, player_names):
        players = []
        for i, name in enumerate(player_names):
            players.append(Player(name, i))
        return players

    def test_pon(self):
        self.current_kyoku.deal()

        # change tile in hand to test pon
        pon_tile = Tile(Suit.JIHAI.value, Jihai.CHUN.value)
        pon_tile.owner = self.players[0].seating_position
        to_discard_tile = Tile(Suit.JIHAI.value, Jihai.HAKU.value)

        self.current_kyoku.players[0].hand = defaultdict(int)
        self.current_kyoku.players[0].hand[pon_tile.index] = 1
        self.current_kyoku.players[0].hand[Tile(2, 1).index] += 1
        self.current_kyoku.players[0].hand[Tile(2, 2).index] += 1
        self.current_kyoku.players[0].hand[Tile(2, 3).index] += 1
        self.current_kyoku.players[1].hand = defaultdict(int)
        self.current_kyoku.players[1].hand[pon_tile.index] = 2
        self.current_kyoku.players[1].hand[to_discard_tile.index] = 1
        self.current_kyoku.players[1].hand[Tile(2, 2).index] += 1
        self.current_kyoku.players[1].hand[Tile(2, 3).index] += 1
        self.current_kyoku.players[1].hand[Tile(2, 4).index] += 1
        self.current_kyoku.players[2].hand = defaultdict(int)
        self.current_kyoku.players[2].hand[Tile(2, 5).index] += 1
        self.current_kyoku.players[2].hand[Tile(2, 6).index] += 1
        self.current_kyoku.players[2].hand[Tile(2, 7).index] += 1
        self.current_kyoku.players[3].hand = defaultdict(int)
        self.current_kyoku.players[3].hand[Tile(2, 7).index] += 1
        self.current_kyoku.players[3].hand[Tile(2, 8).index] += 1
        self.current_kyoku.players[3].hand[Tile(2, 9).index] += 1

        pyinput.inputNum = MagicMock(side_effect=[1, 0, 0])
        pyinput.inputChoice = MagicMock(return_value=2)

        turn = Turn(
            self.current_kyoku.players,
            self.current_kyoku.tile_stack,
            self.logger,
        )

        mock_draw_flow = MagicMock(
            return_value=(0, pon_tile, self.players[0].seating_position))
        state, discard_tile, discard_pos = mock_draw_flow(
            self.current_kyoku.oya_player)

        state, discard_tile, discard_pos, act = turn.discard_flow(
            discard_tile, discard_pos)

        pon_in_kabe = Huro(
            Naki.PON, pon_tile, [pon_tile, pon_tile, pon_tile]
        )

        # Raw input: 1, 2, 0, 0

        self.assertEqual(state, 0)
        self.assertEqual(discard_tile, to_discard_tile)
        self.assertEqual(discard_pos, self.players[1].seating_position)
        self.assertEqual(
            pon_in_kabe.naki_type, self.players[1].kabe[0].naki_type)
        self.assertEqual(
            pon_in_kabe.naki_tile, self.players[1].kabe[0].naki_tile)
        self.assertEqual(pon_in_kabe.tiles, self.players[1].kabe[0].tiles)

    def test_no_haiteihai_pon(self):
        self.current_kyoku.deal()

        # change tile in hand to test pon
        pon_tile = Tile(Suit.JIHAI.value, Jihai.CHUN.value)
        pon_tile.owner = self.players[0].seating_position

        self.current_kyoku.players[0].hand = defaultdict(int)
        self.current_kyoku.players[0].hand[pon_tile.index] = 1
        self.current_kyoku.players[0].hand[Tile(2, 1).index] += 1
        self.current_kyoku.players[0].hand[Tile(2, 2).index] += 1
        self.current_kyoku.players[0].hand[Tile(2, 3).index] += 2
        self.current_kyoku.players[1].hand = defaultdict(int)
        self.current_kyoku.players[1].hand[pon_tile.index] = 2
        self.current_kyoku.players[1].hand[Tile(2, 2).index] += 1
        self.current_kyoku.players[1].hand[Tile(2, 3).index] += 1
        self.current_kyoku.players[1].hand[Tile(2, 4).index] += 2
        self.current_kyoku.players[2].hand = defaultdict(int)
        self.current_kyoku.players[2].hand[Tile(2, 5).index] += 1
        self.current_kyoku.players[2].hand[Tile(2, 6).index] += 1
        self.current_kyoku.players[2].hand[Tile(2, 7).index] += 2
        self.current_kyoku.players[3].hand = defaultdict(int)
        self.current_kyoku.players[3].hand[Tile(2, 7).index] += 1
        self.current_kyoku.players[3].hand[Tile(2, 8).index] += 1
        self.current_kyoku.players[3].hand[Tile(2, 9).index] += 2

        # pyinput.inputNum = MagicMock(side_effect=[1, 0, 0])
        # pyinput.inputChoice = MagicMock(return_value=2)

        turn = Turn(
            self.current_kyoku.players,
            self.current_kyoku.tile_stack,
            self.logger,
        )

        mock_draw_flow = MagicMock(
            return_value=(0, pon_tile, self.players[0].seating_position))
        state, discard_tile, discard_pos = mock_draw_flow(
            self.current_kyoku.oya_player)

        turn.stack.playing_wall = []

        state, discard_tile, discard_pos, act = turn.discard_flow(
            discard_tile, discard_pos)

        self.assertEqual(state, -1)
        self.assertEqual(discard_tile, pon_tile)
        self.assertEqual(discard_pos, self.players[0].seating_position)
        self.assertEqual(act, Action.NOACT)
