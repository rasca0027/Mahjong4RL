import copy

from typing import Tuple, List, Set, DefaultDict, Optional
from collections import defaultdict

from .utils import get_name
from .helpers import nine_yaochuus
from .components import Huro, Tile, Stack, Action, Jihai, Naki
from .naki_and_actions import (
    check_tenpai, check_ron, check_tsumo, check_ankan, check_chakan,
    check_daminkan, check_pon, check_chii, check_riichi
)
from .input_handler import input_switch


class Player:
    def __init__(
        self,
        name,
        seating_position,
        input_method: Optional[str] = 'raw_input'
    ):
        self.name: str = name
        self._seating_position = seating_position  # 固定座位順序 (0~3)
        self.input_method = input_method
        # jikaze 自風, dealer seat (東風) rotates among players
        self.jikaze: Jihai = Jihai[get_name(Jihai, seating_position + 4)]
        self.points: int = 25_000
        self.is_riichi: bool = False
        self.hand: DefaultDict[int] = defaultdict(int)
        self.kabe: List[Huro] = []  # 副露/鳴き
        self.kawa: List[Tile] = []  # 河 is formed by the discarded tiles.
        self.menzenchin: bool = True
        self.tmp_huro: Huro = None
        self.furiten_tiles_idx: Set[int] = set()
        self.tmp_furiten: bool = False
        self.permanent_furiten: bool = False
        self.agari_tile: Tile = None

    def __str__(self):
        return (
            f"Player: { self.name }, Seating Position: "
            f"{ self.seating_position }, Jikaze: { self.jikaze.name }"
        )

    def add_kawa(self, tile: Tile) -> None:
        if tile:
            self.hand[tile.index] -= 1
            self.kawa.append(tile)
            self.furiten_tiles_idx.add(tile.index)
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
    def agari_tile(self):
        return self._agari_tile

    @agari_tile.setter
    def agari_tile(self, tile: Tile) -> None:
        if not isinstance(tile, Tile) and tile is not None:
            raise TypeError("Agari tile must be a Tile")
        self._agari_tile = tile

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

    def get_kamicha(self) -> int:
        return (self.seating_position - 1) % 4

    def get_toimen(self) -> int:
        return (self.seating_position + 2) % 4

    def get_shimocha(self) -> int:
        return (self.seating_position + 1) % 4

    def get_naki_action_list(self,
                             is_drawer,
                             hand,
                             kabe,
                             tile,
                             haiteihai=False):
        """Check player's eligible action to a tile.
        Args:
          is_drawer: bool, if the player drew the tile or other player
                  discarded it.
          hand: player's hand
          kabe: player's huro
          tile: the tile to check against the hand
          haiteihai: bool, if the tile is the last availble tile
        Returns:
          action_list (list of tuples): Naki type and possible nakis
        """
        action_list = [(Action.NOACT, Naki.NONE, []), ]

        if haiteihai:
            return action_list
        elif is_drawer:
            if possible_kans := check_ankan(hand, tile):
                action_list.append((Action.NAKI, Naki.ANKAN, possible_kans))
            if possible_kans := check_chakan(hand, kabe, tile):
                action_list.append((Action.NAKI, Naki.CHAKAN, possible_kans))
        else:
            if possible_kans := check_daminkan(hand, tile):
                action_list.append((Action.NAKI, Naki.DAMINKAN, possible_kans))
            if possible_pons := check_pon(hand, tile):
                action_list.append((Action.NAKI, Naki.PON, possible_pons))

        return action_list

    def call_riichi(self, discard_tile, tile, stack):
        tmp_hand = copy.deepcopy(self.hand)
        tmp_hand[tile.index] += 1
        tmp_hand[discard_tile.index] -= 1
        if check_riichi(self, check_tenpai(tmp_hand, self.kabe), stack):
            action_list = [(Action.NOACT, Naki.NONE, []),
                           (Action.RIICHI, Naki.NONE, [])]
            action, naki = self.get_input(tile, action_list, False)
            if action == Action.RIICHI:
                self.is_riichi = True
                self.points -= 1_000

    def action_with_discard_tile(
        self,
        tile: Tile,
        pos: int,
        is_haiteihai: bool = False,
        suukaikan: bool = False
    ) -> Tuple[Action, Naki]:
        """"Player has to select an action reacting to
          the discarded tile.
        Args:
          tile: discarded tile
          pos: the seating position of the person discarded the tile
        Returns:
          action: CHI/PON/DAMINKAN/RON
        """
        self.tmp_huro = None
        if suukaikan:
            action_list = [(Action.NOACT, Naki.NONE, []), ]
            if check_ron(self, tile):
                action_list.append((Action.RON, Naki.NONE, []))
        else:
            action_list = self.get_naki_action_list(
                False, self.hand, self.kabe, tile, is_haiteihai)
        if pos == self.get_kamicha():
            if possible_chiis := check_chii(self.hand, tile):
                action_list.append((Action.NAKI, Naki.CHII, possible_chiis))
        if check_ron(self, tile):
            action_list.append((Action.RON, Naki.NONE, []))

        action, naki = self.get_input(tile, action_list, True)

        # set temporary and permanent furiten
        if action == Action.NOACT:
            if tile in check_tenpai(self.hand, self.kabe):
                self.tmp_furiten = True
                if self.is_riichi:
                    self.permanent_furiten = True
        elif action == Action.RON:
            self.agari_tile = tile

        return action, naki

    def action_with_new_tile(
        self,
        tile: Tile,
        first_turn: bool,
        stack: Stack,
        suukaikan: bool = False
    ) -> Tuple[Tuple[Action, Naki], Tile]:
        """"Player has to select an action reacting to the new drawn tile.
        Args:
          tile: discarded tile
        Returns:
          (action, naki): TSUMO/ANKAN/CHAKAN
          discard_tile: Tile
        """
        if suukaikan:
            action_list = [(Action.NOACT, Naki.NONE, []), ]
        else:
            action_list = self.get_naki_action_list(
                True, self.hand, self.kabe, tile, stack.is_haitei)
        if first_turn and nine_yaochuus(self.hand, tile):
            action_list.append((Action.RYUUKYOKU, Naki.NONE, []))
        if check_tsumo(self.hand, self.kabe, tile):
            action_list.append((Action.TSUMO, Naki.NONE, []))

        action, naki = self.get_input(tile, action_list, False)

        if action == Action.TSUMO:
            self.agari_tile = tile
            discard_tile = None
        elif action == Action.NAKI:
            discard_tile = None
        else:
            discard_tile = self.get_discard(tile)
            if not self.is_riichi:
                self.call_riichi(discard_tile, tile, stack)

        return (action, naki), discard_tile

    def action_with_naki(self, naki: Naki) -> List[Tile]:
        """Add Player's naki to kabe
        Returns:
          kuikae_tiles: if any
        """
        # add tmp_huro to kabe
        if naki == Naki.CHAKAN:
            for huro in self.kabe:
                if (
                    (huro.naki_type == Naki.PON)
                    & (huro.naki_tile == self.tmp_huro.naki_tile)
                ):
                    huro.add_kan(self.tmp_huro.naki_tile)
                    break
        else:
            self.kabe.append(self.tmp_huro)
        self.remove_huro_tiles(self.tmp_huro.naki_type)
        if naki != Naki.ANKAN:
            self.menzenchin = False

        # check Kuikae 喰い替え
        kuikae_tiles = []
        if naki == Naki.CHII:
            # Middle tile or Same end tile of a chii
            kuikae_tiles.append(self.tmp_huro.naki_tile)
            # Different end tile of a chii
            if self.tmp_huro.naki_tile == self.tmp_huro.tiles[0]:
                kuikae_tiles.append(self.tmp_huro.tiles[2].next_tile())
            elif self.tmp_huro.naki_tile == self.tmp_huro.tiles[2]:
                kuikae_tiles.append(self.tmp_huro.tiles[0].prev_tile())

        elif naki == Naki.PON:
            kuikae_tiles.append(self.tmp_huro.naki_tile)

        self.tmp_huro = None

        return kuikae_tiles

    def remove_huro_tiles(self, naki_type: Naki) -> None:
        """Remove the called tiles from player's hand.
        """
        for tile in self.tmp_huro.tiles:
            if naki_type == Naki.PON:
                self.hand[tile.index] -= 2
                break
            elif naki_type == Naki.DAMINKAN:
                self.hand[tile.index] -= 3
                break
            elif naki_type == Naki.ANKAN:
                self.hand[tile.index] -= 4
                break
            elif naki_type == Naki.CHAKAN:
                self.hand[tile.index] -= 1
                break
            elif naki_type == Naki.CHII:
                if tile != self.tmp_huro.naki_tile:
                    self.hand[tile.index] -= 1
            else:
                raise ValueError("invalid naki type")

    def discard_after_naki(self, kuikae_tiles: List[Tile]) -> Tile:
        discard = self.get_discard(kuikae_tiles=kuikae_tiles)

        return discard

    def action_with_chakan(self, kan_tile, kan_type) -> Action:
        """Player reacts with oya player's CHAKAN or ANKAN.
        Returns:
          action: NOACT or RON
        """
        # TODO: add 國士無雙搶槓 flag
        # can react with RON (CHANKAN)
        return Action.NOACT

    def get_input(
        self,
        new_tile: Tile,
        action_list: List[Tuple[Action, Naki, List[Tile]]],
        discard: bool
    ) -> Tuple[Action, Naki]:
        """Gets user input to choose action and sets tmp_huro
        """
        user_input = input_switch(self.input_method)
        action, naki, huro = user_input.actions(self,
                                                new_tile,
                                                action_list,
                                                discard)
        if action == Action.NAKI:
            self.tmp_huro = Huro(naki, new_tile, huro)

        return action, naki

    def get_discard(
        self,
        new_tile: Tile = None,
        kuikae_tiles: List[Tile] = []
    ) -> Tile:
        """Add in the newly drawn tile and discard a tile
        """
        user_input = input_switch(self.input_method)
        tile_to_discard = user_input.discard(self, new_tile, kuikae_tiles)

        return tile_to_discard
