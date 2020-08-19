import unittest

from mahjong.components import Tile, Suit, Jihai, Naki, Huro
from mahjong.player import Player, Position
from mahjong.naki_and_actions import (
    check_ankan, check_chakan, check_daminkan, check_pon, check_chii,
    check_tenpai, check_riichi)


class TestRon(unittest.TestCase):
    ...


class TestTsumo(unittest.TestCase):
    ...


class TestYaku(unittest.TestCase):
    ...


class TestFuriten(unittest.TestCase):
    ...


class TestAnkan(unittest.TestCase):

    def setUp(self):
        self.player = Player('test', Position.TON.value)
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.SHAA.value).index] += 3
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HATSU.value).index] += 2
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HAKU.value).index] += 1

    def test_ankan_1(self):
        new_tile = Tile(Suit.JIHAI.value, Jihai.SHAA.value)
        ankan_list = [new_tile]
        self.assertEqual(check_ankan(self.player, new_tile), ankan_list)

    def test_ankan_2(self):
        kan_in_hand = Tile(Suit.JIHAI.value, Jihai.TON.value)
        self.player.hand[kan_in_hand.index] += 4

        new_tile = Tile(Suit.JIHAI.value, Jihai.SHAA.value)
        ankan_list = sorted([new_tile, kan_in_hand])

        self.assertEqual(check_ankan(self.player, new_tile), ankan_list)

    def test_no_ankan(self):
        new_tile = Tile(Suit.JIHAI.value, Jihai.HATSU.value)
        self.assertEqual(check_ankan(self.player, new_tile), [])


class TestChakan(unittest.TestCase):

    def setUp(self):
        self.player = Player('test', Position.TON.value)
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.SHAA.value).index] += 3
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HATSU.value).index] += 2
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HAKU.value).index] += 1
        self.player.kabe.append(Huro(Naki.PON, [Tile(Suit.PINZU.value, 5),
                                                Tile(Suit.PINZU.value, 5),
                                                Tile(Suit.PINZU.value, 5)]))
        self.player.kabe.append(Huro(Naki.PON, [Tile(Suit.MANZU.value, 7),
                                                Tile(Suit.MANZU.value, 7),
                                                Tile(Suit.MANZU.value, 7)]))

    def test_chakan_1(self):
        new_tile = Tile(Suit.PINZU.value, 5)
        chakan_list = [new_tile]
        self.assertEqual(check_chakan(self.player, new_tile), chakan_list)

    def test_chakan_2(self):
        self.player.hand[Tile(Suit.MANZU.value, 7).index] += 1
        new_tile = Tile(Suit.PINZU.value, 5)
        chakan_list = sorted([new_tile, Tile(Suit.MANZU.value, 7)])
        self.assertEqual(check_chakan(self.player, new_tile), chakan_list)

    def test_no_chakan(self):
        new_tile = Tile(Suit.PINZU.value, 6)
        self.assertEqual(check_chakan(self.player, new_tile), [])


class TestDaminkan(unittest.TestCase):

    def setUp(self):
        self.player = Player('test', Position.TON.value)
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.SHAA.value).index] += 3
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HATSU.value).index] += 2
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HAKU.value).index] += 1

    def test_daminkan(self):
        discarded_tile = Tile(Suit.JIHAI.value, Jihai.SHAA.value)
        self.assertEqual(check_daminkan(self.player, discarded_tile), True)

    def test_no_daminkan(self):
        discarded_tile = Tile(Suit.JIHAI.value, Jihai.HATSU.value)
        self.assertEqual(check_daminkan(self.player, discarded_tile), False)


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

    def test_chii_1(self):
        discard = Tile(Suit.MANZU.value, 1)
        possible_sets = [[Tile(Suit.MANZU.value, 1),
                          Tile(Suit.MANZU.value, 2),
                          Tile(Suit.MANZU.value, 3)]]
        chii_sets = check_chii(self.player, discard)
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
        chii_sets = check_chii(self.player, discard)
        chii_sets = [sorted(chii_set) for chii_set in chii_sets]

        self.assertEqual(chii_sets, possible_sets)

    def test_chii_3(self):
        discard = Tile(Suit.MANZU.value, 7)
        possible_sets = [[Tile(Suit.MANZU.value, 5),
                          Tile(Suit.MANZU.value, 6),
                          Tile(Suit.MANZU.value, 7)]]
        chii_sets = check_chii(self.player, discard)
        chii_sets = [sorted(chii_set) for chii_set in chii_sets]

        self.assertEqual(chii_sets, possible_sets)

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

    def test_tenpai_1(self):
        player_1_tenpai = [Tile(Suit.MANZU.value, 3),
                           Tile(Suit.SOUZU.value, 5)]
        machi_list = sorted(check_tenpai(self.player_1))
        self.assertEqual(machi_list, player_1_tenpai)

    def test_tenpai_2(self):
        player_2_tenpai = [Tile(Suit.JIHAI.value, Jihai.PEI.value),
                           Tile(Suit.PINZU.value, 4),
                           Tile(Suit.PINZU.value, 7)]
        machi_list = sorted(check_tenpai(self.player_2))
        self.assertEqual(machi_list, player_2_tenpai)

    def test_tenpai_3(self):
        player_3_tenpai = [Tile(Suit.SOUZU.value, 1),
                           Tile(Suit.SOUZU.value, 4),
                           Tile(Suit.SOUZU.value, 7)]
        machi_list = sorted(check_tenpai(self.player_3))
        self.assertEqual(machi_list, player_3_tenpai)

    def test_tenpai_4(self):
        player_4_tenpai = [Tile(Suit.JIHAI.value, Jihai.NAN.value),
                           Tile(Suit.SOUZU.value, 2)]
        machi_list = sorted(check_tenpai(self.player_4))
        self.assertEqual(machi_list, player_4_tenpai)

    def test_tenpai_5(self):
        player_5_tenpai = [Tile(Suit.MANZU.value, 2)]
        machi_list = sorted(check_tenpai(self.player_5))
        self.assertEqual(machi_list, player_5_tenpai)

    def test_tenpai_6(self):
        player_6_tenpai = [Tile(Suit.JIHAI.value, Jihai.TON.value)]
        machi_list = sorted(check_tenpai(self.player_6))
        self.assertEqual(machi_list, player_6_tenpai)

    def test_tenpai_7(self):
        player_7_tenpai = [Tile(Suit.MANZU.value, 1),
                           Tile(Suit.MANZU.value, 4)]
        machi_list = sorted(check_tenpai(self.player_7))
        self.assertEqual(machi_list, player_7_tenpai)

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