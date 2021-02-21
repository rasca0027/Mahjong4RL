from typing import List, Optional, Tuple, TYPE_CHECKING
from abc import ABC, abstractmethod

import pyinputplus as pyinput
import inquirer

from .helpers import convert_hand
from .utils import unicode_block
from .components import Tile, Action, Naki, Huro
if TYPE_CHECKING:
    from .player import Player


class UserInput(ABC):

    def __init__(self):
        ...

    @abstractmethod
    def actions(
        self,
        player: 'Player',
        new_tile: Tile,
        action_list: List,
        discard: bool
    ) -> Tuple[Action, Naki, Huro]:
        """Ask user to choose an action from available options.
        Args:
            player: the user's player
            new_tile: the tile to check against the hand
            action_list: available actions
            discard: bool, if the tile is discarded by other player
        Returns:
            selected action (tuple of action related var):
            if action is Naki then includes naki type and huro
        """
        return NotImplemented

    @abstractmethod
    def discard(
        self,
        player: 'Player',
        new_tile: Tile,
        kuikae_tiles: List[Tile]
    ) -> Tile:
        """Ask user to choose an action from available options.
        Args:
            player: the user's player
            new_tile: the tile to check against the hand
            kuikae_tiles: 喰い替え
        Returns:
            selected tile to discard
        """
        return NotImplemented


class CliInput(UserInput):

    def show_tiles(self,
                   hand_tiles: List[Tile],
                   kawa: Optional[List[Tile]] = [],
                   kabe: Optional[List[Huro]] = [],
                   discard: Optional[bool] = False) -> str:
        """Convert hand into string representation
        """
        hand_representation = "----- Tiles in hand -----\n"
        for i in range(len(hand_tiles)):
            if not discard:
                hand_representation += f"{i}|"
            else:
                if i == len(hand_tiles) - 1:
                    hand_representation += f"|{i}||"
                else:
                    hand_representation += f"{i}|"
        hand_representation += "\n"

        for i, tile in enumerate(hand_tiles):
            tile_unicode = unicode_block[tile.index]
            if not discard:
                if i < 10:
                    if tile.index == 1:
                        hand_representation += f"{tile_unicode}"
                    else:
                        hand_representation += f"{tile_unicode} "
                else:
                    hand_representation += f" {tile_unicode} "
            else:
                if (i == len(hand_tiles) - 1):
                    if i > 9:
                        hand_representation += f"| {tile_unicode}||"
                    else:
                        hand_representation += f"|{tile_unicode}||"
                else:
                    if i < 10:
                        if tile.index == 1:
                            hand_representation += f"{tile_unicode}"
                        else:
                            hand_representation += f"{tile_unicode} "
                    elif i == len(hand_tiles) - 2 :
                        hand_representation += f" {tile_unicode}|"
                    else:
                        hand_representation += f" {tile_unicode} "

        hand_representation += "\n"
        if kawa:
            hand_representation += "----- Tiles in kawa -----\n"
            for tile in kawa:
                tile_unicode = unicode_block[tile.index]
                if tile.index == 1:
                    hand_representation += f"{tile_unicode}"
                else:
                    hand_representation += f"{tile_unicode} "
            hand_representation += "\n"
        if kabe:
            hand_representation += "----- Kabe -----\n"
            for huro in kabe:
                for tile in huro.tiles:
                    tile_unicode = unicode_block[tile.index]
                    if tile.index == 1:
                        hand_representation += f"{tile_unicode}"
                    else:
                        hand_representation += f"{tile_unicode} "
        print(hand_representation)


class UserRawInput(CliInput):

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
                naki_options_str += f"{naki.value}: {naki.name}\n"
                naki_huros[naki.value] = possible_huros
                naki_choices.append(str(naki.value))
        naki_options_str += "6: Cancel\n"
        naki_choices.append("6")

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

        if selected_naki == 6:
            return Naki.NONE, None

        possible_huro_opt = naki_huros[selected_naki]
        possible_huro_str = ""
        for i, huro in enumerate(possible_huro_opt):
            huro_str = " ".join([unicode_block[h.index] for h in huro])
            possible_huro_str += f"{i}: {huro_str}\n"
        possible_huro_str += "6: Cancel\n"

        selected_huro = pyinput.inputNum(
            f"""Please select huro set using number:
{possible_huro_str}""",
            min=0,
            max=6
        )
        if selected_huro == 6:
            return Naki.NONE, None

        return selected_naki, possible_huro_opt[selected_huro]

    def actions_with_new_tile(self, action_list):
        options_str, min_act, max_act = self.parse_options(action_list)
        selected_action = pyinput.inputNum(
            "Please select action using number:\n" + options_str,
            min=min_act,
            max=max_act
        )

        selected_naki = None
        selected_huro = None
        if selected_action == Action.NAKI.value:
            selected_naki, selected_huro = self.get_naki(action_list)
            if selected_naki == Naki.NONE:
                selected_action = Action.NOACT.value
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
            print(f"----------------------------------\nPlayer: {player.name}")
            print(f"Jikaze: {player.jikaze.name}")
            if discard:
                print(f"The discarded tile is: {tile_unicode}")
            else:
                print(f"Drawn tile is: {tile_unicode}")

            self.show_tiles(hand_tiles, player.kawa, player.kabe)

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
        print("Please selected the tile you want to discard:")
        self.show_tiles(hand_tiles, discard=True)

        discard = pyinput.inputNum(
            "Discard tile No.: ",
            min=0,
            max=len(hand_tiles) - 1
        )
        discard_tile = hand_tiles[discard]
        print(f"Tile to discard: \n{unicode_block[discard_tile.index]}")

        return hand_tiles[discard]


class UserInquirerInput(CliInput):

    def parse_options(self, action_list):
        action_options = set()
        for act, naki, possible_huros in action_list:
            action_options.add(act.name)

        return list(action_options)

    def parse_naki_options(self, action_list):
        naki_choices = set()
        naki_huros = {}
        for act, naki, possible_huros in action_list:
            if act == Action.NAKI:
                naki_choices.add(str(naki.name))
                naki_huros[naki] = possible_huros
        naki_choices.add("Cancel")

        return list(naki_choices), naki_huros

    def get_naki(self, action_list):
        naki_choices, naki_huros = self.parse_naki_options(action_list)
        questions = [
            inquirer.List('naki',
                          message="Please select naki type:",
                          choices=naki_choices),
        ]
        selected_naki = inquirer.prompt(questions)['naki']

        if selected_naki == "Cancel":
            return Naki.NONE, None

        selected_naki = Naki[selected_naki]

        possible_huro_opt = []
        possible_huro_dict = {}
        for huro in naki_huros[selected_naki]:
            huro_str = " ".join([unicode_block[h.index] for h in huro])
            possible_huro_opt.append(huro_str)
            possible_huro_dict[huro_str] = huro
        possible_huro_opt.append("Cancel")

        questions = [
            inquirer.List('huro',
                          message="Please select huro set:",
                          choices=possible_huro_opt),
        ]
        selected_huro = inquirer.prompt(questions)['huro']

        if selected_huro == "Cancel":
            return Naki.NONE, None

        return selected_naki, possible_huro_dict[selected_huro]

    def actions_with_new_tile(self, action_list):
        action_options = self.parse_options(action_list)
        questions = [
            inquirer.List('action',
                          message="Please select action:",
                          choices=action_options,),
        ]
        selected_action = Action[inquirer.prompt(questions)['action']]

        selected_naki = None
        selected_huro = None
        if selected_action == Action.NAKI:
            selected_naki, selected_huro = self.get_naki(action_list)
            if selected_naki == Naki.NONE:
                selected_action = Action.NOACT
        elif selected_action == Action.RON:
            print("Player RON!")
        elif selected_action == Action.TSUMO:
            print("Player TSUMO!")
        else:
            ...

        naki = Naki(selected_naki) if selected_naki else None

        return selected_action, naki, selected_huro

    def actions(self, player, new_tile, action_list, discard):
        if (action_list == [(Action.NOACT, Naki.NONE, [])]) and discard:
            return Action.NOACT, Naki.NONE, []
        else:
            hand_tiles = convert_hand(player.hand)
            tile_unicode = unicode_block[new_tile.index]
            print(f"----------------------------------\nPlayer: {player.name}")
            print(f"Jikaze: {player.jikaze.name}")
            if discard:
                print(f"The discarded tile is: {tile_unicode}")
            else:
                print(f"Drawn tile is: {tile_unicode}")

            if action_list == [(Action.NOACT, Naki.NONE, [])]:
                return Action.NOACT, Naki.NONE, []
            else:
                self.show_tiles(hand_tiles, player.kawa, player.kabe)
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

        self.show_tiles(hand_tiles, discard=True)
        tiles_dict = {}
        tiles_opt = set()
        for tile in hand_tiles:
            tiles_dict[unicode_block[tile.index]] = tile
            tiles_opt.add(unicode_block[tile.index])
        questions = [
            inquirer.List(
                'tile_to_discard',
                message="Please selected the tile you want to discard:",
                choices=sorted(list(tiles_opt)),
                carousel=True),
        ]
        tile = inquirer.prompt(questions)['tile_to_discard']
        discard_tile = tiles_dict[tile]

        print(f"Tile to discard: \n{unicode_block[discard_tile.index]}")

        return discard_tile


def input_switch(input_method):
    if input_method == 'raw_input':
        return UserRawInput()
    elif input_method == 'inquirer':
        return UserInquirerInput()
    else:
        raise ValueError('input method should be raw_input or inquirer')
