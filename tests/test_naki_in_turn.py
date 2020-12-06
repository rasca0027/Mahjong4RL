import unittest
from unittest.mock import MagicMock
from typing import List

from mahjong.kyoku import Kyoku, Turn
from mahjong.player import Player
from mahjong.components import Suit, Tile, Jihai
from mahjong.helpers import convert_hand


def show_tiles(hand_tiles: List[Tile], discard: bool) -> str:
    """Convert hand into string representation
    """
    hand_representation = "----- Tiles in hand -----\n"
    for i in range(len(hand_tiles)):
        hand_representation += f"  {i}  |"
    hand_representation += "\n"

    for i, tile in enumerate(hand_tiles):
        if not discard and i == len(hand_tiles) - 1:
            hand_representation += f"| {tile} ||"
        else:
            hand_representation += f" {tile} |"
    hand_representation += "\n"
    return hand_representation


class TestPon(unittest.TestCase):

    def setUp(self):
        player_names = ['Kelly', 'Leo', 'Ball', 'Hao']
        self.bakaze = Jihai.TON
        self.kyoku_num = 1  # e.g.東1局
        self.players = self.get_init_players(player_names)
        self.current_kyoku = Kyoku(self.players, 0, self.bakaze, 0)

    def get_init_players(self, player_names):
        players = []
        for i, name in enumerate(player_names):
            players.append(Player(name, i))
        return players

    def test_pon(self):
        self.current_kyoku.deal()

        # change tile in hand to test pon
        pon_tile = Tile(Suit.JIHAI.value, Jihai.CHUN.value)
        pon_tile.owner = self.players[0].seating_position
        self.current_kyoku.players[0].hand[pon_tile.index] = 1
        self.current_kyoku.players[1].hand[pon_tile.index] = 2
        self.current_kyoku.players[2].hand[pon_tile.index] = 0
        self.current_kyoku.players[3].hand[pon_tile.index] = 0

        turn = Turn(self.current_kyoku.players, self.current_kyoku.tile_stack)

        mock_draw_flow = MagicMock(
            return_value=(0, pon_tile, self.players[0].seating_position))
        state, discard_tile, discard_pos = mock_draw_flow(
            self.current_kyoku.oya_player)

        state, discard_tile, discard_pos = turn.discard_flow(
            discard_tile, discard_pos)

        print(f'returned value, state: {state}, {discard_tile}, {discard_pos}')
