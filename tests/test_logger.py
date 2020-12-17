import unittest

from mahjong.player import Player
from mahjong.components import Stack, Tile, Action, Suit, Naki, Huro
from mahjong.event_logger import KyokuLogger


class TestActionLog(unittest.TestCase):
    def setUp(self):
        self.player_1 = Player('player 1', 0)
        self.player_2 = Player('player 2', 1)
        self.player_3 = Player('player 3', 2)
        self.player_4 = Player('player 4', 3)
        self.players = [self.player_1, self.player_2,
                        self.player_3, self.player_4]
        self.tile_stack = Stack()
        for player in self.players:
            for i in range(13):
                player.hand[self.tile_stack.draw().index] += 1

    def test_log_naki(self):
        naki_tile = Tile(Suit.SOUZU.value, 5)
        kan = Huro(Naki.ANKAN,
                   naki_tile,
                   [Tile(Suit.SOUZU.value, 5) for i in range(4)])
        logger = KyokuLogger()
        logger.log(
            p_pos=self.player_1.seating_position,
            action=Action.NAKI,
            action_tile=naki_tile,
            naki_type=Naki.ANKAN,
            huro=kan,
        )
        log = logger.logs[0]
        self.assertEqual(log.p_pos, 0)
        self.assertEqual(log.action, Action.NAKI)
        self.assertEqual(log.action_tile, naki_tile)
        self.assertEqual(log.naki_type, Naki.ANKAN)
        self.assertEqual(
            str(log),
            "Player 0 NAKI ANKAN with 5 SOUZU forms "
            "5 SOUZU|5 SOUZU|5 SOUZU|5 SOUZU",
        )

    def test_log_draw(self):
        drown_tile = Tile(Suit.SOUZU.value, 5)
        logger = KyokuLogger()
        logger.log(
            p_pos=self.player_1.seating_position,
            action=Action.DRAW,
            action_tile=drown_tile,
        )
        log = logger.logs[0]
        self.assertEqual(log.p_pos, 0)
        self.assertEqual(log.action, Action.DRAW)
        self.assertEqual(log.action_tile, drown_tile)
        self.assertEqual(
            str(log),
            "Player 0 DRAW with 5 SOUZU",
        )

    def test_log_draw_from_rinshan(self):
        drown_tile = Tile(Suit.MANZU.value, 5)
        logger = KyokuLogger()
        # from linshan
        logger.log(
            p_pos=self.player_2.seating_position,
            action=Action.DRAW_RINSHAN,
            action_tile=drown_tile,
        )
        log = logger.logs[0]
        self.assertEqual(log.p_pos, 1)
        self.assertEqual(log.action, Action.DRAW_RINSHAN)
        self.assertEqual(log.action_tile, drown_tile)
        self.assertEqual(
            str(log),
            "Player 1 DRAW_RINSHAN with 5 MANZU",
        )

    def test_discard(self):
        discard_tile = Tile(Suit.MANZU.value, 5)
        logger = KyokuLogger()
        # from linshan
        logger.log(
            p_pos=self.player_2.seating_position,
            action=Action.DISCARD,
            action_tile=discard_tile,
        )
        log = logger.logs[0]
        self.assertEqual(log.p_pos, 1)
        self.assertEqual(log.action, Action.DISCARD)
        self.assertEqual(log.action_tile, discard_tile)
        self.assertEqual(
            str(log),
            "Player 1 DISCARD with 5 MANZU",
        )
