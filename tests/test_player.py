import unittest

from mahjong.player import Player
from mahjong.components import Stack, Tile, Suit, Naki, Huro, Jihai


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player('test player', 0)
        self.player_2 = Player('test player 2', 1)

    def test_att(self):
        tile_stack = Stack()
        for i in range(13):
            self.player.hand[tile_stack.draw().index] += 1
        self.assertEqual(self.player.name, 'test player')
        self.assertEqual(self.player.seating_position, 0)
        self.assertEqual(self.player.jikaze, Jihai.TON)
        self.assertEqual(self.player.points, 25_000)
        self.assertEqual(self.player.is_riichi, False)
        self.assertEqual(sum(self.player.hand.values()), 13)
        self.assertEqual(len(self.player.kabe), 0)
        self.assertEqual(len(self.player.kawa), 0)
        self.assertEqual(self.player.menzenchin, True)
        self.assertEqual(self.player.tmp_huro, None)
        self.assertEqual(self.player.tmp_furiten, False)
        self.assertEqual(self.player.permanent_furiten, False)
        self.assertEqual(self.player.agari_tile, None)

    def test_str(self):
        player_str = "Player: test player, Seating Position: 0, Jikaze: TON"
        self.assertEqual(str(self.player), player_str)

    def test_add_kawa(self):
        discard_tile = Tile(0, 1)
        self.player.add_kawa(discard_tile)

        self.assertEqual(len(self.player.kawa), 1)
        self.assertEqual(self.player.kawa[0], discard_tile)

    def test_hand_setter(self):
        list_of_tiles = [Tile(0, 1), Tile(0, 1), Tile(0, 2)]
        self.player.hand = list_of_tiles

        self.assertEqual(sum(self.player.hand.values()), 3)
        self.assertEqual(self.player.hand[Tile(0, 1).index], 2)
        self.assertEqual(self.player.hand[Tile(0, 2).index], 1)

    def test_agari_tile_setter(self):
        tile_nan = Tile(Suit.JIHAI.value, Jihai.NAN.value)
        self.player.agari_tile = tile_nan
        self.assertEqual(self.player.agari_tile, tile_nan)

        with self.assertRaises(TypeError):
            self.player.agari_tile = Jihai.HAKU

    def test_seating_position_setter(self):
        with self.assertRaises(AttributeError):
            self.player.seating_position = 2

    def test_jikaze_setter(self):
        self.assertEqual(self.player.jikaze, Jihai.TON)
        self.player.jikaze = Jihai.NAN
        self.assertEqual(self.player.jikaze, Jihai.NAN)
        self.player.jikaze = Jihai((self.player.jikaze.value + 3) % 4 + 4)
        self.assertEqual(self.player.jikaze, Jihai.TON)

        with self.assertRaises(ValueError):
            self.player.jikaze = Jihai.HAKU
        with self.assertRaises(ValueError):
            self.player.jikaze = 1

    def test_get_kamicha(self):
        self.assertEqual(self.player.get_kamicha(), 3)
        self.assertEqual(self.player_2.get_kamicha(), 0)

    def test_get_toimen(self):
        self.assertEqual(self.player.get_toimen(), 2)
        self.assertEqual(self.player_2.get_toimen(), 3)

    def test_get_shimocha(self):
        self.assertEqual(self.player.get_shimocha(), 1)
        self.assertEqual(self.player_2.get_shimocha(), 2)

    def test_action_with_discard_tile(self):
        ...

    def test_action_with_new_tile(self):
        ...

    def test_action_with_naki(self):
        naki_tile = Tile(Suit.SOUZU.value, 5)
        naki_tile.owner = self.player.seating_position
        pon_5_souzu = Huro(Naki.PON,
                           naki_tile,
                           [Tile(Suit.SOUZU.value, 5) for i in range(3)])
        self.player.tmp_huro = pon_5_souzu
        self.player.action_with_naki(Naki.PON)
        self.assertEqual(self.player.kabe[0], pon_5_souzu)
        self.assertEqual(self.player.tmp_huro, None)

    def test_discard_after_naki(self):
        ...

    def test_get_input(self):
        ...

    def test_validate_input(self):
        ...
