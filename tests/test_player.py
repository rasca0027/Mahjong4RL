import unittest

from mahjong.player import Player
from mahjong.components import Stack, Tile, Suit, Naki, Huro, Action, Jihai


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player('test player', 1)
        self.player_2 = Player('test player 2', 2)

    def test_att(self):
        tile_stack = Stack()
        for i in range(13):
            self.player.hand[tile_stack.draw().index] += 1
        self.assertEqual(self.player.name, 'test player')
        self.assertEqual(self.player.seating_position, 1)
        self.assertEqual(self.player.jikaze, Jihai.TON)
        self.assertEqual(self.player.points, 25_000)
        self.assertEqual(self.player.is_riichi, False)
        self.assertEqual(sum(self.player.hand.values()), 13)
        self.assertEqual(len(self.player.kabe), 0)
        self.assertEqual(len(self.player.kawa), 0)
        self.assertEqual(self.player.tmp_huro, None)
        self.assertEqual(self.player.tmp_furiten, False)
        self.assertEqual(self.player.permanent_furiten, False)

    def test_str(self):
        self.assertEqual(str(self.player),
                         "Player: test player, Seating Position: TON")

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

    def test_seating_position_setter(self):
        with self.assertRaises(AttributeError):
            self.player.seating_position = 2

    def test_jikaze_setter(self):
        self.assertEqual(self.player.jikaze, Jihai.TON)
        self.player.jikaze = Jihai.NAN
        self.assertEqual(self.player.jikaze, Jihai.NAN)
        self.player.jikaze = Jihai((self.player.jikaze.value - 3) % 4 + 4)
        self.assertEqual(self.player.jikaze, Jihai.SHAA)

        with self.assertRaises(ValueError):
            self.player.jikaze = Jihai.HAKU
        with self.assertRaises(ValueError):
            self.player.jikaze = 1

    def test_get_komicha(self):
        self.assertEqual(self.player.get_komicha(), 4)
        self.assertEqual(self.player_2.get_komicha(), 1)

    def test_get_toimen(self):
        self.assertEqual(self.player.get_toimen(), 3)
        self.assertEqual(self.player_2.get_toimen(), 4)

    def test_get_shimocha(self):
        self.assertEqual(self.player.get_shimocha(), 2)
        self.assertEqual(self.player_2.get_shimocha(), 3)

    def test_action_with_discard_tile(self):
        ...

    def test_action_with_new_tile(self):
        ...

    def test_action_with_naki(self):
        pon_5_souzu = Huro(Naki.PON,
                           [Tile(Suit.SOUZU.value, 5) for i in range(3)])
        self.player.tmp_huro = pon_5_souzu
        self.player.action_with_naki(Action.PON)
        self.assertEqual(self.player.kabe[0], pon_5_souzu)
        self.assertEqual(self.player.tmp_huro, None)

    def test_discard_after_naki(self):
        ...

    def test_get_input(self):
        ...

    def test_validate_input(self):
        ...