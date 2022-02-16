import unittest

from mahjong.components import Stack, Jihai, Suit, Tile
from mahjong.player import Player
from mahjong.yaku_calculator import YakuCalculator
from mahjong.naki_and_actions import check_tenpai


class TestYakuCalculator(unittest.TestCase):
    def setUp(self):
        self.player = Player('test player', 0)
        self.stack = Stack()
        self.stack.doras = [Tile(Suit.PINZU.value, 3)]
        self.bakaze = Jihai.TON
        for i in range(2, 8):
            self.player.hand[Tile(Suit.PINZU.value, i).index] += 1
        self.player.hand[Tile(Suit.MANZU.value, 3).index] += 3
        self.player.hand[Tile(Suit.MANZU.value, 9).index] += 2
        self.player.hand[Tile(Suit.SOUZU.value, 5).index] += 2
        self.player.agari_tile = Tile(Suit.SOUZU.value, 5)
        self.machi_tiles = check_tenpai(self.player.hand, self.player.kabe)

    def test_filter_yaku_1(self):
        yaku_calc = YakuCalculator(
            self.player, self.stack, self.bakaze, False,
            self.machi_tiles, self.player.agari_tile)
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

    def test_filter_yaku_2(self):
        yaku_calc = YakuCalculator(
            self.player, self.stack, self.bakaze, False,
            self.machi_tiles, self.player.agari_tile)
        possible_yakus = [
            ('ryanpeikou', 3),
            ('menzen_tsumo', 1),
        ]
        final_yakus = yaku_calc.filter_yaku(possible_yakus)
        self.assertEqual(len(final_yakus), 2)
        final_yaku_answer = [
            ('ryanpeikou', 3),
            ('menzen_tsumo', 1),
        ]
        self.assertEqual(final_yakus, final_yaku_answer)

    def test_filter_yaku_3(self):
        yaku_calc = YakuCalculator(
            self.player, self.stack, self.bakaze, False,
            self.machi_tiles, self.player.agari_tile)
        possible_yakus = [
            ('ryanpeikou', 3),
            ('toitoihou', 2),
            ('sanankou', 2)
        ]
        final_yakus = yaku_calc.filter_yaku(possible_yakus)
        self.assertEqual(len(final_yakus), 1)
        final_yaku_answer = [
            ('ryanpeikou', 3)
        ]
        self.assertEqual(final_yakus, final_yaku_answer)

    def test_menzen_tsumo(self):
        yaku_calc = YakuCalculator(
            self.player, self.stack, self.bakaze, False,
            self.machi_tiles, self.player.agari_tile)
        total_han, fu = yaku_calc.calculate()
        self.assertEqual(total_han, 2)  # menzen tsumo and dora
        self.assertEqual(fu, 40)

    def test_check_doras(self):
        yaku_calc = YakuCalculator(
            self.player, self.stack, self.bakaze, False,
            self.machi_tiles, self.player.agari_tile)
        dora = yaku_calc.check_doras()
        self.assertEqual(dora, 1)
