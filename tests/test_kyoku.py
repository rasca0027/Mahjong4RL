import unittest

from mahjong.player import Player
from mahjong.components import Jihai
from mahjong.kyoku import Kyoku


class TestTurnDrawFlow(unittest.TestCase):

    def setUp(self):
        self.player_1 = Player('player 1', 0)
        self.player_2 = Player('player 2', 1)
        self.player_3 = Player('player 3', 2)
        self.player_4 = Player('player 4', 3)
        self.players = [self.player_1, self.player_2,
                        self.player_3, self.player_4]

        self.kyoku = Kyoku(
            players=self.players,
            honba=0,
            bakaze=Jihai.TON,
            kyotaku=0
        )

    def test_att(self):
        self.assertEqual(self.kyoku.winner, [])
        self.assertEqual(self.kyoku.players, self.players)
        self.assertEqual(self.kyoku.oya_player, self.player_1)
        self.assertEqual(self.kyoku.honba, 0)
        self.assertEqual(self.kyoku.kyotaku, 0)
        self.assertEqual(self.kyoku.bakaze, Jihai.TON)
        self.assertEqual(self.kyoku.atamahane, True)

    def test_bakaze_setter(self):
        self.kyoku.bakaze = Jihai.NAN
        self.assertEqual(self.kyoku.bakaze, Jihai.NAN)
        with self.assertRaises(ValueError):
            self.kyoku.bakaze = Jihai.CHUN

    def test_get_oya_player(self):
        for p in self.kyoku.players:
            p.jikaze = Jihai((p.jikaze.value + 3) % 4 + 4)

        oya_player = self.kyoku.get_oya_player()
        self.assertEqual(oya_player, self.kyoku.players[1])

    def test_deal(self):
        self.kyoku.deal()
        self.assertEqual(sum(self.kyoku.players[0].hand.values()), 13)
        self.assertEqual(sum(self.kyoku.players[1].hand.values()), 13)
        self.assertEqual(sum(self.kyoku.players[2].hand.values()), 13)
        self.assertEqual(sum(self.kyoku.players[3].hand.values()), 13)

    def test_calculate_yaku(self):
        ...

    def test_start(self):
        ...
        # self.kyoku.start()
        # self.kyoku.oya_player.action_with_new_tile = MagicMock(
        #     return_value=((Action.NOACT, Naki.NONE), Tile(1, 1)))
