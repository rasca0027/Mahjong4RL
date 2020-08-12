import unittest

from mahjong.mahjong import Tile, Suit, Jihai
from mahjong.player import Player, Position
from mahjong.naki_and_actions import check_pon, check_chii


class TestPon(unittest.TestCase):

    def setUp(self):
        self.player = Player('test', Position.TON.value)
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.SHAA.value).index] += 3
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HATSU.value).index] += 2
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HAKU.value).index] += 1

    def test_pon(self):
        discard_shaa = Tile(Suit.JIHAI.value, Jihai.SHAA.value)
        discard_hatsu = Tile(Suit.JIHAI.value, Jihai.HATSU.value)
        discard_haku = Tile(Suit.JIHAI.value, Jihai.HAKU.value)
        self.assertEqual(check_pon(self.player, discard_shaa), True)
        self.assertEqual(check_pon(self.player, discard_hatsu), True)
        self.assertEqual(check_pon(self.player, discard_haku), False)


class TestChii(unittest.TestCase):

    def setUp(self):
        self.player = Player('test', Position.TON.value)
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.SHAA.value).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 2).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 3).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 4).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 5).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 6).index] += 1

    def test_chii(self):
        discard_1 = Tile(Suit.MANZU.value, 1)
        possible_sets_1 = [[Tile(Suit.MANZU.value, 1),
                            Tile(Suit.MANZU.value, 2),
                            Tile(Suit.MANZU.value, 3)]]
        discard_4 = Tile(Suit.MANZU.value, 4)
        possible_sets_4 = [[Tile(Suit.MANZU.value, 2),
                            Tile(Suit.MANZU.value, 3),
                            Tile(Suit.MANZU.value, 4)],
                           [Tile(Suit.MANZU.value, 3),
                            Tile(Suit.MANZU.value, 4),
                            Tile(Suit.MANZU.value, 5)],
                           [Tile(Suit.MANZU.value, 4),
                            Tile(Suit.MANZU.value, 5),
                            Tile(Suit.MANZU.value, 6)]]
        discard_7 = Tile(Suit.MANZU.value, 7)
        possible_sets_7 = [[Tile(Suit.MANZU.value, 5),
                            Tile(Suit.MANZU.value, 6),
                            Tile(Suit.MANZU.value, 7)]]
        self.assertEqual(check_chii(self.player, discard_1), possible_sets_1)
        self.assertEqual(check_chii(self.player, discard_4), possible_sets_4)
        self.assertEqual(check_chii(self.player, discard_7), possible_sets_7)
