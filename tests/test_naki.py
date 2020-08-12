import unittest

from mahjong.mahjong import Tile, Suit, Jihai
from mahjong.player import Player, Position
from mahjong.naki_and_actions import check_pon


class TestPon(unittest.TestCase):

    def setUp(self):
        self.player = Player('test', Position.TON.value)
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.SHAA.value).index] += 3
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HATSU.value).index] += 3
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.HAKU.value).index] += 2
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.PEI.value).index] += 2
        self.player.hand[Tile(Suit.JIHAI.value, Jihai.TON.value).index] += 3

    def test_pon(self):
        discard = Tile(Suit.JIHAI.value, Jihai.HAKU.value)
        self.assertEqual(check_pon(self.player, discard), True)


