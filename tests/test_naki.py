import unittest

from mahjong.mahjong import Tile, Suit, Jihai, Naki, Huro
from mahjong.player import Player, Position
from mahjong.naki_and_actions import (
    check_pon, check_chii, check_tenpai, check_riichi)


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
        discard_2 = Tile(Suit.MANZU.value, 4)
        possible_sets_2 = [[Tile(Suit.MANZU.value, 2),
                            Tile(Suit.MANZU.value, 3),
                            Tile(Suit.MANZU.value, 4)],
                           [Tile(Suit.MANZU.value, 3),
                            Tile(Suit.MANZU.value, 4),
                            Tile(Suit.MANZU.value, 5)],
                           [Tile(Suit.MANZU.value, 4),
                            Tile(Suit.MANZU.value, 5),
                            Tile(Suit.MANZU.value, 6)]]
        discard_3 = Tile(Suit.MANZU.value, 7)
        possible_sets_3 = [[Tile(Suit.MANZU.value, 5),
                            Tile(Suit.MANZU.value, 6),
                            Tile(Suit.MANZU.value, 7)]]
        self.assertEqual(check_chii(self.player, discard_1), possible_sets_1)
        self.assertEqual(check_chii(self.player, discard_2), possible_sets_2)
        self.assertEqual(check_chii(self.player, discard_3), possible_sets_3)

    def test_no_chii(self):
        discard = Tile(Suit.MANZU.value, 8)
        self.assertEqual(check_chii(self.player, discard), [])


class TestTenpai(unittest.TestCase):

    def setUp(self):
        # tenpai: 3 MANZU 5 SOUZU
        self.player_1 = Player('test_1', Position.TON.value)
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
        # tenpai: PEI 4 PINZU 7 PINZU
        self.player_2 = Player('test_2', Position.TON.value)
        self.player_2.hand[Tile(Suit.PINZU.value, 5).index] += 1
        self.player_2.hand[Tile(Suit.PINZU.value, 6).index] += 1
        self.player_2.hand[Tile(Suit.PINZU.value, 7).index] += 3
        self.player_2.hand[Tile(Suit.MANZU.value, 1).index] += 3
        self.player_2.hand[Tile(Suit.JIHAI.value, Jihai.TON.value).index] += 3
        self.player_2.hand[Tile(Suit.JIHAI.value, Jihai.PEI.value).index] += 2
        # tenpai: 1 SOUZU 4 SOUZU 7 SOUZU
        self.player_3 = Player('test_3', Position.TON.value)
        self.player_3.hand[Tile(Suit.MANZU.value, 1).index] += 3
        self.player_3.hand[Tile(Suit.SOUZU.value, 2).index] += 1
        self.player_3.hand[Tile(Suit.SOUZU.value, 3).index] += 1
        self.player_3.hand[Tile(Suit.SOUZU.value, 4).index] += 1
        self.player_3.hand[Tile(Suit.SOUZU.value, 5).index] += 1
        self.player_3.hand[Tile(Suit.SOUZU.value, 6).index] += 1
        self.player_3.hand[Tile(Suit.PINZU.value, 8).index] += 3
        self.player_3.hand[Tile(Suit.JIHAI.value, Jihai.SHAA.value).index] += 2
        # tenpai: NAN 2 SOUZU
        self.player_4 = Player('test_4', Position.TON.value)
        self.player_4.hand[Tile(Suit.SOUZU.value, 2).index] += 2
        self.player_4.hand[Tile(Suit.SOUZU.value, 3).index] += 1
        self.player_4.hand[Tile(Suit.SOUZU.value, 4).index] += 1
        self.player_4.hand[Tile(Suit.SOUZU.value, 5).index] += 1
        self.player_4.hand[Tile(Suit.MANZU.value, 8).index] += 3
        self.player_4.hand[Tile(Suit.JIHAI.value, Jihai.NAN.value).index] += 2
        self.player_4.kabe.append(Huro(Naki.PON, [Tile(Suit.SOUZU.value, 5),
                                                  Tile(Suit.SOUZU.value, 5),
                                                  Tile(Suit.SOUZU.value, 5)]))
        # tenpai: 2 MANZU
        self.player_5 = Player('test_5', Position.TON.value)
        self.player_5.hand[Tile(Suit.PINZU.value, 9).index] += 2
        self.player_5.hand[Tile(Suit.MANZU.value, 1).index] += 1
        self.player_5.hand[Tile(Suit.MANZU.value, 3).index] += 1
        self.player_5.kabe.append(Huro(Naki.PON, [Tile(Suit.SOUZU.value, 5),
                                                  Tile(Suit.SOUZU.value, 5),
                                                  Tile(Suit.SOUZU.value, 5)]))
        self.player_5.kabe.append(Huro(Naki.PON, [Tile(Suit.PINZU.value, 5),
                                                  Tile(Suit.PINZU.value, 5),
                                                  Tile(Suit.PINZU.value, 5)]))
        self.player_5.kabe.append(Huro(Naki.CHII, [Tile(Suit.MANZU.value, 7),
                                                   Tile(Suit.MANZU.value, 8),
                                                   Tile(Suit.MANZU.value, 9)]))
        # tenpai: TON
        self.player_6 = Player('test_6', Position.TON.value)
        self.player_6.hand[Tile(Suit.JIHAI.value, Jihai.TON.value).index] += 1
        self.player_6.kabe.append(
            Huro(Naki.PON, [Tile(Suit.JIHAI.value, Jihai.SHAA.value),
                            Tile(Suit.JIHAI.value, Jihai.SHAA.value),
                            Tile(Suit.JIHAI.value, Jihai.SHAA.value)]))
        self.player_6.kabe.append(Huro(Naki.PON, [Tile(Suit.SOUZU.value, 5),
                                                  Tile(Suit.SOUZU.value, 5),
                                                  Tile(Suit.SOUZU.value, 5)]))
        self.player_6.kabe.append(Huro(Naki.PON, [Tile(Suit.PINZU.value, 5),
                                                  Tile(Suit.PINZU.value, 5),
                                                  Tile(Suit.PINZU.value, 5)]))
        self.player_6.kabe.append(Huro(Naki.CHII, [Tile(Suit.MANZU.value, 7),
                                                   Tile(Suit.MANZU.value, 8),
                                                   Tile(Suit.MANZU.value, 9)]))
        # tenpai: 1 MANZU 4 MANZU 空聴（カラテン）
        self.player_7 = Player('test_7', Position.TON.value)
        self.player_7.hand[Tile(Suit.MANZU.value, 1).index] += 4
        self.player_7.hand[Tile(Suit.MANZU.value, 2).index] += 1
        self.player_7.hand[Tile(Suit.MANZU.value, 3).index] += 1
        self.player_7.hand[Tile(Suit.MANZU.value, 4).index] += 4
        self.player_7.kabe.append(
            Huro(Naki.PON, [Tile(Suit.JIHAI.value, Jihai.SHAA.value),
                            Tile(Suit.JIHAI.value, Jihai.SHAA.value),
                            Tile(Suit.JIHAI.value, Jihai.SHAA.value)]))

    def test_tenpai(self):
        player_1_tenpai = [Tile(Suit.MANZU.value, 3),
                           Tile(Suit.SOUZU.value, 5)]
        player_2_tenpai = [Tile(Suit.JIHAI.value, Jihai.PEI.value),
                           Tile(Suit.PINZU.value, 4),
                           Tile(Suit.PINZU.value, 7)]
        player_3_tenpai = [Tile(Suit.SOUZU.value, 1),
                           Tile(Suit.SOUZU.value, 4),
                           Tile(Suit.SOUZU.value, 7)]
        player_4_tenpai = [Tile(Suit.JIHAI.value, Jihai.NAN.value),
                           Tile(Suit.SOUZU.value, 2)]
        player_5_tenpai = [Tile(Suit.MANZU.value, 2)]
        player_6_tenpai = [Tile(Suit.JIHAI.value, Jihai.TON.value)]
        player_7_tenpai = [Tile(Suit.MANZU.value, 1),
                           Tile(Suit.MANZU.value, 4)]
        self.assertEqual(check_tenpai(self.player_1), player_1_tenpai)
        self.assertEqual(check_tenpai(self.player_2), player_2_tenpai)
        self.assertEqual(check_tenpai(self.player_3), player_3_tenpai)
        self.assertEqual(check_tenpai(self.player_4), player_4_tenpai)
        self.assertEqual(check_tenpai(self.player_5), player_5_tenpai)
        self.assertEqual(check_tenpai(self.player_6), player_6_tenpai)
        self.assertEqual(check_tenpai(self.player_7), player_7_tenpai)

    def test_no_tenpai(self):
        self.player_1.hand[Tile(Suit.PINZU.value, 1).index] -= 1
        self.player_1.hand[Tile(Suit.PINZU.value, 2).index] += 1
        self.assertEqual(check_tenpai(self.player_1), [])


class TestRiichi(unittest.TestCase):
    def setUp(self):
        # tenpai: 3 MANZU 5 SOUZU
        self.player = Player('test', Position.TON.value)
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

    def test_riichi(self):
        machi = check_tenpai(self.player)
        self.assertEqual(check_riichi(self.player, machi), True)

    def test_no_riichi(self):
        self.player.hand[Tile(Suit.PINZU.value, 1).index] -= 1
        self.player.hand[Tile(Suit.SOUZU.value, 5).index] -= 2
        self.player.kabe.append(Huro(Naki.PON, [Tile(Suit.SOUZU.value, 5),
                                                Tile(Suit.SOUZU.value, 5),
                                                Tile(Suit.SOUZU.value, 5)]))

        machi = check_tenpai(self.player)
        self.assertEqual(check_riichi(self.player, machi), False)
