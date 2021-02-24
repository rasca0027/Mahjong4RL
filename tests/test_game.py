import unittest
from unittest.mock import patch

from mahjong.game import Game
from mahjong.components import Jihai


class TestGame(unittest.TestCase):

    def setUp(self):
        names = ['Kelly', 'Leo', 'Ball', 'Hoa']
        self.game = Game(names, 'config_test.json')
        # self.game.current_kyoku = MagicMock()

    def test_init(self):
        self.assertEqual(self.game.players[0].name, 'Kelly')
        self.assertEqual(self.game.players[0].jikaze, Jihai.TON)
        self.assertEqual(self.game.players[1].name, 'Leo')
        self.assertEqual(self.game.players[1].jikaze, Jihai.NAN)
        self.assertEqual(self.game.players[2].name, 'Ball')
        self.assertEqual(self.game.players[2].jikaze, Jihai.SHAA)
        self.assertEqual(self.game.players[3].name, 'Hoa')
        self.assertEqual(self.game.players[3].jikaze, Jihai.PEI)
        self.assertEqual(self.game.bakaze, Jihai.TON)

    def test_start_game(self):
        ...

    def test_tobu(self):
        with patch('mahjong.kyoku.Kyoku.start') as mock_func:
            def f():
                self.game.players[0].points = -2_500
                return False, 0, 0
            mock_func.side_effect = f
            self.game.start_game()
        mock_func.assert_called()

    def test_complete_game(self):
        ...

    def test_ryuukyoku(self):
        ...
