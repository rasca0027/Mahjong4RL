import unittest

from mahjong.components import Tile, Suit, Stack, Jihai


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

    def test_rank_setter_error2(self):
        self.tile.suit = 0
        with self.assertRaises(ValueError):
            self.tile.rank = 9

    def test_rank_setter_error3(self):
        self.tile.suit = 1
        with self.assertRaises(ValueError):
            self.tile.rank = 10

    def test_index(self):
        self.assertEqual(self.tile.index, 12)

    def test_from_index(self):
        self.assertEqual(self.tile, Tile.from_index(self.tile.index))

    def test_eq(self):
        self.assertEqual(self.tile == Tile(Suit.MANZU.value, 2), True)
        self.assertEqual(self.tile == Tile(Suit.MANZU.value, 3), False)

    def test_lt(self):
        self.assertEqual(self.tile < Tile(Suit.MANZU.value, 3), True)
        self.assertEqual(self.tile < Tile(Suit.MANZU.value, 1), False)

    def test_gt(self):
        self.assertEqual(self.tile > Tile(Suit.MANZU.value, 1), True)
        self.assertEqual(self.tile > Tile(Suit.MANZU.value, 3), False)


class TestStack(unittest.TestCase):

    def setUp(self):
        self.test_stack = Stack()

    def test_tiles_in_stack(self):
        self.assertEqual(len(self.test_stack.stack), 136)
        self.assertEqual(len(self.test_stack.dora_indicator), 1)
        self.assertEqual(len(self.test_stack.unadora_indicator), 1)
        self.assertEqual(len(self.test_stack.dora), 1)
        self.assertEqual(len(self.test_stack.unadora), 1)
        self.assertEqual(next(self.test_stack.playling_wall),
                         self.test_stack.stack[0])
        self.assertEqual(next(self.test_stack.rinshanpai),
                         self.test_stack.stack[-1])

    def test_add_dora(self):
        self.test_stack.add_dora_indicator()
        self.assertEqual(len(self.test_stack.dora_indicator), 2)
        self.assertEqual(len(self.test_stack.unadora_indicator), 2)
        self.assertEqual(len(self.test_stack.dora), 2)
        self.assertEqual(len(self.test_stack.unadora), 2)

        self.assertEqual(self.test_stack.can_add_dora_indicator(), True)
        self.test_stack.dora_index = -12
        self.assertEqual(self.test_stack.can_add_dora_indicator(), False)

    def test_compute_dora(self):
        dora_indicator1 = Tile(Suit.JIHAI.value, Jihai.HAKU.value)
        dora1 = Tile(Suit.JIHAI.value, Jihai.HATSU.value)
        dora_indicator2 = Tile(Suit.JIHAI.value, Jihai.CHUN.value)
        dora2 = Tile(Suit.JIHAI.value, Jihai.HAKU.value)
        dora_indicator3 = Tile(Suit.JIHAI.value, Jihai.TON.value)
        dora3 = Tile(Suit.JIHAI.value, Jihai.NAN.value)
        dora_indicator4 = Tile(Suit.JIHAI.value, Jihai.PEI.value)
        dora4 = Tile(Suit.JIHAI.value, Jihai.TON.value)
        dora_indicator5 = Tile(Suit.MANZU.value, 1)
        dora5 = Tile(Suit.MANZU.value, 2)
        dora_indicator6 = Tile(Suit.SOUZU.value, 9)
        dora6 = Tile(Suit.SOUZU.value, 1)
        self.assertEqual(Stack.compute_dora(dora_indicator1), dora1)
        self.assertEqual(Stack.compute_dora(dora_indicator2), dora2)
        self.assertEqual(Stack.compute_dora(dora_indicator3), dora3)
        self.assertEqual(Stack.compute_dora(dora_indicator4), dora4)
        self.assertEqual(Stack.compute_dora(dora_indicator5), dora5)
        self.assertEqual(Stack.compute_dora(dora_indicator6), dora6)
