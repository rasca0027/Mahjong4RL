import unittest
import pyinputplus as pyinput
from unittest.mock import MagicMock

from mahjong.components import Tile, Stack, Suit, Jihai, Naki, Huro, Action
from mahjong.player import Player
from mahjong.naki_and_actions import (
    check_ron, check_tsumo, check_furiten, check_own_discard_furiten,
    check_ankan, check_chakan, check_daminkan, check_pon, check_chii,
    check_riichi, check_tenpai, check_remains_are_sets)


class TestRon(unittest.TestCase):

    def setUp(self):
        # tenpai: 3 MANZU 5 SOUZU
        self.player = Player('test', 1)
        self.player.hand[Tile(Suit.PINZU.value, 1).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 2).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 3).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 4).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 5).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 6).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 7).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 8).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 9).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 3).index] += 2
        self.player.hand[Tile(Suit.SOUZU.value, 5).index] += 2

        self.stack = Stack()
        self.bakaze = Jihai.TON

    def test_ron(self):
        discard_1 = Tile(Suit.MANZU.value, 3)
        discard_2 = Tile(Suit.SOUZU.value, 5)

        ron_1 = check_ron(self.player, discard_1, self.stack, self.bakaze)
        ron_2 = check_ron(self.player, discard_2, self.stack, self.bakaze)
        self.assertEqual(ron_1, True)
        self.assertEqual(ron_2, True)

    def test_no_ron(self):
        discard_1 = Tile(Suit.MANZU.value, 4)
        ron_1 = check_ron(self.player, discard_1, self.stack, self.bakaze)
        self.assertEqual(ron_1, False)

        # 振聴
        discard_2 = Tile(Suit.MANZU.value, 3)
        self.player.add_kawa(Tile(Suit.MANZU.value, 3))

        ron_2 = check_ron(self.player, discard_2, self.stack, self.bakaze)
        self.assertEqual(ron_2, False)


class TestTsumo(unittest.TestCase):

    def setUp(self):
        # tenpai: 3 MANZU 5 SOUZU
        self.player = Player('test', 1)
        self.player.hand[Tile(Suit.PINZU.value, 1).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 2).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 3).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 4).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 5).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 6).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 7).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 8).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 9).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 3).index] += 2
        self.player.hand[Tile(Suit.SOUZU.value, 5).index] += 2

        self.stack = Stack()
        self.bakaze = Jihai.TON

    def test_tsumo(self):
        discard_1 = Tile(Suit.MANZU.value, 3)
        discard_2 = Tile(Suit.SOUZU.value, 5)
        check_tsumo_1 = check_tsumo(self.player,
                                    discard_1,
                                    self.stack,
                                    self.bakaze)
        check_tsumo_2 = check_tsumo(self.player,
                                    discard_2,
                                    self.stack,
                                    self.bakaze)

        self.assertEqual(check_tsumo_1, True)
        self.assertEqual(check_tsumo_2, True)

    def test_no_tsumo(self):
        discard_1 = Tile(Suit.MANZU.value, 4)
        check_no_tsumo = check_tsumo(self.player,
                                     discard_1,
                                     self.stack,
                                     self.bakaze)
        self.assertEqual(check_no_tsumo, False)


class TestYaku(unittest.TestCase):
    ...


class TestFuriten(unittest.TestCase):
    def setUp(self):
        # tenpai: TON and NAN
        self.player = Player('test', 1)
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.TON.value).index] += 2
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.NAN.value).index] += 2
        naki_tile_1 = Tile(Suit.SOUZU.value, 5)
        naki_tile_1.owner = 0
        naki_tile_2 = Tile(Suit.PINZU.value, 5)
        naki_tile_2.owner = 3
        naki_tile_3 = Tile(Suit.MANZU.value, 8)
        naki_tile_3.owner = 0
        naki_tile_4 = Tile(Suit.MANZU.value, 6)
        naki_tile_4.owner = 0
        self.player.kabe.append(
            Huro(Naki.PON,
                 naki_tile_1,
                 [Tile(Suit.SOUZU.value, 5) for i in range(3)]))
        self.player.kabe.append(
            Huro(Naki.PON,
                 naki_tile_2,
                 [Tile(Suit.PINZU.value, 5) for i in range(3)]))
        self.player.kabe.append(
            Huro(Naki.CHII,
                 naki_tile_3,
                 [Tile(Suit.MANZU.value, i) for i in range(7, 10)]))
        self.player.kabe.append(
            Huro(Naki.CHII,
                 naki_tile_4,
                 [Tile(Suit.MANZU.value, i) for i in range(6, 9)]))

    def test_furiten(self):
        self.player.add_kawa(Tile(Suit.JIHAI.value, Jihai.TON.value))
        self.assertEqual(check_furiten(self.player), True)

    def test_no_furiten(self):
        self.assertEqual(check_furiten(self.player), False)

    def test_own_discard_furiten(self):
        self.player.add_kawa(Tile(Suit.JIHAI.value, Jihai.TON.value))
        self.assertEqual(check_own_discard_furiten(self.player), True)

    def test_no_own_discard_furiten(self):
        self.assertEqual(check_own_discard_furiten(self.player), False)


class TestAnkan(unittest.TestCase):

    def setUp(self):
        self.player = Player('test', 1)
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.SHAA.value).index] += 3
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HATSU.value).index] += 2
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HAKU.value).index] += 1

    def test_ankan_1(self):
        new_tile = Tile(Suit.JIHAI.value, Jihai.SHAA.value)
        ankan_list = [[new_tile, new_tile, new_tile, new_tile]]
        self.assertEqual(check_ankan(self.player.hand, new_tile), ankan_list)

    def test_ankan_2(self):
        kan_in_hand = Tile(Suit.JIHAI.value, Jihai.TON.value)
        self.player.hand[kan_in_hand.index] += 4

        new_tile = Tile(Suit.JIHAI.value, Jihai.SHAA.value)
        ankan_list = sorted(
            [
                [kan_in_hand, kan_in_hand, kan_in_hand, kan_in_hand],
                [new_tile, new_tile, new_tile, new_tile]
            ])

        self.assertEqual(check_ankan(self.player.hand, new_tile), ankan_list)

    def test_no_ankan(self):
        new_tile = Tile(Suit.JIHAI.value, Jihai.HATSU.value)
        self.assertEqual(check_ankan(self.player.hand, new_tile), [])


class TestChakan(unittest.TestCase):

    def setUp(self):
        self.player = Player('test', 1)
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.SHAA.value).index] += 3
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HATSU.value).index] += 2
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HAKU.value).index] += 1
        naki_tile_1 = Tile(Suit.PINZU.value, 5)
        naki_tile_1.owner = 0
        naki_tile_2 = Tile(Suit.MANZU.value, 7)
        naki_tile_2.owner = 3
        self.player.kabe.append(
            Huro(Naki.PON,
                 naki_tile_1,
                 [Tile(Suit.PINZU.value, 5) for i in range(3)]))
        self.player.kabe.append(
            Huro(Naki.PON,
                 naki_tile_2,
                 [Tile(Suit.MANZU.value, 7) for i in range(3)]))

    def test_chakan_1(self):
        new_tile = Tile(Suit.PINZU.value, 5)
        chakan_list = [[new_tile, new_tile, new_tile, new_tile]]
        self.assertEqual(check_chakan(self.player.hand,
                                      self.player.kabe,
                                      new_tile), chakan_list)

    def test_chakan_2(self):
        tile_in_hand = Tile(Suit.MANZU.value, 7)
        self.player.hand[tile_in_hand.index] += 1
        new_tile = Tile(Suit.PINZU.value, 5)
        chakan_list = sorted(
            [
                [new_tile, new_tile, new_tile, new_tile],
                [tile_in_hand, tile_in_hand, tile_in_hand, tile_in_hand]
            ])
        self.assertEqual(check_chakan(self.player.hand,
                                      self.player.kabe,
                                      new_tile), chakan_list)

    def test_no_chakan(self):
        new_tile = Tile(Suit.PINZU.value, 6)
        self.assertEqual(check_chakan(self.player.hand,
                                      self.player.kabe,
                                      new_tile), [])


class TestDaminkan(unittest.TestCase):

    def setUp(self):
        self.player = Player('test', 1)
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.SHAA.value).index] += 3
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HATSU.value).index] += 2
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HAKU.value).index] += 1

    def test_daminkan(self):
        discarded_tile = Tile(Suit.JIHAI.value, Jihai.SHAA.value)
        self.assertEqual(
            check_daminkan(self.player.hand, discarded_tile), [[
                discarded_tile,
                Tile(Suit.JIHAI.value, Jihai.SHAA.value),
                Tile(Suit.JIHAI.value, Jihai.SHAA.value),
                Tile(Suit.JIHAI.value, Jihai.SHAA.value)
            ], ]
        )

    def test_no_daminkan(self):
        discarded_tile = Tile(Suit.JIHAI.value, Jihai.HATSU.value)
        self.assertEqual(check_daminkan(self.player.hand, discarded_tile), [])


class TestPon(unittest.TestCase):

    def setUp(self):
        self.player = Player('test', 1)
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.SHAA.value).index] += 3
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HATSU.value).index] += 2
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HAKU.value).index] += 1

    def test_pon(self):
        discard_shaa = Tile(Suit.JIHAI.value, Jihai.SHAA.value)
        discard_hatsu = Tile(Suit.JIHAI.value, Jihai.HATSU.value)
        discard_haku = Tile(Suit.JIHAI.value, Jihai.HAKU.value)
        self.assertEqual(check_pon(self.player.hand, discard_shaa), [[
            discard_shaa,
            Tile(Suit.JIHAI.value, Jihai.SHAA.value),
            Tile(Suit.JIHAI.value, Jihai.SHAA.value)
        ], ])
        self.assertEqual(check_pon(self.player.hand, discard_hatsu), [[
            discard_hatsu,
            Tile(Suit.JIHAI.value, Jihai.HATSU.value),
            Tile(Suit.JIHAI.value, Jihai.HATSU.value)
        ], ])
        self.assertEqual(check_pon(self.player.hand, discard_haku), [])


class TestChii(unittest.TestCase):

    def setUp(self):
        self.player = Player('test', 1)
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.SHAA.value).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 2).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 3).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 4).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 5).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 6).index] += 1

    def test_chii_jihai(self):
        discard = Tile(Suit.JIHAI.value, Jihai.NAN.value)
        chii_sets = check_chii(self.player.hand, discard)

        self.assertEqual(chii_sets, [])

    def test_chii_1(self):
        discard = Tile(Suit.MANZU.value, 1)
        possible_sets = [[Tile(Suit.MANZU.value, 1),
                          Tile(Suit.MANZU.value, 2),
                          Tile(Suit.MANZU.value, 3)]]
        chii_sets = check_chii(self.player.hand, discard)
        chii_sets = [sorted(chii_set) for chii_set in chii_sets]

        self.assertEqual(chii_sets, possible_sets)

    def test_chii_2(self):
        discard = Tile(Suit.MANZU.value, 4)
        possible_sets = [[Tile(Suit.MANZU.value, 2),
                          Tile(Suit.MANZU.value, 3),
                          Tile(Suit.MANZU.value, 4)],
                         [Tile(Suit.MANZU.value, 3),
                          Tile(Suit.MANZU.value, 4),
                          Tile(Suit.MANZU.value, 5)],
                         [Tile(Suit.MANZU.value, 4),
                          Tile(Suit.MANZU.value, 5),
                          Tile(Suit.MANZU.value, 6)]]
        chii_sets = check_chii(self.player.hand, discard)
        chii_sets = [sorted(chii_set) for chii_set in chii_sets]

        self.assertEqual(chii_sets, possible_sets)

    def test_chii_3(self):
        discard = Tile(Suit.MANZU.value, 7)
        possible_sets = [[Tile(Suit.MANZU.value, 5),
                          Tile(Suit.MANZU.value, 6),
                          Tile(Suit.MANZU.value, 7)]]
        chii_sets = check_chii(self.player.hand, discard)
        chii_sets = [sorted(chii_set) for chii_set in chii_sets]

        self.assertEqual(chii_sets, possible_sets)

    def test_no_chii(self):
        discard = Tile(Suit.MANZU.value, 8)
        self.assertEqual(check_chii(self.player.hand, discard), [])


class TestTenpai(unittest.TestCase):

    def setUp(self):
        self.player = Player('test', 1)

    def assert_tenpai(self, player, tenpai):
        machi_list = sorted(check_tenpai(player.hand, player.kabe))
        self.assertEqual(machi_list, tenpai)

    def test_tenpai_1(self):
        self.player.hand[Tile(Suit.PINZU.value, 1).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 2).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 3).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 4).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 5).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 6).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 7).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 8).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 9).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 3).index] += 2
        self.player.hand[Tile(Suit.SOUZU.value, 5).index] += 2
        tenpai = [Tile(Suit.MANZU.value, 3),
                  Tile(Suit.SOUZU.value, 5)]

        self.assert_tenpai(self.player, tenpai)

    def test_tenpai_2(self):
        self.player.hand[Tile(Suit.PINZU.value, 6).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 5).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 7).index] += 3
        self.player.hand[Tile(Suit.MANZU.value, 1).index] += 3
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.TON.value).index] += 3
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.PEI.value).index] += 2
        tenpai = [Tile(Suit.JIHAI.value, Jihai.PEI.value),
                  Tile(Suit.PINZU.value, 4),
                  Tile(Suit.PINZU.value, 7)]

        self.assert_tenpai(self.player, tenpai)

    def test_tenpai_3(self):
        self.player.hand[Tile(Suit.MANZU.value, 1).index] += 3
        self.player.hand[Tile(Suit.SOUZU.value, 2).index] += 1
        self.player.hand[Tile(Suit.SOUZU.value, 3).index] += 1
        self.player.hand[Tile(Suit.SOUZU.value, 4).index] += 1
        self.player.hand[Tile(Suit.SOUZU.value, 5).index] += 1
        self.player.hand[Tile(Suit.SOUZU.value, 6).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 8).index] += 3
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.SHAA.value).index] += 2
        tenpai = [Tile(Suit.SOUZU.value, 1),
                  Tile(Suit.SOUZU.value, 4),
                  Tile(Suit.SOUZU.value, 7)]

        self.assert_tenpai(self.player, tenpai)

    def test_tenpai_4(self):
        self.player.hand[Tile(Suit.SOUZU.value, 2).index] += 2
        self.player.hand[Tile(Suit.SOUZU.value, 3).index] += 1
        self.player.hand[Tile(Suit.SOUZU.value, 4).index] += 1
        self.player.hand[Tile(Suit.SOUZU.value, 5).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 8).index] += 3
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.NAN.value).index] += 2
        naki_tile = Tile(Suit.SOUZU.value, 5)
        naki_tile.owner = 0
        self.player.kabe.append(
            Huro(Naki.PON,
                 naki_tile,
                 [Tile(Suit.SOUZU.value, 5) for i in range(3)]))
        tenpai = [Tile(Suit.JIHAI.value, Jihai.NAN.value),
                  Tile(Suit.SOUZU.value, 2)]

        self.assert_tenpai(self.player, tenpai)

    def test_tenpai_5(self):
        self.player.hand[Tile(Suit.PINZU.value, 9).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 1).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 3).index] += 1
        naki_tile_1 = Tile(Suit.SOUZU.value, 5)
        naki_tile_1.owner = 0
        naki_tile_2 = Tile(Suit.PINZU.value, 5)
        naki_tile_2.owner = 3
        naki_tile_3 = Tile(Suit.MANZU.value, 8)
        naki_tile_3.owner = 0
        self.player.kabe.append(
            Huro(Naki.PON,
                 naki_tile_1,
                 [Tile(Suit.SOUZU.value, 5) for i in range(3)]))
        self.player.kabe.append(
            Huro(Naki.PON,
                 naki_tile_2,
                 [Tile(Suit.PINZU.value, 5) for i in range(3)]))
        self.player.kabe.append(
            Huro(Naki.CHII,
                 naki_tile_3,
                 [Tile(Suit.MANZU.value, i) for i in range(7, 10)]))
        tenpai = [Tile(Suit.MANZU.value, 2)]

        self.assert_tenpai(self.player, tenpai)

    def test_tenpai_6(self):
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.TON.value).index] += 1
        naki_tile_1 = Tile(Suit.JIHAI.value, Jihai.SHAA.value)
        naki_tile_1.owner = 3
        naki_tile_2 = Tile(Suit.SOUZU.value, 5)
        naki_tile_2.owner = 3
        naki_tile_3 = Tile(Suit.PINZU.value, 5)
        naki_tile_3.owner = 2
        naki_tile_4 = Tile(Suit.MANZU.value, 9)
        naki_tile_4.owner = 0
        self.player.kabe.append(
            Huro(Naki.PON,
                 naki_tile_1,
                 [Tile(Suit.JIHAI.value, Jihai.SHAA.value) for i in range(3)]))
        self.player.kabe.append(
            Huro(Naki.PON,
                 naki_tile_2,
                 [Tile(Suit.SOUZU.value, 5) for i in range(3)]))
        self.player.kabe.append(
            Huro(Naki.PON,
                 naki_tile_3,
                 [Tile(Suit.PINZU.value, 5) for i in range(3)]))
        self.player.kabe.append(
            Huro(Naki.CHII,
                 naki_tile_4,
                 [Tile(Suit.MANZU.value, i) for i in range(7, 10)]))
        tenpai = [Tile(Suit.JIHAI.value, Jihai.TON.value)]

        self.assert_tenpai(self.player, tenpai)

    def test_tenpai_7(self):
        self.player.hand[Tile(Suit.MANZU.value, 1).index] += 4
        self.player.hand[Tile(Suit.MANZU.value, 2).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 3).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 4).index] += 4
        naki_tile = Tile(Suit.JIHAI.value, Jihai.SHAA.value)
        naki_tile.owner = 0
        self.player.kabe.append(
            Huro(Naki.PON,
                 naki_tile,
                 [Tile(Suit.JIHAI.value, Jihai.SHAA.value) for i in range(3)]))
        tenpai = [Tile(Suit.MANZU.value, 1),
                  Tile(Suit.MANZU.value, 4)]
        # tenpai: 1 MANZU 4 MANZU 空聴（カラテン）
        self.assert_tenpai(self.player, tenpai)

    def test_tenpai_8(self):
        self.player.hand[Tile(Suit.MANZU.value, 1).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 2).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 3).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 4).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 5).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 6).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 7).index] += 1
        tenpai = [Tile(Suit.MANZU.value, 1),
                  Tile(Suit.MANZU.value, 4),
                  Tile(Suit.MANZU.value, 7)]
        self.assert_tenpai(self.player, tenpai)

    def test_tenpai_9(self):
        self.player.hand[Tile(Suit.MANZU.value, 1).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 3).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 5).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 7).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 9).index] += 2
        self.player.hand[Tile(Suit.SOUZU.value, 1).index] += 2
        self.player.hand[Tile(Suit.SOUZU.value, 3).index] += 1
        tenpai = [Tile(Suit.SOUZU.value, 3)]
        self.assert_tenpai(self.player, tenpai)

    def test_tenpai_10(self):
        self.player.hand[Tile(Suit.MANZU.value, 9).index] += 1
        self.player.hand[Tile(Suit.SOUZU.value, 1).index] += 1
        self.player.hand[Tile(Suit.SOUZU.value, 9).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 1).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 9).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HAKU.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HATSU.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.CHUN.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.TON.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.NAN.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.SHAA.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.PEI.value).index] += 2
        tenpai = [Tile(Suit.MANZU.value, 1)]
        # tenpai: 1 MANZU (kokushi musou single wait)
        self.assert_tenpai(self.player, tenpai)

    def test_tenpai_11(self):
        self.player.hand[Tile(Suit.MANZU.value, 2).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 9).index] += 1
        self.player.hand[Tile(Suit.SOUZU.value, 1).index] += 1
        self.player.hand[Tile(Suit.SOUZU.value, 9).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 1).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 9).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HAKU.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HATSU.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.CHUN.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.TON.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.NAN.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.SHAA.value).index] += 1
        tenpai = []
        # no tenpai: test kokushi musou single wait
        self.assert_tenpai(self.player, tenpai)

    def test_tenpai_12(self):
        self.player.hand[Tile(Suit.MANZU.value, 2).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 9).index] += 1
        self.player.hand[Tile(Suit.SOUZU.value, 1).index] += 1
        self.player.hand[Tile(Suit.SOUZU.value, 9).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 1).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 9).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HAKU.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HATSU.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.CHUN.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.TON.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.NAN.value).index] += 0
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.SHAA.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.PEI.value).index] += 1
        tenpai = []
        # no tenpai: test kokushi musou single wait
        self.assert_tenpai(self.player, tenpai)

    def test_tenpai_13(self):
        self.player.hand[Tile(Suit.MANZU.value, 1).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 9).index] += 1
        self.player.hand[Tile(Suit.SOUZU.value, 1).index] += 1
        self.player.hand[Tile(Suit.SOUZU.value, 9).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 1).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 9).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HAKU.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HATSU.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.CHUN.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.TON.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.NAN.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.SHAA.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.PEI.value).index] += 1
        honor_tiles, terminal_tiles = Tile.get_yaochuuhai()
        tenpai = honor_tiles + terminal_tiles
        # tenpai: 1 MANZU (kokushi musou 13-way wait)
        self.assert_tenpai(self.player, tenpai)

    def test_no_tenpai(self):
        self.player.hand[Tile(Suit.PINZU.value, 1).index] -= 1
        self.player.hand[Tile(Suit.PINZU.value, 2).index] += 1
        self.assertEqual(check_tenpai(self.player.hand, self.player.kabe), [])


class TestRiichi(unittest.TestCase):
    def setUp(self):
        # tenpai: 3 MANZU 5 SOUZU
        self.player = Player('test', 1)
        for i in range(1, 10):
            self.player.hand[Tile(Suit.PINZU.value, i).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 3).index] += 2
        self.player.hand[Tile(Suit.SOUZU.value, 5).index] += 2
        self.stack = Stack()

    def test_riichi(self):
        machi = check_tenpai(self.player.hand, self.player.kabe)
        riichi = check_riichi(self.player, machi, self.stack)
        self.assertEqual(riichi, True)

    def test_no_riichi_kabe(self):
        self.player.hand[Tile(Suit.PINZU.value, 1).index] -= 1
        self.player.hand[Tile(Suit.SOUZU.value, 5).index] -= 2
        naki_tile = Tile(Suit.SOUZU.value, 5)
        naki_tile.owner = 0
        self.player.kabe.append(
            Huro(Naki.PON,
                 naki_tile,
                 [Tile(Suit.SOUZU.value, 5) for i in range(3)]))
        self.player.menzenchin = False

        machi = check_tenpai(self.player.hand, self.player.kabe)
        riichi = check_riichi(self.player, machi, self.stack)
        self.assertEqual(riichi, False)

    def test_riichi_stack(self):
        for i in range(120):
            _ = self.stack.draw()
        machi = check_tenpai(self.player.hand, self.player.kabe)
        riichi = check_riichi(self.player, machi, self.stack)
        self.assertEqual(riichi, False)

    def test_ankan_after_riichi(self):
        # tenpai: 5 SOUZU
        self.player.hand[Tile(Suit.MANZU.value, 3).index] += 1
        self.player.hand[Tile(Suit.SOUZU.value, 5).index] -= 1
        self.player.is_riichi = True

        ankan_tile = Tile(Suit.MANZU.value, 3)
        ankan_tile.owner = 1

        pyinput.inputNum = MagicMock(side_effect=[1, 0])
        pyinput.inputChoice = MagicMock(return_value=5)

        (action, naki), discard_tile = self.player.action_with_new_tile(
            ankan_tile, False, self.stack, False)

        self.assertEqual(action, Action.NAKI)
        self.assertEqual(naki, Naki.ANKAN)
        self.assertEqual(discard_tile, None)

    def test_no_ankan_after_riichi(self):
        # tenpai: 7 PINZU
        self.player = Player('test', 1)
        self.player.hand[Tile(Suit.MANZU.value, 1).index] += 4
        self.player.hand[Tile(Suit.MANZU.value, 2).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 3).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 4).index] += 1
        for i in range(4, 7):
            self.player.hand[Tile(Suit.SOUZU.value, i).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 7).index] += 1

        self.player.is_riichi = True

        ankan_tile = Tile(Suit.SOUZU.value, 1)
        ankan_tile.owner = 1

        pyinput.inputNum = MagicMock(side_effect=[0])

        (action, naki), discard_tile = self.player.action_with_new_tile(
            ankan_tile, False, self.stack, False)

        self.assertEqual(action, Action.NOACT)
        self.assertEqual(naki, Naki.NONE)
        self.assertEqual(discard_tile, ankan_tile)


class TestRemainsAreSets(unittest.TestCase):

    def setUp(self):
        # tenpai: 3 MANZU 5 SOUZU
        self.player_1 = Player('test_1', 1)
        self.player_1.hand[Tile(Suit.PINZU.value, 1).index] += 1
        self.player_1.hand[Tile(Suit.PINZU.value, 2).index] += 1
        self.player_1.hand[Tile(Suit.PINZU.value, 3).index] += 1
        self.player_1.hand[Tile(Suit.PINZU.value, 4).index] += 1
        self.player_1.hand[Tile(Suit.PINZU.value, 5).index] += 1
        self.player_1.hand[Tile(Suit.PINZU.value, 6).index] += 1
        self.player_1.hand[Tile(Suit.PINZU.value, 7).index] += 1
        self.player_1.hand[Tile(Suit.PINZU.value, 8).index] += 1
        self.player_1.hand[Tile(Suit.PINZU.value, 9).index] += 1
        self.player_1.hand[Tile(Suit.MANZU.value, 3).index] += 2
        self.player_1.hand[Tile(Suit.SOUZU.value, 5).index] += 2

    def test_remains_are_sets(self):
        self.player_1.hand[Tile(Suit.MANZU.value, 3).index] += 1
        self.player_1.hand[Tile(Suit.SOUZU.value, 5).index] -= 2
        remain_tiles = self.player_1.hand
        huro_count = len(self.player_1.kabe)
        self.assertEqual(
            check_remains_are_sets(remain_tiles, huro_count), True)

    def test_remains_are_not_sets(self):
        self.player_1.hand[Tile(Suit.SOUZU.value, 5).index] -= 2
        remain_tiles = self.player_1.hand
        huro_count = len(self.player_1.kabe)
        self.assertEqual(
            check_remains_are_sets(remain_tiles, huro_count), False)
