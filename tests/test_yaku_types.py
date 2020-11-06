import unittest

from mahjong.components import Tile, Suit, Jihai, Naki, Huro
from mahjong.player import Player
from mahjong.components import Stack
from mahjong.yaku_types import TeYaku


class TestTeYaku(unittest.TestCase):

    def setUp(self):
        self.player = Player('test', 0)
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
        self.player.agari_tile = Tile(Suit.SOUZU.value, 5)

        self.stack = Stack
        self.bakaze = Jihai.TON

    def test_no_ikkitsuukan(self):  # 一気通貫
        self.player.hand[Tile(Suit.PINZU.value, 1).index] += 2
        self.player.hand[Tile(Suit.PINZU.value, 2).index] -= 1
        self.player.hand[Tile(Suit.PINZU.value, 3).index] -= 1
        yaku_types = TeYaku(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.ikkitsuukan(), False)

    def test_ikkitsuukan_closed(self):  # 一気通貫
        yaku_types = TeYaku(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.ikkitsuukan(), True)
        self.assertEqual(yaku_types.total_yaku, ['ikkitsuukan'])
        self.assertEqual(yaku_types.total_han, 2)

    def test_ikkitsuukan_opened(self):  # 一気通貫
        # 非門清
        self.player.hand[Tile(Suit.PINZU.value, 1).index] -= 1
        self.player.hand[Tile(Suit.PINZU.value, 2).index] -= 1
        self.player.hand[Tile(Suit.PINZU.value, 3).index] -= 1
        naki_tile = Tile(Suit.PINZU.value, 2)
        naki_tile.owner = 3
        self.player.kabe.append(
            Huro(Naki.CHII,
                 naki_tile,
                 [Tile(Suit.PINZU.value, i) for i in range(1, 4)]))
        self.player.menzenchin = False

        yaku_types = TeYaku(self.player, self.stack, self.bakaze, True)
        self.assertEqual(yaku_types.ikkitsuukan(), True)
        self.assertEqual(yaku_types.total_yaku, ['ikkitsuukan'])
        self.assertEqual(yaku_types.total_han, 1)
