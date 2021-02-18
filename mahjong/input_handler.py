from typing import List, Optional
from abc import ABC, abstractmethod

import pyinputplus as pyinput

from .helpers import convert_hand
from .utils import unicode_block
from .components import Tile, Action, Naki, Huro


class UserInput(ABC):

    def __init__(self):
        ...

    @abstractmethod
    def actions(self, hand, new_tile, action_list, discard):
        return NotImplemented

    @abstractmethod
    def discard(self, hand, new_tile, kuikae_tiles):
        return NotImplemented


class UserRawInput(UserInput):

    def show_tiles(self,
                   hand_tiles: List[Tile],
                   kabe: List[Huro],
                   discard: Optional[bool] = False) -> str:
        """Convert hand into string representation
        """
        hand_representation = "----- Tiles in hand -----\n"
        for i in range(len(hand_tiles)):
            if not discard and i == len(hand_tiles) - 1:
                hand_representation += f"|{i}||"
            else:
                hand_representation += f"{i}|"
        hand_representation += "\n"

        for i, tile in enumerate(hand_tiles):
            tile_unicode = unicode_block[tile.index]
            if not discard and i == len(hand_tiles) - 1:
                hand_representation += f"| {tile_unicode}||"
            else:
                if i < 10:
                    hand_representation += f"{tile_unicode}|"
                else:
                    hand_representation += f" {tile_unicode}|"
        hand_representation += "\n"
        if kabe:
            hand_representation += "----- Kabe -----\n"
            for huro in kabe:
                for tile in huro.tiles:
                    tile_unicode = unicode_block[tile.index]
                    hand_representation += f"{tile_unicode}|"
        return hand_representation

    def parse_options(self, action_list):
        options_str = ""
        act_values = []
        # TODO: fix duplication like the following
        # Please select action using number:
        # 0: Action.NOACT
        # 1: Action.NAKI
        # 1: Action.NAKI
        for act, naki, possible_huros in action_list:
            options_str += f"{act.value}: {act}\n"
            act_values.append(act.value)

        return options_str, min(act_values), max(act_values)

    def parse_naki_options(self, action_list):
        naki_options_str = ""
        naki_huros = {}
        naki_choices = []
        for act, naki, possible_huros in action_list:
            if act == Action.NAKI:
                naki_options_str += f"{naki.value}: {naki}\n"
                naki_huros[naki.value] = possible_huros
                naki_choices.append(str(naki.value))

        return naki_options_str, naki_huros, naki_choices

    def get_naki(self, action_list):
        (naki_options_str,
         naki_huros,
         naki_choices) = self.parse_naki_options(action_list)

        selected_naki = int(pyinput.inputChoice(
            naki_choices,
            prompt=f"""Please select naki type using number:
                       {naki_options_str}""",
            blank=True
        ))

        possible_huro_opt = naki_huros[selected_naki]
        possible_huro_str = ""
        for i, huro in enumerate(possible_huro_opt):
            huro_str = "|".join([unicode_block[h.index] for h in huro])
            possible_huro_str += f"{i}: {huro_str}\n"

        selected_huro = pyinput.inputNum(
            f"""Please select huro set using number: {possible_huro_str}""",
            min=0,
            max=len(possible_huro_opt) - 1
        )

        return selected_naki, possible_huro_opt[selected_huro]

    def actions_with_new_tile(self, action_list):
        options_str, min_act ,max_act = self.parse_options(action_list)
        selected_action = pyinput.inputNum(
            "Please select action using number:\n" + options_str,
            min=min_act,
            max=max_act
        )

        selected_naki = None
        selected_huro = None
        if selected_action == Action.NAKI.value:
            selected_naki, selected_huro = self.get_naki(action_list)
        elif selected_action == Action.RON.value:
            print("Player RON!")
        elif selected_action == Action.TSUMO.value:
            print("Player TSUMO!")
        else:
            ...

        naki = Naki(selected_naki) if selected_naki else None

        return Action(selected_action), naki, selected_huro

    def actions(self, player, new_tile, action_list, discard):
        if (action_list == [(Action.NOACT, Naki.NONE, [])]) and discard:
            return Action.NOACT, Naki.NONE, []
        else:
            hand_tiles = convert_hand(player.hand)
            tile_unicode = unicode_block[new_tile.index]
            print(f"------ \nPlayer: {player.name}")
            print(f"Jikaze: {player.jikaze.name}")
            if discard:
                print(f"The discarded tile is: {tile_unicode}")
                hand_representation = self.show_tiles(hand_tiles,
                                                      player.kabe,
                                                      discard)
                print(hand_representation)
            else:
                print(f"Drawn tile is: {tile_unicode}")

            if action_list == [(Action.NOACT, Naki.NONE, [])]:
                return Action.NOACT, Naki.NONE, []
            else:
                return self.actions_with_new_tile(action_list)

    def discard(self, player, new_tile, kuikae_tiles):
        hand_tiles = convert_hand(player.hand)
        if new_tile:
            hand_tiles.append(new_tile)
        if kuikae_tiles:
            # not allowed to choose from this list
            # TODO: now just hide from hand_representation,
            # need to change to something else if UI changes
            hand_tiles = [tile for tile in hand_tiles
                          if tile not in kuikae_tiles]
        hand_representation = self.show_tiles(hand_tiles, player.kabe)
        print("Please selected the tile you want to discard:")
        print(hand_representation)

        discard = pyinput.inputNum(
            "Discard tile No.: ",
            min=0,
            max=len(hand_tiles) - 1
        )
        discard_tile = hand_tiles[discard]
        print(f"Tile to discard: \n{unicode_block[discard_tile.index]}")

        return hand_tiles[discard]


def input_switch(input_method):
    if input_method == 'raw_input':
        return UserRawInput()
    else:
        raise ValueError('input method should be: raw_input')
