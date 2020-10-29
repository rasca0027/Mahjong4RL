import unittest

from mahjong.components import Suit, Tile
from mahjong.player import Player
from mahjong.helpers import is_yaochuu, consists_jantou_and_sets


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


class TestConsistsJantouAndSets(unittest.TestCase):

    def setUp(self):
        self.player = Player('test', 0)
        self.player.hand[Tile(Suit.PINZU.value, 1).index] += 3
        self.player.hand[Tile(Suit.PINZU.value, 2).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 3).index] += 1

    def test_consists_jantou_and_sets(self):
        self.assertEqual(
            consists_jantou_and_sets(self.player.hand, 3), True)

    def test_not_consists_jantou_and_sets(self):
        self.player.hand[Tile(Suit.PINZU.value, 3).index] -= 1
        self.assertEqual(
            consists_jantou_and_sets(self.player.hand, 3), False)
