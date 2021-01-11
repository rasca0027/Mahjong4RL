import unittest

from mahjong.components import Jihai
from mahjong.kyoku import Kyoku
from mahjong.player import Player


class TestPoints(unittest.TestCase):

    def setUp(self):

        self.player_1 = Player('player 1', 0)
        self.player_2 = Player('player 2', 1)
        self.player_3 = Player('player 3', 2)
        self.player_4 = Player('player 4', 3)
        players = [self.player_1, self.player_2, self.player_3, self.player_4]
        self.kyoku = Kyoku(players, 0, Jihai.TON, 0)

    def test_oya_tsumo(self):
        self.kyoku.winners = [self.player_1]
        self.kyoku.apply_points(1, 30, True)
        self.assertEqual(self.player_1.points, 26_500)
        self.assertEqual(self.player_2.points, 24_500)
        self.assertEqual(self.player_3.points, 24_500)
        self.assertEqual(self.player_4.points, 24_500)

    def test_oya_ron(self):
        self.kyoku.winners = [self.player_1]
        self.kyoku.apply_points(3, 70, False, self.player_2)
        self.assertEqual(self.player_1.points, 37_000)
        self.assertEqual(self.player_2.points, 13_000)
        self.assertEqual(self.player_3.points, 25_000)
        self.assertEqual(self.player_4.points, 25_000)

    def test_ko_tsumo(self):
        self.kyoku.winners = [self.player_2]
        self.kyoku.apply_points(3, 30, True)
        self.assertEqual(self.player_1.points, 23_000)
        self.assertEqual(self.player_2.points, 29_000)
        self.assertEqual(self.player_3.points, 24_000)
        self.assertEqual(self.player_4.points, 24_000)

    def test_ko_ron(self):
        self.kyoku.winners = [self.player_2]
        self.kyoku.apply_points(3, 30, False, self.player_4)
        self.assertEqual(self.player_1.points, 25_000)
        self.assertEqual(self.player_2.points, 28_900)
        self.assertEqual(self.player_3.points, 25_000)
        self.assertEqual(self.player_4.points, 21_100)

    def test_tsumo_with_honba(self):
        self.kyoku.winners = [self.player_2]
        self.kyoku.honba = 1
        self.kyoku.apply_points(4, 25, True)
        self.assertEqual(self.player_1.points, 21_700)
        self.assertEqual(self.player_2.points, 31_700)
        self.assertEqual(self.player_3.points, 23_300)
        self.assertEqual(self.player_4.points, 23_300)

    def test_tsumo_with_kyotaku(self):
        self.kyoku.winners = [self.player_1]
        self.kyoku.kyotaku = 2
        self.player_1.points = 24_000
        self.player_2.points = 24_000
        self.kyoku.apply_points(6, 30, True)
        self.assertEqual(self.player_1.points, 44_000)
        self.assertEqual(self.player_2.points, 18_000)
        self.assertEqual(self.player_3.points, 19_000)
        self.assertEqual(self.player_4.points, 19_000)
