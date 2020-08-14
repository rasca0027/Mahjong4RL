import unittest

from mahjong.components import Tile, Suit


class TestTile(unittest.TestCase):

    def setUp(self):
        self.tile = Tile(Suit.MANZU.value, 2)  # 二萬

    def test_getter(self):
        self.assertEqual(self.tile.suit, 1)
        self.assertEqual(self.tile.rank, 2)

    def test_suit_setter(self):
        self.tile.suit = Suit.PINZU.value
        self.assertEqual(self.tile.suit, 3)
        self.assertEqual(self.tile.rank, 2)

    def test_suit_setter_error(self):
        with self.assertRaises(ValueError):
            self.tile.suit = 4

    def test_suit_setter_error2(self):
        with self.assertRaises(ValueError):
            self.tile.suit = -1

    def test_rank_setter_error(self):
        with self.assertRaises(ValueError):
            self.tile.rank = -1

    def test_index(self):
        self.assertEqual(self.tile.index, 12)
