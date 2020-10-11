from typing import Tuple, List, DefaultDict
from collections import defaultdict

from .utils import get_name
from .components import Huro, Tile, Action, Jihai
from .naki_and_actions import check_tenpai


class Player:
    def __init__(self, name, seating_position):
        self.name: str = name
        self._seating_position = seating_position  # 固定座位順序
        # jikaze 自風, dealer seat (東風) rotates among players
        self.jikaze: Jihai = Jihai[get_name(Jihai, seating_position + 3)]
        self.points: int = 25_000
        self.is_riichi: bool = False
        self.hand: DefaultDict[int] = defaultdict(int)
        self.kabe: List[Huro] = []  # 副露/鳴き
        self.kawa: List[Tile] = []  # 河 is formed by the discarded tiles.
        self.tmp_huro: Huro = None
        self.tmp_furiten: bool = False
        self.permanent_furiten: bool = False
        self.agari_tile: Tile = None
        # TODO: Build Player's connection (socket)?

    def __str__(self):
        return (
            f"Player: { self.name }, Seating Position: "
            f"{ self.seating_position }, Jikaze: { self.jikaze.name }"
        )

    def add_kawa(self, tile: Tile) -> None:
        if tile:
            self.kawa.append(tile)
        return

    @property
    def hand(self):
        return self._hand

    @hand.setter
    def hand(self, tiles: List[Tile]) -> None:
        self._hand = defaultdict(int)
        # TODO: raise error when len(hand) > 13
        for tile in tiles:
            self._hand[tile.index] += 1

    @property
    def seating_position(self) -> int:
        return self._seating_position

    @property
    def jikaze(self) -> Jihai:
        return self._jikaze

    @jikaze.setter
    def jikaze(self, value) -> None:
        if value not in (jikaze_value := [Jihai.TON, Jihai.NAN,
                                          Jihai.SHAA, Jihai.PEI]):
            raise ValueError(f"Jikaze should be in: {jikaze_value}")
        self._jikaze = value

    def get_komicha(self) -> int:
        return (self.seating_position + 2) % 4 + 1

    def get_toimen(self) -> int:
        return (self.seating_position + 1) % 4 + 1

    def get_shimocha(self) -> int:
        return (self.seating_position % 4) + 1

    def action_with_discard_tile(self, tile: Tile, pos: int) -> Action:
        """"Player has to select an action reacting to
          the discarded tile.
        Args:
          tile: discarded tile
          pos: the seating position of the person discarded the tile
        Returns:
          action: CHI/PON/DAMINKAN/RON
        """
        self.tmp_huro = None
        # TODO: connect player's input with the action

        action = None  # temporary, otherwise linter doesn't let me through
        # set temporary and permanent furiten
        if action == Action.NOACT:
            if tile in check_tenpai(self.hand, self.kabe):
                self.tmp_furiten = True
                if self.is_riichi:
                    self.permanent_furiten = True

        elif action == Action.RON:
            self.agari_tile = tile

        return action

    def action_with_new_tile(self, tile: Tile) -> Tuple[Action, Tile]:
        """"Player has to select an action reacting to the new drawn tile.
        Args:
          tile: discarded tile
        Returns:
          action: TSUMO/ANKAN/CHAKAN
          discard_tile: Tile
        """
        self.tmp_huro = None
        action = None
        # TODO: check TSUMO/ANKAN/CHAKAN, else pick discard tile
        if action == Action.RON:
            self.agari_tile = tile

        return

    def action_with_naki(self, action: Action) -> None:
        # add tmp_huro to kabe
        self.kabe.append(self.tmp_huro)
        self.tmp_huro = None
        return

    def discard_after_naki(self) -> Tile:
        return

    def action_with_chakan(self, kan_tile, kan_type) -> Tile:
        """Player reacts with oya player's CHAKAN or ANKAN.
        Returns:
          action: NOACT or RON
        """
        # can react with RON (CHANKAN)
        return Action.NOACT

    def get_input(self):
        # TODO: get input from player
        # input()
        # socket.request()
        return

    def validate_input(self):
        # TODO: validate each input
        input_ = input()
        try:
            int(input_)
        except ValueError:
            print("digit please :(")
        return
