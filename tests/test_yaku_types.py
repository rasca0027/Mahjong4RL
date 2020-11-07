import unittest

from mahjong.components import Tile, Suit, Jihai, Naki, Huro
from mahjong.player import Player
from mahjong.components import Stack
from mahjong.yaku_types import TeYaku, Yakuhai, Peikou, Chanta


class TestTeYaku(unittest.TestCase):

    def setUp(self):
        self.player = Player('test', 0)
        self.stack = Stack
        self.bakaze = Jihai.TON

    def test_no_ryuuiisou(self):  # 緑一色
        self.player.hand[Tile(Suit.SOUZU.value, 2).index] += 2
        self.player.hand[Tile(Suit.SOUZU.value, 3).index] += 2
        self.player.hand[Tile(Suit.SOUZU.value, 4).index] += 2
        self.player.hand[Tile(Suit.SOUZU.value, 6).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 8).index] += 2
        naki_tile = Tile(Suit.JIHAI.value, Jihai.HATSU.value)
        naki_tile.owner = 2
        self.player.kabe.append(
            Huro(Naki.PON, naki_tile,
                 [Tile(Suit.JIHAI.value, Jihai.HATSU.value)
                  for i in range(1, 4)]))
        self.player.agari_tile = Tile(Suit.SOUZU.value, 6)
        self.player.menzenchin = False

        yaku_types = TeYaku(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.ryuuiisou(), False)
        self.assertEqual(yaku_types.total_yaku, [])
        self.assertEqual(yaku_types.total_han, 0)
        self.assertEqual(yaku_types.yakuman_count, 0)

    def test_ryuuiisou(self):  # 緑一色
        self.player.hand[Tile(Suit.SOUZU.value, 2).index] += 2
        self.player.hand[Tile(Suit.SOUZU.value, 3).index] += 2
        self.player.hand[Tile(Suit.SOUZU.value, 4).index] += 2
        self.player.hand[Tile(Suit.SOUZU.value, 6).index] += 2
        self.player.hand[Tile(Suit.SOUZU.value, 8).index] += 2
        naki_tile = Tile(Suit.JIHAI.value, Jihai.HATSU.value)
        naki_tile.owner = 2
        self.player.kabe.append(
            Huro(Naki.PON, naki_tile,
                 [Tile(Suit.JIHAI.value, Jihai.HATSU.value)
                  for i in range(1, 4)]))
        self.player.agari_tile = Tile(Suit.SOUZU.value, 6)
        self.player.menzenchin = False

        yaku_types = TeYaku(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.ryuuiisou(), True)
        self.assertEqual(yaku_types.total_yaku, ['ryuuiisou'])
        self.assertEqual(yaku_types.total_han, 0)
        self.assertEqual(yaku_types.yakuman_count, 1)

    def test_no_kokushi_musou(self):  # 国士無双
        self.player.hand[Tile(Suit.SOUZU.value, 1).index] += 1
        self.player.hand[Tile(Suit.SOUZU.value, 9).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 1).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 9).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 1).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 9).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.CHUN.value).index] += 2
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.TON.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.NAN.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.SHAA.value).index] += 2
        self.player.agari_tile = Tile(Suit.JIHAI.value, Jihai.PEI.value)

        yaku_types = TeYaku(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.kokushi_musou(), False)
        self.assertEqual(yaku_types.total_yaku, [])
        self.assertEqual(yaku_types.total_han, 0)
        self.assertEqual(yaku_types.yakuman_count, 0)

    def test_kokushi_musou(self):  # 国士無双 single wait
        self.player.hand[Tile(Suit.SOUZU.value, 1).index] += 1
        self.player.hand[Tile(Suit.SOUZU.value, 9).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 1).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 9).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 1).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 9).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HAKU.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HATSU.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.CHUN.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.TON.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.NAN.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.SHAA.value).index] += 2
        self.player.agari_tile = Tile(Suit.JIHAI.value, Jihai.PEI.value)

        yaku_types = TeYaku(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.kokushi_musou(), True)
        self.assertEqual(yaku_types.total_yaku, ['kokushi musou'])
        self.assertEqual(yaku_types.total_han, 0)
        self.assertEqual(yaku_types.yakuman_count, 1)

    def test_kokushi_musou_13_way(self):  # 国士無双 13-way wait
        self.player.hand[Tile(Suit.SOUZU.value, 1).index] += 1
        self.player.hand[Tile(Suit.SOUZU.value, 9).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 1).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 9).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 1).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 9).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HAKU.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HATSU.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.CHUN.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.TON.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.NAN.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.SHAA.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.PEI.value).index] += 1
        self.player.agari_tile = Tile(Suit.JIHAI.value, Jihai.PEI.value)

        yaku_types = TeYaku(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.kokushi_musou(), True)
        self.assertEqual(yaku_types.total_yaku, ['kokushi musou 13-way wait'])
        self.assertEqual(yaku_types.total_han, 0)
        self.assertEqual(yaku_types.yakuman_count, 2)

    def test_chuuren_poutou(self):  # 九連宝燈 or 純正九蓮宝燈
        ...

    def test_no_toitoihou(self):  # 対々和
        self.player.hand[Tile(Suit.PINZU.value, 8).index] += 1
        self.player.hand[Tile(Suit.PINZU.value, 9).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HAKU.value).index] += 2
        for tile_rank in range(2, 5):
            naki_tile = Tile(Suit.MANZU.value, tile_rank)
            naki_tile.owner = 2
            self.player.kabe.append(
                Huro(Naki.PON, naki_tile,
                     [Tile(Suit.MANZU.value, tile_rank) for i in range(1, 4)]))

        self.player.agari_tile = Tile(Suit.PINZU.value, 7)

        yaku_types = TeYaku(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.toitoihou(), False)
        self.assertEqual(yaku_types.total_yaku, [])
        self.assertEqual(yaku_types.total_han, 0)

    def test_no_toitoihou_2(self):  # 対々和
        self.player.hand[Tile(Suit.PINZU.value, 9).index] += 2
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HAKU.value).index] += 2
        for tile_rank in range(2, 4):
            naki_tile = Tile(Suit.MANZU.value, tile_rank)
            naki_tile.owner = 2
            self.player.kabe.append(
                Huro(Naki.PON, naki_tile,
                     [Tile(Suit.MANZU.value, tile_rank) for i in range(1, 4)]))
        naki_tile = Tile(Suit.SOUZU.value, 1)
        naki_tile.owner = 3
        self.player.kabe.append(
            Huro(Naki.CHII, naki_tile,
                 [Tile(Suit.SOUZU.value, i) for i in range(1, 4)]))

        self.player.agari_tile = Tile(Suit.JIHAI.value, Jihai.HAKU.value)

        yaku_types = TeYaku(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.toitoihou(), False)
        self.assertEqual(yaku_types.total_yaku, [])
        self.assertEqual(yaku_types.total_han, 0)

    def test_toitoihou(self):  # 対々和
        self.player.hand[Tile(Suit.PINZU.value, 9).index] += 2
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HAKU.value).index] += 2
        for tile_rank in range(2, 5):
            naki_tile = Tile(Suit.MANZU.value, tile_rank)
            naki_tile.owner = 2
            self.player.kabe.append(
                Huro(Naki.PON, naki_tile,
                     [Tile(Suit.MANZU.value, tile_rank) for i in range(1, 4)]))

        self.player.agari_tile = Tile(Suit.JIHAI.value, Jihai.HAKU.value)

        yaku_types = TeYaku(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.toitoihou(), True)
        self.assertEqual(yaku_types.total_yaku, ['toitoihou'])
        self.assertEqual(yaku_types.total_han, 2)

    def test_no_chiitoitsu(self):  # 七対子
        self.player.hand[Tile(Suit.PINZU.value, 9).index] += 2
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HAKU.value).index] += 2
        for tile_rank in range(2, 5):
            naki_tile = Tile(Suit.MANZU.value, tile_rank)
            naki_tile.owner = 2
            self.player.kabe.append(
                Huro(Naki.PON, naki_tile,
                     [Tile(Suit.MANZU.value, tile_rank) for i in range(1, 4)]))

        self.player.agari_tile = Tile(Suit.JIHAI.value, Jihai.HAKU.value)

        yaku_types = TeYaku(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.chiitoitsu(), False)
        self.assertEqual(yaku_types.total_yaku, [])
        self.assertEqual(yaku_types.total_han, 0)

    def test_chiitoitsu(self):  # 七対子
        self.player.hand[Tile(Suit.PINZU.value, 8).index] += 2
        self.player.hand[Tile(Suit.PINZU.value, 9).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 2).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 3).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 4).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 5).index] += 2
        self.player.hand[Tile(Suit.SOUZU.value, 1).index] += 1
        self.player.agari_tile = Tile(Suit.SOUZU.value, 1)

        yaku_types = TeYaku(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.chiitoitsu(), True)
        self.assertEqual(yaku_types.total_yaku, ['chiitoitsu'])
        self.assertEqual(yaku_types.total_han, 2)

    def test_no_ikkitsuukan(self):  # 一気通貫
        for i in range(4, 10):
            self.player.hand[Tile(Suit.PINZU.value, i).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 2).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 3).index] += 3
        self.player.hand[Tile(Suit.SOUZU.value, 5).index] += 2
        self.player.agari_tile = Tile(Suit.SOUZU.value, 5)

        yaku_types = TeYaku(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.ikkitsuukan(), False)
        self.assertEqual(yaku_types.total_yaku, [])
        self.assertEqual(yaku_types.total_han, 0)

    def test_ikkitsuukan_closed(self):  # 一気通貫
        for i in range(1, 10):
            self.player.hand[Tile(Suit.PINZU.value, i).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 3).index] += 2
        self.player.hand[Tile(Suit.SOUZU.value, 5).index] += 2
        self.player.agari_tile = Tile(Suit.SOUZU.value, 5)

        yaku_types = TeYaku(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.ikkitsuukan(), True)
        self.assertEqual(yaku_types.total_yaku, ['ikkitsuukan'])
        self.assertEqual(yaku_types.total_han, 2)

    def test_ikkitsuukan_opened(self):  # 一気通貫
        # 非門清
        for i in range(4, 10):
            self.player.hand[Tile(Suit.PINZU.value, i).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 3).index] += 2
        self.player.hand[Tile(Suit.SOUZU.value, 5).index] += 2
        self.player.agari_tile = Tile(Suit.SOUZU.value, 5)
        naki_tile = Tile(Suit.PINZU.value, 2)
        naki_tile.owner = 3
        self.player.kabe.append(
            Huro(Naki.CHII, naki_tile,
                 [Tile(Suit.PINZU.value, i) for i in range(1, 4)]))
        self.player.menzenchin = False

        yaku_types = TeYaku(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.ikkitsuukan(), True)
        self.assertEqual(yaku_types.total_yaku, ['ikkitsuukan'])
        self.assertEqual(yaku_types.total_han, 1)

    def test_pinfu(self):  # 平和
        ...

    def test_no_tanyao_closed(self):  # 断么九
        for i in range(1, 7):
            self.player.hand[Tile(Suit.PINZU.value, i).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 3).index] += 3
        self.player.hand[Tile(Suit.MANZU.value, 8).index] += 2
        self.player.hand[Tile(Suit.SOUZU.value, 5).index] += 2
        self.player.agari_tile = Tile(Suit.SOUZU.value, 5)

        yaku_types = TeYaku(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.tanyao(), False)
        self.assertEqual(yaku_types.total_yaku, [])
        self.assertEqual(yaku_types.total_han, 0)

    def test_no_tanyao_opened(self):  # 断么九
        for i in range(2, 8):
            self.player.hand[Tile(Suit.PINZU.value, i).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 8).index] += 2
        self.player.hand[Tile(Suit.SOUZU.value, 5).index] += 2
        naki_tile = Tile(Suit.PINZU.value, 9)
        naki_tile.owner = 3
        self.player.kabe.append(
            Huro(Naki.PON, naki_tile,
                 [Tile(Suit.PINZU.value, 9) for i in range(1, 4)]))
        self.player.menzenchin = False
        self.player.agari_tile = Tile(Suit.SOUZU.value, 5)

        yaku_types = TeYaku(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.tanyao(), False)
        self.assertEqual(yaku_types.total_yaku, [])
        self.assertEqual(yaku_types.total_han, 0)

    def test_tanyao_closed(self):  # 断么九
        for i in range(2, 8):
            self.player.hand[Tile(Suit.PINZU.value, i).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 3).index] += 3
        self.player.hand[Tile(Suit.MANZU.value, 8).index] += 2
        self.player.hand[Tile(Suit.SOUZU.value, 5).index] += 2
        self.player.agari_tile = Tile(Suit.SOUZU.value, 5)

        yaku_types = TeYaku(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.tanyao(), True)
        self.assertEqual(yaku_types.total_yaku, ['tanyao'])
        self.assertEqual(yaku_types.total_han, 1)

    def test_tanyao_opened(self):  # 断么九
        for i in range(2, 8):
            self.player.hand[Tile(Suit.PINZU.value, i).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 8).index] += 2
        self.player.hand[Tile(Suit.SOUZU.value, 5).index] += 2
        naki_tile = Tile(Suit.PINZU.value, 2)
        naki_tile.owner = 3
        self.player.kabe.append(
            Huro(Naki.PON, naki_tile,
                 [Tile(Suit.PINZU.value, 2) for i in range(1, 4)]))
        self.player.menzenchin = False
        self.player.agari_tile = Tile(Suit.SOUZU.value, 5)

        yaku_types = TeYaku(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.tanyao(), True)
        self.assertEqual(yaku_types.total_yaku, ['tanyao'])
        self.assertEqual(yaku_types.total_han, 1)


class TestYakuhai(unittest.TestCase):

    def setUp(self):
        self.player = Player('test', 0)
        self.stack = Stack
        self.bakaze = Jihai.TON

    def test_no_daisangen(self):  # 大三元
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HAKU.value).index] += 2
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HATSU.value).index] += 3
        self.player.hand[Tile(Suit.SOUZU.value, 6).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 8).index] += 3
        naki_tile = Tile(Suit.JIHAI.value, Jihai.CHUN.value)
        naki_tile.owner = 2
        self.player.kabe.append(
            Huro(Naki.PON, naki_tile,
                 [Tile(Suit.JIHAI.value, Jihai.CHUN.value)
                  for i in range(1, 4)]))
        self.player.agari_tile = Tile(Suit.SOUZU.value, 6)
        self.player.menzenchin = False

        yaku_types = Yakuhai(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.daisangen(), False)
        self.assertEqual(yaku_types.total_yaku, [])
        self.assertEqual(yaku_types.total_han, 0)
        self.assertEqual(yaku_types.yakuman_count, 0)

    def test_daisangen(self):  # 大三元
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HAKU.value).index] += 3
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HATSU.value).index] += 3
        self.player.hand[Tile(Suit.SOUZU.value, 6).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 8).index] += 2
        naki_tile = Tile(Suit.JIHAI.value, Jihai.CHUN.value)
        naki_tile.owner = 2
        self.player.kabe.append(
            Huro(Naki.PON, naki_tile,
                 [Tile(Suit.JIHAI.value, Jihai.CHUN.value)
                  for i in range(1, 4)]))
        self.player.agari_tile = Tile(Suit.SOUZU.value, 6)
        self.player.menzenchin = False

        yaku_types = Yakuhai(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.daisangen(), True)
        self.assertEqual(yaku_types.total_yaku, ['daisangen'])
        self.assertEqual(yaku_types.total_han, 0)
        self.assertEqual(yaku_types.yakuman_count, 1)

    def test_no_tsuuiisou(self):  # 字一色
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HAKU.value).index] += 3
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HATSU.value).index] += 3
        self.player.hand[Tile(Suit.SOUZU.value, 6).index] += 2
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.SHAA.value).index] += 2
        naki_tile = Tile(Suit.JIHAI.value, Jihai.CHUN.value)
        naki_tile.owner = 2
        self.player.kabe.append(
            Huro(Naki.PON, naki_tile,
                 [Tile(Suit.JIHAI.value, Jihai.CHUN.value)
                  for i in range(1, 4)]))
        self.player.agari_tile = Tile(Suit.JIHAI.value, Jihai.SHAA.value)
        self.player.menzenchin = False

        yaku_types = Yakuhai(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.tsuuiisou(), False)
        self.assertEqual(yaku_types.total_yaku, [])
        self.assertEqual(yaku_types.total_han, 0)
        self.assertEqual(yaku_types.yakuman_count, 0)

    def test_tsuuiisou(self):  # 字一色
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HAKU.value).index] += 3
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HATSU.value).index] += 3
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.TON.value).index] += 2
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.SHAA.value).index] += 2
        naki_tile = Tile(Suit.JIHAI.value, Jihai.CHUN.value)
        naki_tile.owner = 2
        self.player.kabe.append(
            Huro(Naki.PON, naki_tile,
                 [Tile(Suit.JIHAI.value, Jihai.CHUN.value)
                  for i in range(1, 4)]))
        self.player.agari_tile = Tile(Suit.JIHAI.value, Jihai.SHAA.value)
        self.player.menzenchin = False

        yaku_types = Yakuhai(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.tsuuiisou(), True)
        self.assertEqual(yaku_types.total_yaku, ['tsuuiisou'])
        self.assertEqual(yaku_types.total_han, 0)
        self.assertEqual(yaku_types.yakuman_count, 1)

    def test_no_daisuushii(self):  # 大四喜
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.CHUN.value).index] += 3
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.NAN.value).index] += 3
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.SHAA.value).index] += 2
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HAKU.value).index] += 2
        naki_tile = Tile(Suit.JIHAI.value, Jihai.PEI.value)
        naki_tile.owner = 2
        self.player.kabe.append(
            Huro(Naki.DAMINKAN, naki_tile,
                 [Tile(Suit.JIHAI.value, Jihai.PEI.value)
                  for i in range(1, 5)]))
        self.player.agari_tile = Tile(Suit.JIHAI.value, Jihai.SHAA.value)
        self.player.menzenchin = False

        yaku_types = Yakuhai(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.daisuushii(), False)
        self.assertEqual(yaku_types.total_yaku, [])
        self.assertEqual(yaku_types.total_han, 0)
        self.assertEqual(yaku_types.yakuman_count, 0)

    def test_daisuushii(self):  # 大四喜
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.TON.value).index] += 3
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.NAN.value).index] += 3
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.SHAA.value).index] += 2
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HAKU.value).index] += 2
        naki_tile = Tile(Suit.JIHAI.value, Jihai.PEI.value)
        naki_tile.owner = 2
        self.player.kabe.append(
            Huro(Naki.DAMINKAN, naki_tile,
                 [Tile(Suit.JIHAI.value, Jihai.PEI.value)
                  for i in range(1, 5)]))
        self.player.agari_tile = Tile(Suit.JIHAI.value, Jihai.SHAA.value)
        self.player.menzenchin = False

        yaku_types = Yakuhai(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.daisuushii(), True)
        self.assertEqual(yaku_types.total_yaku, ['daisuushii'])
        self.assertEqual(yaku_types.total_han, 0)
        self.assertEqual(yaku_types.yakuman_count, 1)

    def test_shousuushii(self):  # 小四喜
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.TON.value).index] += 3
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.NAN.value).index] += 3
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.SHAA.value).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HAKU.value).index] += 3
        naki_tile = Tile(Suit.JIHAI.value, Jihai.PEI.value)
        naki_tile.owner = 2
        self.player.kabe.append(
            Huro(Naki.DAMINKAN, naki_tile,
                 [Tile(Suit.JIHAI.value, Jihai.PEI.value)
                  for i in range(1, 5)]))
        self.player.agari_tile = Tile(Suit.JIHAI.value, Jihai.SHAA.value)
        self.player.menzenchin = False

        yaku_types = Yakuhai(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.shousuushii(), True)
        self.assertEqual(yaku_types.total_yaku, ['shousuushii'])
        self.assertEqual(yaku_types.total_han, 0)
        self.assertEqual(yaku_types.yakuman_count, 1)

    def test_no_shousangen(self):  # 小三元
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.PEI.value).index] += 2
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HATSU.value).index] += 3
        self.player.hand[Tile(Suit.SOUZU.value, 6).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 8).index] += 3
        naki_tile = Tile(Suit.JIHAI.value, Jihai.CHUN.value)
        naki_tile.owner = 2
        self.player.kabe.append(
            Huro(Naki.PON, naki_tile,
                 [Tile(Suit.JIHAI.value, Jihai.CHUN.value)
                  for i in range(1, 4)]))
        self.player.agari_tile = Tile(Suit.SOUZU.value, 6)
        self.player.menzenchin = False

        yaku_types = Yakuhai(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.shousangen(), False)
        self.assertEqual(yaku_types.total_yaku, [])
        self.assertEqual(yaku_types.total_han, 0)
        self.assertEqual(yaku_types.yakuman_count, 0)

    def test_shousangen(self):  # 小三元
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HAKU.value).index] += 2
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HATSU.value).index] += 3
        self.player.hand[Tile(Suit.SOUZU.value, 6).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 8).index] += 3
        naki_tile = Tile(Suit.JIHAI.value, Jihai.CHUN.value)
        naki_tile.owner = 2
        self.player.kabe.append(
            Huro(Naki.PON, naki_tile,
                 [Tile(Suit.JIHAI.value, Jihai.CHUN.value)
                  for i in range(1, 4)]))
        self.player.agari_tile = Tile(Suit.SOUZU.value, 6)
        self.player.menzenchin = False

        yaku_types = Yakuhai(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.shousangen(), True)
        self.assertEqual(yaku_types.total_yaku, ['shousangen'])
        self.assertEqual(yaku_types.total_han, 2)
        self.assertEqual(yaku_types.yakuman_count, 0)

    def test_yakuhai(self):  # 役牌
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.NAN.value).index] += 2
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.TON.value).index] += 3
        self.player.hand[Tile(Suit.SOUZU.value, 6).index] += 2
        self.player.hand[Tile(Suit.MANZU.value, 8).index] += 3
        naki_tile = Tile(Suit.JIHAI.value, Jihai.CHUN.value)
        naki_tile.owner = 2
        self.player.kabe.append(
            Huro(Naki.PON, naki_tile,
                 [Tile(Suit.JIHAI.value, Jihai.CHUN.value)
                  for i in range(1, 4)]))
        self.player.agari_tile = Tile(Suit.SOUZU.value, 6)
        self.player.menzenchin = False

        yaku_types = Yakuhai(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.yakuhai(), True)
        self.assertEqual(yaku_types.total_yaku,
                         ['sangenpai_CHUN', 'bakaze_TON', 'jikaze_TON'])
        self.assertEqual(yaku_types.total_han, 3)
        self.assertEqual(yaku_types.yakuman_count, 0)


class TestPeikou(unittest.TestCase):

    def setUp(self):
        self.player = Player('test', 0)
        self.stack = Stack
        self.bakaze = Jihai.TON

    def test_no_ryanpeikou(self):  # 二盃口
        for i in range(1, 4):
            self.player.hand[Tile(Suit.MANZU.value, i).index] += 2
        for i in range(4, 7):
            self.player.hand[Tile(Suit.MANZU.value, i).index] += 1
        self.player.hand[Tile(Suit.SOUZU.value, 5).index] += 1
        naki_tile = Tile(Suit.MANZU.value, 5)
        naki_tile.owner = 0
        self.player.kabe.append(
            Huro(Naki.CHII, naki_tile,
                 [Tile(Suit.MANZU.value, i) for i in range(4, 7)]))
        self.player.agari_tile = Tile(Suit.SOUZU.value, 5)

        yaku_types = Peikou(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.ryanpeikou(), False)
        self.assertEqual(yaku_types.total_yaku, [])
        self.assertEqual(yaku_types.total_han, 0)

    def test_ryanpeikou(self):  # 二盃口
        for i in range(1, 7):
            self.player.hand[Tile(Suit.MANZU.value, i).index] += 2
        self.player.hand[Tile(Suit.SOUZU.value, 5).index] += 1
        self.player.agari_tile = Tile(Suit.SOUZU.value, 5)

        yaku_types = Peikou(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.ryanpeikou(), True)
        self.assertEqual(yaku_types.total_yaku, ['ryanpeikou'])
        self.assertEqual(yaku_types.total_han, 3)

    def test_no_iipeikou(self):  # 一盃口
        for i in range(1, 7):
            self.player.hand[Tile(Suit.MANZU.value, i).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.NAN.value).index] += 3
        self.player.hand[Tile(Suit.SOUZU.value, 5).index] += 1
        naki_tile = Tile(Suit.MANZU.value, 5)
        naki_tile.owner = 0
        self.player.kabe.append(
            Huro(Naki.CHII, naki_tile,
                 [Tile(Suit.MANZU.value, i) for i in range(4, 7)]))
        self.player.agari_tile = Tile(Suit.SOUZU.value, 5)

        yaku_types = Peikou(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.iipeikou(), False)
        self.assertEqual(yaku_types.total_yaku, [])
        self.assertEqual(yaku_types.total_han, 0)

    def test_iipeikou(self):  # 一盃口
        for i in range(1, 4):
            self.player.hand[Tile(Suit.MANZU.value, i).index] += 2
        for i in range(4, 7):
            self.player.hand[Tile(Suit.MANZU.value, i).index] += 1
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.NAN.value).index] += 3
        self.player.hand[Tile(Suit.SOUZU.value, 5).index] += 1
        self.player.agari_tile = Tile(Suit.SOUZU.value, 5)

        yaku_types = Peikou(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.iipeikou(), True)
        self.assertEqual(yaku_types.total_yaku, ['iipeikou'])
        self.assertEqual(yaku_types.total_han, 1)


class TestChanta(unittest.TestCase):

    def setUp(self):
        self.player = Player('test', 0)
        self.stack = Stack
        self.bakaze = Jihai.TON

    def test_no_chinroutou(self):  # 清老頭
        self.player.hand[Tile(Suit.MANZU.value, 2).index] += 3
        self.player.hand[Tile(Suit.MANZU.value, 9).index] += 3
        self.player.hand[Tile(Suit.SOUZU.value, 1).index] += 3
        self.player.hand[Tile(Suit.SOUZU.value, 9).index] += 3
        self.player.hand[Tile(Suit.PINZU.value, 1).index] += 1

        naki_tile = Tile(Suit.SOUZU.value, 9)
        naki_tile.owner = 2
        self.player.kabe.append(
            Huro(Naki.PON, naki_tile,
                 [Tile(Suit.SOUZU.value, 9) for i in range(1, 4)]))
        self.player.agari_tile = Tile(Suit.PINZU.value, 1)

        yaku_types = Chanta(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.chinroutou(), False)
        self.assertEqual(yaku_types.total_yaku, [])
        self.assertEqual(yaku_types.total_han, 0)
        self.assertEqual(yaku_types.yakuman_count, 0)

    def test_chinroutou(self):  # 清老頭
        self.player.hand[Tile(Suit.MANZU.value, 1).index] += 3
        self.player.hand[Tile(Suit.MANZU.value, 9).index] += 3
        self.player.hand[Tile(Suit.SOUZU.value, 1).index] += 3
        self.player.hand[Tile(Suit.SOUZU.value, 9).index] += 3
        self.player.hand[Tile(Suit.PINZU.value, 1).index] += 1

        naki_tile = Tile(Suit.SOUZU.value, 9)
        naki_tile.owner = 2
        self.player.kabe.append(
            Huro(Naki.PON, naki_tile,
                 [Tile(Suit.SOUZU.value, 9) for i in range(1, 4)]))
        self.player.agari_tile = Tile(Suit.PINZU.value, 1)

        yaku_types = Chanta(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.chinroutou(), True)
        self.assertEqual(yaku_types.total_yaku, ['chinroutou'])
        self.assertEqual(yaku_types.total_han, 0)
        self.assertEqual(yaku_types.yakuman_count, 1)

    def test_no_honroutou(self):  # 混老頭
        self.player.hand[Tile(Suit.MANZU.value, 2).index] += 3
        self.player.hand[Tile(Suit.MANZU.value, 9).index] += 3
        self.player.hand[Tile(Suit.SOUZU.value, 1).index] += 3
        self.player.hand[Tile(Suit.SOUZU.value, 9).index] += 3
        self.player.hand[Tile(Suit.PINZU.value, 1).index] += 1

        naki_tile = Tile(Suit.SOUZU.value, 9)
        naki_tile.owner = 2
        self.player.kabe.append(
            Huro(Naki.PON, naki_tile,
                 [Tile(Suit.SOUZU.value, 9) for i in range(1, 4)]))
        self.player.agari_tile = Tile(Suit.PINZU.value, 1)

        yaku_types = Chanta(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.honroutou(), False)
        self.assertEqual(yaku_types.total_yaku, [])
        self.assertEqual(yaku_types.total_han, 0)
        self.assertEqual(yaku_types.yakuman_count, 0)

    def test_honroutou(self):  # 混老頭
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.CHUN.value).index] += 3
        self.player.hand[Tile(Suit.MANZU.value, 9).index] += 3
        self.player.hand[Tile(Suit.SOUZU.value, 1).index] += 3
        self.player.hand[Tile(Suit.SOUZU.value, 9).index] += 3
        self.player.hand[Tile(Suit.PINZU.value, 1).index] += 1

        naki_tile = Tile(Suit.SOUZU.value, 9)
        naki_tile.owner = 2
        self.player.kabe.append(
            Huro(Naki.PON, naki_tile,
                 [Tile(Suit.SOUZU.value, 9) for i in range(1, 4)]))
        self.player.agari_tile = Tile(Suit.PINZU.value, 1)

        yaku_types = Chanta(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.honroutou(), True)
        self.assertEqual(yaku_types.total_yaku, ['honroutou'])
        self.assertEqual(yaku_types.total_han, 2)
        self.assertEqual(yaku_types.yakuman_count, 0)
    
    def test_junchantaiyaochuu(self):  # 純全帯么九
        ...

    def test_chanta(self):  # 混全帯么九
        ...


class TestKoutsu(unittest.TestCase):

    def setUp(self):
        self.player = Player('test', 0)
        self.stack = Stack
        self.bakaze = Jihai.TON

    def test_suuankou(self):  # 四暗刻 or 四暗刻単騎
        ...

    def test_suukantsu(self):  # 四槓子
        ...

    def test_sanankou(self):  # 三暗刻
        ...

    def test_sankantsu(self):  # 三槓子
        ...
