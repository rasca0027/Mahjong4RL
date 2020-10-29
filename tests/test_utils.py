import unittest

from mahjong.components import Suit, Tile
from mahjong.utils import get_values, get_name, roundup, is_yaochuu


class TestGetValue(unittest.TestCase):

    def test_get_values(self):
        suit_value = ['JIHAI', 'MANZU', 'SOUZU', 'PINZU']
        self.assertEqual(get_values(Suit), suit_value)


class TestGetName(unittest.TestCase):

    def test_get_name(self):
        self.assertEqual(get_name(Suit, 0), 'JIHAI')


class TestRoundup(unittest.TestCase):

    def test_roundup(self):
        self.assertEqual(roundup(1), 100)


class TestIsYaochuu(unittest.TestCase):

    def setUp(self):
        self.yaochuu_tile_1 = Tile(Suit.JIHAI.value, 1)
        self.yaochuu_tile_2 = Tile(Suit.MANZU.value, 9)
        self.not_yaochuu_tile = Tile(Suit.SOUZU.value, 5)

    def test_is_yaochuu(self):
        test_1 = is_yaochuu(self.yaochuu_tile_1.suit, self.yaochuu_tile_1.rank)
        test_2 = is_yaochuu(self.yaochuu_tile_2.suit, self.yaochuu_tile_2.rank)
        test_3 = is_yaochuu(self.not_yaochuu_tile.suit,
                            self.not_yaochuu_tile.rank)

        self.assertEqual(test_1, True)
        self.assertEqual(test_2, True)
        self.assertEqual(test_3, False)