import unittest

from mahjong.components import Suit, Jihai, Naki, Tile, Stack, Huro


class TestTile(unittest.TestCase):

    def setUp(self):
        self.tile = Tile(Suit.MANZU.value, 2)  # 二萬
        self.tile_2 = Tile(Suit.JIHAI.value, Jihai.CHUN.value)  # 紅中

    def test_str(self):
        tile_str = "2 MANZU"
        tile_str_2 = "CHUN"
        self.assertEqual(str(self.tile), tile_str)
        self.assertEqual(str(self.tile_2), tile_str_2)

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

    def test_owner_getter(self):
        self.tile.owner = 0
        self.assertEqual(self.tile.owner, 0)

    def test_owner_setter(self):
        self.tile.owner = 0
        with self.assertRaises(ValueError):
            self.tile.owner = 5

    def test_akadora(self):
        self.assertEqual(self.tile.akadora(), None)

    def test_index(self):
        self.assertEqual(self.tile.index, 12)

    def test_from_index(self):
        self.assertEqual(self.tile, Tile.from_index(self.tile.index))

    def test_next_tile(self):
        tile = Tile(Suit.MANZU.value, 1)
        self.assertEqual(tile.next_tile(), Tile(Suit.MANZU.value, 2))
        tile = Tile(Suit.MANZU.value, 9)
        self.assertEqual(tile.next_tile(), Tile(Suit.MANZU.value, 1))
        tile = Tile(Suit.JIHAI.value, 1)
        self.assertEqual(tile.next_tile(), Tile(Suit.JIHAI.value, 2))
        tile = Tile(Suit.JIHAI.value, 3)
        self.assertEqual(tile.next_tile(), Tile(Suit.JIHAI.value, 1))
        tile = Tile(Suit.JIHAI.value, 4)
        self.assertEqual(tile.next_tile(), Tile(Suit.JIHAI.value, 5))
        tile = Tile(Suit.JIHAI.value, 7)
        self.assertEqual(tile.next_tile(), Tile(Suit.JIHAI.value, 4))

    def test_prev_tile(self):
        tile = Tile(Suit.MANZU.value, 1)
        self.assertEqual(tile.prev_tile(), Tile(Suit.MANZU.value, 9))
        tile = Tile(Suit.MANZU.value, 9)
        self.assertEqual(tile.prev_tile(), Tile(Suit.MANZU.value, 8))
        tile = Tile(Suit.JIHAI.value, 1)
        self.assertEqual(tile.prev_tile(), Tile(Suit.JIHAI.value, 3))
        tile = Tile(Suit.JIHAI.value, 3)
        self.assertEqual(tile.prev_tile(), Tile(Suit.JIHAI.value, 2))
        tile = Tile(Suit.JIHAI.value, 4)
        self.assertEqual(tile.prev_tile(), Tile(Suit.JIHAI.value, 7))
        tile = Tile(Suit.JIHAI.value, 7)
        self.assertEqual(tile.prev_tile(), Tile(Suit.JIHAI.value, 6))

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
        self.assertEqual(len(self.test_stack.dora_indicators), 1)
        self.assertEqual(len(self.test_stack.doras), 1)
        self.assertEqual(len(self.test_stack.uradoras), 1)
        self.assertEqual(self.test_stack.draw(),
                         self.test_stack.stack[0])
        self.assertEqual(self.test_stack.draw(from_rinshan=True),
                         self.test_stack.stack[-1])

    def test_add_dora(self):
        self.test_stack.add_dora_indicator()
        self.assertEqual(len(self.test_stack.dora_indicators), 2)
        self.assertEqual(len(self.test_stack.uradora_indicators), 2)
        self.assertEqual(len(self.test_stack.doras), 2)
        self.assertEqual(len(self.test_stack.uradoras), 2)

    def test_add_dora_value_error(self):
        self.test_stack.add_dora_indicator()
        self.test_stack.add_dora_indicator()
        self.test_stack.add_dora_indicator()
        self.test_stack.add_dora_indicator()
        with self.assertRaises(ValueError):
            self.test_stack.add_dora_indicator()

    def test_get_dora_indicator(self):
        dora_indicator = self.test_stack.get_dora_indicator()
        self.assertEqual(dora_indicator, [self.test_stack.stack[-5]])

    def test_get_unadora_indicator(self):
        unadora_indicator = self.test_stack.get_unadora_indicator()
        self.assertEqual(unadora_indicator, [self.test_stack.stack[-6]])

    def test_get_dora(self):
        [dora] = self.test_stack.get_dora()
        self.assertEqual(dora, self.test_stack.stack[-5].next_tile())

    def test_get_unadora(self):
        [unadora] = self.test_stack.get_unadora()
        self.assertEqual(unadora, self.test_stack.stack[-6].next_tile())

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

    def test_draw_from_rinshan(self):
        self.test_stack.draw(from_rinshan=True)
        self.assertEqual(len(self.test_stack.playling_wall), 121)


class TestHuro(unittest.TestCase):

    def setUp(self):
        chii_tile = Tile(Suit.MANZU.value, 7)
        chii_tile.owner = 0
        self.huro_chii = Huro(Naki.CHII,
                              chii_tile,
                              [Tile(Suit.MANZU.value, 7),
                               Tile(Suit.MANZU.value, 8),
                               Tile(Suit.MANZU.value, 9)])
        pon_tile = Tile(Suit.MANZU.value, 2)
        pon_tile.owner = 0
        self.huro_pon = Huro(Naki.PON,
                             pon_tile,
                             [Tile(Suit.MANZU.value, 2) for i in range(3)])
        kan_tile = Tile(Suit.MANZU.value, 5)
        kan_tile.owner = 0
        self.huro_kan = Huro(Naki.DAMINKAN,
                             kan_tile,
                             [Tile(Suit.MANZU.value, 5) for i in range(4)])

    def test_naki_type(self):
        self.assertEqual(self.huro_kan.naki_type, Naki.DAMINKAN)

    def test_tiles_getter(self):
        tiles_in_huro = [Tile(Suit.MANZU.value, 7),
                         Tile(Suit.MANZU.value, 8),
                         Tile(Suit.MANZU.value, 9)]
        self.assertEqual(self.huro_chii.tiles, tiles_in_huro)

    def test_tiles_setter(self):
        new_tiles_in_huro = [Tile(Suit.MANZU.value, 5),
                             Tile(Suit.MANZU.value, 6),
                             Tile(Suit.MANZU.value, 7)]
        self.huro_chii.tiles = new_tiles_in_huro
        self.assertEqual(self.huro_chii.tiles, new_tiles_in_huro)

    def test_add_kan(self):
        self.huro_pon.add_kan(Tile(Suit.MANZU.value, 2))
        self.assertEqual(self.huro_pon.naki_type, Naki.CHAKAN)

    def test_add_kan_error(self):
        with self.assertRaises(ValueError):
            self.huro_chii.add_kan(Tile(Suit.MANZU.value, 7))
