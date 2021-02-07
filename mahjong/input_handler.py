from typing import List

import pyinputplus as pyinput

from .helpers import convert_hand
from .components import Tile, Action, Naki


class UserInput:

    def actions(self, hand, new_tile, action_list, discard):
        action = Action.NOACT
        naki = Naki.NONE
        huro = []
        if True:
            user_raw_input = UserRawInput()
            action, naki, huro = user_raw_input.actions(
                hand, new_tile, action_list, discard)

        return action, naki, huro

    def discard(self, hand, new_tile, kuikae_tiles):
        tile_to_discard = None
        if True:
            user_raw_input = UserRawInput()
            tile_to_discard = user_raw_input.discard(
                hand, new_tile, kuikae_tiles)

        return tile_to_discard


class UserRawInput:

    def show_tiles(self,
                   hand_tiles: List[Tile],
                   discard: bool) -> str:
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

    def parse_options(self, action_list):
        options_str = ""
        for act, naki, possible_huros in action_list:
            options_str += f"{act.value}: {act}\n"

        return options_str

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
            huro_str = ", ".join([str(h) for h in huro])
            possible_huro_str += f"{i}: {huro_str}\n"

        selected_huro = pyinput.inputNum(
            f"""Please select huro set using number: {possible_huro_str}""",
            min=0,
            max=len(possible_huro_opt) - 1
        )

        return selected_naki, possible_huro_opt[selected_huro]

    def actions_with_new_tile(self, action_list):
        options_str = self.parse_options(action_list)
        selected_action = pyinput.inputNum(
            "Please select action using number:\n" + options_str,
            min=0,
            max=len(action_list) - 1
        )

        if selected_action == 1:  # NAKI
            selected_naki, selected_huro = self.get_naki(action_list)
        else:
            selected_naki = None
            selected_huro = None

        naki = Naki(selected_naki) if selected_naki else None

        return Action(selected_action), naki, selected_huro

    def actions(self, hand, new_tile, action_list, discard):
        hand_tiles = convert_hand(hand)
        if discard:
            print(f"The discarded tile is: | {new_tile} |")
        else:
            print(f"Drawn tile is: | {new_tile} |")
            hand_tiles.append(new_tile)
        hand_representation = self.show_tiles(hand_tiles, discard)
        print(hand_representation)

        return self.actions_with_new_tile(action_list)

    def discard(self, hand, new_tile, kuikae_tiles):
        hand_tiles = convert_hand(hand)
        if new_tile:
            hand_tiles.append(new_tile)
        if kuikae_tiles:
            # not allowed to choose from this list
            # TODO: now just hide from hand_representation,
            # need to change to something else if UI changes
            hand_tiles = [tile for tile in hand_tiles
                          if tile not in kuikae_tiles]
        hand_representation = self.show_tiles(hand_tiles, False)
        print("Please selected the tile you want to discard:")
        print(hand_representation)

        discard = pyinput.inputNum(
            "Discard tile No.: ",
            min=0,
            max=len(hand_tiles) - 1
        )
        return hand_tiles[discard]
