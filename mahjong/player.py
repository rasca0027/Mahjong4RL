from typing import Tuple, List, Set, DefaultDict
from collections import defaultdict

from .utils import get_name
from .helpers import nine_yaochuus, convert_hand
from .components import Huro, Tile, Action, Jihai, Naki
from .naki_and_actions import (
    check_tenpai, check_tsumo, check_ankan, check_chakan,
    check_daminkan, check_pon, check_chii
)


class Player:
    def __init__(self, name, seating_position):
        self.name: str = name
        self._seating_position = seating_position  # 固定座位順序 (0~3)
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

    def get_komicha(self) -> int:
        return (self.seating_position - 1) % 4

    def get_toimen(self) -> int:
        return (self.seating_position + 2) % 4

    def get_shimocha(self) -> int:
        return (self.seating_position + 1) % 4

    def action_with_discard_tile(
        self, tile: Tile, pos: int
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

        action_list = [(Action.NOACT, None, [])]
        if possible_kans := check_daminkan(self.hand, tile):
            action_list.append((Action.NAKI, Naki.DAMINKAN, possible_kans))
        if possible_pons := check_pon(self.hand, tile):
            action_list.append((Action.NAKI, Naki.PON, possible_pons))
        if possible_chiis := check_chii(self.hand, tile):
            action_list.append((Action.NAKI, Naki.CHII, possible_chiis))

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
        self, tile: Tile, first_turn: bool
    ) -> Tuple[Tuple[Action, Naki], Tile]:
        """"Player has to select an action reacting to the new drawn tile.
        Args:
          tile: discarded tile
        Returns:
          (action, naki): TSUMO/ANKAN/CHAKAN
          discard_tile: Tile
        """
        action_list = [(Action.NOACT, None, [])]
        if first_turn and nine_yaochuus(self.hand, tile):
            action_list.append((Action.RYUUKYOKU, None, []))
        if check_tsumo(self, tile):
            action_list.append((Action.TSUMO, None, []))
        if possible_kans := check_ankan(self.hand, tile):
            action_list.append((Action.NAKI, Naki.ANKAN, possible_kans))
        if possible_kans := check_chakan(self.hand, self.kabe, tile):
            action_list.append((Action.NAKI, Naki.CHAKAN, possible_kans))

        action, naki = self.get_input(tile, action_list, False)

        if action == Action.TSUMO:
            self.agari_tile = tile
            discard_tile = None
        elif action == Action.NAKI:
            discard_tile = None
        else:
            discard_tile = self.get_discard(tile)

        return (action, naki), discard_tile

    def action_with_naki(self, naki: Naki) -> None:
        # add tmp_huro to kabe
        self.kabe.append(self.tmp_huro)
        self.remove_huro_tiles()
        if naki != Naki.ANKAN:
            self.menzenchin = False
        self.tmp_huro = None
        return

    def remove_huro_tiles(self) -> None:
        """Remove the called tiles from player's hand.
        """
        for tile in self.tmp_huro.tiles:
            if tile != self.tmp_huro.naki_tile:
                self.hand[tile.index] -= 1

    def discard_after_naki(self) -> Tile:
        discard = self.get_discard()
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
        hand_tiles = convert_hand(self.hand)
        if discard:
            print(f"The discarded tile is: | {new_tile} |")
        else:
            print(f"Drawn tile is: | {new_tile} |")
            hand_tiles.append(new_tile)
        hand_representation = self.show_tiles(hand_tiles, discard)
        print(hand_representation)

        options_str = ""
        naki_options_str = ""
        naki_huros = {}
        for act, naki, possible_huros in action_list:
            options_str += f"{act.value}: {act}\n"
            if act == Action.NAKI:
                naki_options_str += f"{naki.value}: {naki}\n"
                naki_huros[naki.value] = possible_huros
        selected_action = int(input(
            "Please select action using number:\n" + options_str
        ))
        if selected_action < 0 or selected_action > len(action_list) - 1:
            raise ValueError

        if selected_action == 1:  # NAKI
            selected_naki = int(input(
                "Please select naki type using number:\n" + naki_options_str
            ))
            possible_huro_opt = naki_huros[selected_naki]
            possible_huro_str = ""
            for i, huro in enumerate(possible_huro_opt):
                huro_str = ",".join([str(h) for h in huro])
                possible_huro_str += f"{i}: {huro_str}\n"
            selected_huro = int(input(
                f"""Please select huro set using number:
                {possible_huro_str}"""
            ))
            if selected_huro < 0 or selected_huro > len(possible_huro_opt) - 1:
                raise ValueError
            self.tmp_huro = Huro(
                Naki(selected_naki),
                new_tile,
                possible_huro_opt[selected_huro]
            )
        else:
            selected_naki = None

        naki = Naki(selected_naki) if selected_naki else None
        return Action(selected_action), naki

    def get_discard(self, new_tile: Tile = None) -> Tile:
        """Add in the newly drawn tile and discard a tile
        """
        hand_tiles = convert_hand(self.hand)
        if new_tile:
            hand_tiles.append(new_tile)
        hand_representation = self.show_tiles(hand_tiles, False)

        print("Please selected the tile you want to discard:")
        print(hand_representation)
        discard = int(input("Discard tile No.: "))

        if discard < 0 or discard > len(hand_tiles) - 1:
            raise ValueError

        return hand_tiles[discard]

    def show_tiles(self, hand_tiles: List[Tile], discard: bool) -> str:
        """Convert hand into string representation
        """
        hand_representation = f"----- {self.name}'s hand -----\n"
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
