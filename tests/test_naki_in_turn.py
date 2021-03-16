import unittest
from unittest.mock import MagicMock, patch
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
            Jihai.TON,
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
        # test remove_huro_tiles()
        self.assertEqual(self.players[1].hand[pon_tile.index], 0)
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
            Jihai.TON
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


class TestChii(unittest.TestCase):

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

    def test_chii(self):
        self.current_kyoku.deal()

        # change tile in hand to test chii
        chii_tile = Tile(Suit.MANZU.value, 5)
        chii_tile.owner = self.players[0].seating_position
        to_discard_tile = Tile(Suit.PINZU.value, 9)

        self.current_kyoku.players[0].hand = defaultdict(int)
        self.current_kyoku.players[0].hand[chii_tile.index] = 1
        self.current_kyoku.players[0].hand[Tile(2, 1).index] += 1
        self.current_kyoku.players[0].hand[Tile(2, 2).index] += 1
        self.current_kyoku.players[0].hand[Tile(2, 3).index] += 1
        self.current_kyoku.players[1].hand = defaultdict(int)
        self.current_kyoku.players[1].hand[chii_tile.index - 1] = 1
        self.current_kyoku.players[1].hand[chii_tile.index + 1] = 1
        self.current_kyoku.players[1].hand[to_discard_tile.index] = 1
        self.current_kyoku.players[1].hand[Tile(2, 2).index] += 2
        self.current_kyoku.players[1].hand[Tile(2, 3).index] += 1
        self.current_kyoku.players[1].hand[Tile(2, 4).index] += 1
        self.current_kyoku.players[2].hand = defaultdict(int)
        self.current_kyoku.players[2].hand[Tile(2, 5).index] += 2
        self.current_kyoku.players[2].hand[Tile(2, 6).index] += 1
        self.current_kyoku.players[2].hand[Tile(2, 7).index] += 1
        self.current_kyoku.players[3].hand = defaultdict(int)
        self.current_kyoku.players[3].hand[Tile(3, 7).index] += 2
        self.current_kyoku.players[3].hand[Tile(3, 8).index] += 1
        self.current_kyoku.players[3].hand[Tile(3, 9).index] += 1

        pyinput.inputNum = MagicMock(side_effect=[1, 0, 4])
        pyinput.inputChoice = MagicMock(return_value=1)

        turn = Turn(
            self.current_kyoku.players,
            self.current_kyoku.tile_stack,
            Jihai.TON,
            self.logger,
        )

        mock_draw_flow = MagicMock(
            return_value=(0, chii_tile, self.players[0].seating_position))
        state, discard_tile, discard_pos = mock_draw_flow(
            self.current_kyoku.oya_player)

        state, discard_tile, discard_pos, act = turn.discard_flow(
            discard_tile, discard_pos)

        chii_in_kabe = Huro(
            Naki.CHII,
            chii_tile,
            [chii_tile.prev_tile(), chii_tile, chii_tile.next_tile()]
        )

        self.assertEqual(state, 0)
        self.assertEqual(discard_tile, to_discard_tile)
        self.assertEqual(discard_pos, self.players[1].seating_position)
        self.assertEqual(
            chii_in_kabe.naki_type, self.players[1].kabe[0].naki_type)
        self.assertEqual(
            chii_in_kabe.naki_tile, self.players[1].kabe[0].naki_tile)
        # test remove_huro_tiles()
        self.assertEqual(self.players[1].hand[chii_tile.index - 1], 0)
        self.assertEqual(self.players[1].hand[chii_tile.index + 1], 0)
        self.assertEqual(chii_in_kabe.tiles, self.players[1].kabe[0].tiles)


class TestKan(unittest.TestCase):

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

    def test_daminkan(self):
        self.current_kyoku.deal()

        # change tile in hand to test pon
        kan_tile = Tile(Suit.JIHAI.value, Jihai.CHUN.value)
        kan_tile.owner = self.players[0].seating_position
        to_discard_tile = Tile(Suit.JIHAI.value, Jihai.HAKU.value)

        self.current_kyoku.players[0].hand = defaultdict(int)
        self.current_kyoku.players[0].hand[kan_tile.index] = 1
        self.current_kyoku.players[0].hand[Tile(2, 1).index] += 1
        self.current_kyoku.players[0].hand[Tile(2, 2).index] += 1
        self.current_kyoku.players[0].hand[Tile(2, 3).index] += 1
        self.current_kyoku.players[1].hand = defaultdict(int)
        self.current_kyoku.players[1].hand[kan_tile.index] = 3
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
        pyinput.inputChoice = MagicMock(return_value=3)

        turn = Turn(
            self.current_kyoku.players,
            self.current_kyoku.tile_stack,
            Jihai.TON,
            self.logger,
        )

        mock_draw_flow = MagicMock(
            return_value=(0, kan_tile, self.players[0].seating_position))
        state, discard_tile, discard_pos = mock_draw_flow(
            self.current_kyoku.oya_player)

        state, discard_tile, discard_pos, act = turn.discard_flow(
            discard_tile, discard_pos)

        kan_in_kabe = Huro(
            Naki.DAMINKAN,
            kan_tile,
            [kan_tile, kan_tile, kan_tile, kan_tile]
        )

        self.assertEqual(state, 0)
        self.assertEqual(discard_tile, to_discard_tile)
        self.assertEqual(discard_pos, self.players[1].seating_position)
        self.assertEqual(
            kan_in_kabe.naki_type, self.players[1].kabe[0].naki_type)
        self.assertEqual(
            kan_in_kabe.naki_tile, self.players[1].kabe[0].naki_tile)
        # test remove_huro_tiles()
        self.assertEqual(self.players[1].hand[kan_tile.index], 0)
        self.assertEqual(kan_in_kabe.tiles, self.players[1].kabe[0].tiles)

    def test_chakan(self):
        self.current_kyoku.deal()

        # change tile in hand to test chakan after pon
        pon_tile = Tile(Suit.JIHAI.value, Jihai.CHUN.value)
        pon_tile.owner = self.players[0].seating_position
        to_discard_tile = Tile(Suit.JIHAI.value, Jihai.HAKU.value)

        pon_in_kabe = Huro(
            Naki.PON, pon_tile, [pon_tile, pon_tile, pon_tile]
        )

        self.current_kyoku.players[0].hand = defaultdict(int)
        self.current_kyoku.players[0].hand[Tile(2, 1).index] += 2
        self.current_kyoku.players[0].hand[Tile(2, 2).index] += 1
        self.current_kyoku.players[0].hand[Tile(2, 3).index] += 1
        self.current_kyoku.players[1].hand = defaultdict(int)
        self.current_kyoku.players[1].hand[to_discard_tile.index] = 1
        self.current_kyoku.players[1].hand[Tile(2, 2).index] += 2
        self.current_kyoku.players[1].hand[Tile(2, 3).index] += 1
        self.current_kyoku.players[1].hand[Tile(2, 4).index] += 1
        self.current_kyoku.players[1].kabe.append(pon_in_kabe)
        self.current_kyoku.players[2].hand = defaultdict(int)
        self.current_kyoku.players[2].hand[Tile(2, 5).index] += 2
        self.current_kyoku.players[2].hand[Tile(2, 6).index] += 1
        self.current_kyoku.players[2].hand[Tile(2, 7).index] += 1
        self.current_kyoku.players[3].hand = defaultdict(int)
        self.current_kyoku.players[3].hand[Tile(2, 7).index] += 2
        self.current_kyoku.players[3].hand[Tile(2, 8).index] += 1
        self.current_kyoku.players[3].hand[Tile(2, 9).index] += 1

        pyinput.inputNum = MagicMock(side_effect=[1, 0, 0])
        pyinput.inputChoice = MagicMock(return_value=4)

        turn = Turn(
            self.current_kyoku.players,
            self.current_kyoku.tile_stack,
            Jihai.TON,
            self.logger,
        )

        mock_draw_flow = MagicMock(
            return_value=(0,
                          Tile(Suit.JIHAI.value, Jihai.TON.value),
                          self.players[0].seating_position))
        state, discard_tile, discard_pos = mock_draw_flow(
            self.current_kyoku.oya_player)

        chakan_tile = Tile(Suit.JIHAI.value, Jihai.CHUN.value)
        with patch('mahjong.components.Stack.draw') as mock_func:
            def f(from_rinshan):
                if from_rinshan:
                    return Tile(Suit.SOUZU.value, 9)
                else:
                    return chakan_tile
            mock_func.side_effect = f
            state, discard_tile, discard_pos, act = turn.discard_flow(
                discard_tile, discard_pos)

        kan_in_kabe = Huro(
            Naki.CHAKAN,
            chakan_tile,
            [pon_tile, pon_tile, pon_tile, pon_tile]
        )

        self.assertEqual(state, 0)
        self.assertEqual(discard_tile, to_discard_tile)
        self.assertEqual(discard_pos, self.players[1].seating_position)
        self.assertEqual(
            kan_in_kabe.naki_type, self.players[1].kabe[0].naki_type)
        self.assertEqual(
            kan_in_kabe.naki_tile, self.players[1].kabe[0].naki_tile)
        self.assertEqual(self.players[1].hand[pon_tile.index], 0)
        self.assertEqual(kan_in_kabe.tiles, self.players[1].kabe[0].tiles)

    def test_ankan(self):
        self.current_kyoku.deal()

        kan_tile = Tile(Suit.JIHAI.value, Jihai.CHUN.value)
        to_discard_tile = Tile(Suit.JIHAI.value, Jihai.HAKU.value)

        self.current_kyoku.players[0].hand = defaultdict(int)
        self.current_kyoku.players[0].hand[Tile(2, 1).index] += 2
        self.current_kyoku.players[0].hand[Tile(2, 2).index] += 1
        self.current_kyoku.players[0].hand[Tile(2, 3).index] += 1
        self.current_kyoku.players[1].hand = defaultdict(int)
        self.current_kyoku.players[1].hand[kan_tile.index] = 3
        self.current_kyoku.players[1].hand[to_discard_tile.index] = 1
        self.current_kyoku.players[1].hand[Tile(2, 2).index] += 2
        self.current_kyoku.players[1].hand[Tile(2, 3).index] += 1
        self.current_kyoku.players[1].hand[Tile(2, 4).index] += 1
        self.current_kyoku.players[2].hand = defaultdict(int)
        self.current_kyoku.players[2].hand[Tile(2, 5).index] += 2
        self.current_kyoku.players[2].hand[Tile(2, 6).index] += 1
        self.current_kyoku.players[2].hand[Tile(2, 7).index] += 1
        self.current_kyoku.players[3].hand = defaultdict(int)
        self.current_kyoku.players[3].hand[Tile(2, 7).index] += 2
        self.current_kyoku.players[3].hand[Tile(2, 8).index] += 1
        self.current_kyoku.players[3].hand[Tile(2, 9).index] += 1

        pyinput.inputNum = MagicMock(side_effect=[1, 0, 0])
        pyinput.inputChoice = MagicMock(return_value=5)

        turn = Turn(
            self.current_kyoku.players,
            self.current_kyoku.tile_stack,
            Jihai.TON,
            self.logger,
        )

        mock_draw_flow = MagicMock(
            return_value=(0,
                          Tile(Suit.JIHAI.value, Jihai.TON.value),
                          self.players[0].seating_position))
        state, discard_tile, discard_pos = mock_draw_flow(
            self.current_kyoku.oya_player)

        ankan_tile = kan_tile
        with patch('mahjong.components.Stack.draw') as mock_func:
            def f(from_rinshan):
                if from_rinshan:
                    return Tile(Suit.SOUZU.value, 9)
                else:
                    return ankan_tile
            mock_func.side_effect = f
            state, discard_tile, discard_pos, act = turn.discard_flow(
                discard_tile, discard_pos)

        kan_in_kabe = Huro(
            Naki.ANKAN,
            ankan_tile,
            [kan_tile, kan_tile, kan_tile, kan_tile]
        )

        self.assertEqual(state, 0)
        self.assertEqual(discard_tile, to_discard_tile)
        self.assertEqual(discard_pos, self.players[1].seating_position)
        self.assertEqual(
            kan_in_kabe.naki_type, self.players[1].kabe[0].naki_type)
        self.assertEqual(
            kan_in_kabe.naki_tile, self.players[1].kabe[0].naki_tile)
        self.assertEqual(self.players[1].hand[ankan_tile.index], 0)
        self.assertEqual(kan_in_kabe.tiles, self.players[1].kabe[0].tiles)
