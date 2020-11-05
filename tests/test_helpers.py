import unittest

from mahjong.components import Suit, Tile, Huro, Naki, Jihai
from mahjong.player import Player
from mahjong.helpers import (
    is_yaochuu, consists_jantou_and_sets, separate_sets, is_chi, is_pon
)


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


class TestSeparateSets(unittest.TestCase):

    def setUp(self):
        self.player = Player('test', 0)
        self.player.hand[Tile(Suit.SOUZU.value, 2).index] += 2
        self.player.hand[Tile(Suit.SOUZU.value, 3).index] += 1
        self.player.hand[Tile(Suit.SOUZU.value, 4).index] += 1
        self.player.hand[Tile(Suit.SOUZU.value, 5).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 8).index] += 3
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.NAN.value).index] += 3
        naki_tile = Tile(Suit.SOUZU.value, 5)
        naki_tile.owner = 0
        self.player.kabe.append(
            Huro(Naki.PON,
                 naki_tile,
                 [Tile(Suit.SOUZU.value, 5) for i in range(3)]))

    def test_separate_sets(self):
        koutsu_in_hand = [Tile(Suit.JIHAI.value, Jihai.NAN.value),
                          Tile(Suit.MANZU.value, 8)]
        shuntsu_in_hand = [[Tile(Suit.SOUZU.value, 3),
                            Tile(Suit.SOUZU.value, 4),
                            Tile(Suit.SOUZU.value, 5)]]
        koutsu, shuntsu, jantou = separate_sets(self.player.hand,
                                                len(self.player.kabe))

        self.assertEqual(koutsu, koutsu_in_hand)
        self.assertEqual(shuntsu, shuntsu_in_hand)
        self.assertEqual(jantou, Tile(Suit.SOUZU.value, 2))

    def test_not_separate_sets(self):
        self.player.hand[Tile(Suit.MANZU.value, 8).index] -= 1
        koutsu, shuntsu, jantou = separate_sets(self.player.hand,
                                                len(self.player.kabe))

        self.assertEqual(koutsu, [])
        self.assertEqual(shuntsu, [])
        self.assertEqual(jantou, None)


class TestIsChi(unittest.TestCase):

    def test_is_chi(self):
        tile_set = [Tile(Suit.SOUZU.value, 3),
                    Tile(Suit.SOUZU.value, 4),
                    Tile(Suit.SOUZU.value, 5)]
        self.assertEqual(is_chi(tile_set), True)

    def test_not_chi(self):
        tile_set = [Tile(Suit.SOUZU.value, 3),
                    Tile(Suit.SOUZU.value, 4),
                    Tile(Suit.SOUZU.value, 7)]
        self.assertEqual(is_chi(tile_set), False)
        tile_set.pop()
        self.assertEqual(is_chi(tile_set), False)


class TestIsPon(unittest.TestCase):

    def test_is_pon(self):
        tile_set = [Tile(Suit.MANZU.value, 5) for _ in range(3)]
        self.assertEqual(is_pon(tile_set), True)

    def test_not_pon(self):
        tile_set = [Tile(Suit.SOUZU.value, 3),
                    Tile(Suit.SOUZU.value, 4),
                    Tile(Suit.SOUZU.value, 5)]
        self.assertEqual(is_pon(tile_set), False)
        tile_set.pop()
        self.assertEqual(is_pon(tile_set), False)
