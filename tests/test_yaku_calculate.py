import unittest

from mahjong.components import Stack, Jihai, Suit, Tile
from mahjong.player import Player
from mahjong.yaku_calculator import YakuCalculator
from mahjong.naki_and_actions import check_tenpai


class TestYakuCalculator(unittest.TestCase):
    def setUp(self):
        self.player = Player('test player', 0)
        self.stack = Stack()
        self.bakaze = Jihai.TON
        for i in range(2, 8):
            self.player.hand[Tile(Suit.PINZU.value, i).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 3).index] += 3
        self.player.hand[Tile(Suit.MANZU.value, 9).index] += 2
        self.player.hand[Tile(Suit.SOUZU.value, 5).index] += 2
        self.player.agari_tile = Tile(Suit.SOUZU.value, 5)

    def test_filter_yaku(self):
        machi_tiles = check_tenpai(self.player.hand, self.player.kabe)
        yaku_calc = YakuCalculator(
            self.player, self.stack, self.bakaze, False,
            machi_tiles, self.player.agari_tile)
        possible_yakus = [
            ('ryanpeikou', 3),
            ('chiitoitsu', 2),
            ('menzen_tsumo', 1),
        ]
        final_yakus = yaku_calc.filter_yaku(possible_yakus)
        self.assertEqual(len(final_yakus), 2)
        final_yaku_answer = [
            ('ryanpeikou', 3),
            ('menzen_tsumo', 1),
        ]
        self.assertEqual(final_yakus, final_yaku_answer)

    def test_menzen_tsumo(self):
        machi_tiles = check_tenpai(self.player.hand, self.player.kabe)
        yaku_calc = YakuCalculator(
            self.player, self.stack, self.bakaze, False,
            machi_tiles, self.player.agari_tile)
        total_han, fu = yaku_calc.calculate()
        self.assertEqual(total_han, 1)
        self.assertEqual(fu, 40)
