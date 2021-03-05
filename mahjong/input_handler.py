from typing import List, Optional, Tuple, TYPE_CHECKING
from abc import ABC, abstractmethod
from random import randrange

import pyinputplus as pyinput

from forked_inquirer.forked_inquirer import inquirer, InquirerList, BlueTheme
from .helpers import convert_hand
from .utils import unicode_block
from .components import Tile, Action, Naki, Huro
if TYPE_CHECKING:
    from .player import Player


class UserInput(ABC):

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
                    hand_representation += f"{tile_unicode}"
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
                        hand_representation += f"{tile_unicode}"
                    elif i == len(hand_tiles) - 2 :
                        hand_representation += f" {tile_unicode}|"
                    else:
                        hand_representation += f" {tile_unicode} "

        hand_representation += "\n"
        if kawa:
            hand_representation += "----- Tiles in kawa -----\n"
            for tile in kawa:
                hand_representation += f"{unicode_block[tile.index]}"
            hand_representation += "\n"
        if kabe:
            hand_representation += "----- Kabe -----\n"
            for huro in kabe:
                for tile in huro.tiles:
                    hand_representation += f"{unicode_block[tile.index]}"
        print(hand_representation)

    @abstractmethod
    def actions_with_new_tile(self, action_list):
        return NotImplemented

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

    @abstractmethod
    def select_discard(self, hand_tiles, kuikae_tiles, new_tile):
        return NotImplemented

    def discard(self, player, new_tile, kuikae_tiles):
        hand_tiles = convert_hand(player.hand)
        if new_tile:
            hand_tiles.append(new_tile)

        self.show_tiles(hand_tiles, player.kawa, player.kabe, discard=True)

        return self.select_discard(hand_tiles, kuikae_tiles, new_tile)


class UserRawInput(CliInput):

    def parse_options(self, action_list):
        options_str = ""
        act_values = set()
        for act, naki, possible_huros in action_list:
            act_values.add(act.value)

        for act_value in act_values:
            options_str += f"{act_value}: {Action(act_value).name}\n"

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
            huro_str = "".join([unicode_block[h.index] for h in huro])
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

        naki = Naki(selected_naki) if selected_naki else None

        return Action(selected_action), naki, selected_huro

    def select_discard(self, hand_tiles, kuikae_tiles, new_tile):
        if kuikae_tiles:
            # not allowed to choose from this list
            # TODO: now just hide from hand_representation,
            # need to change to something else if UI changes
            hand_tiles = [tile for tile in hand_tiles
                          if tile not in kuikae_tiles]
        if player.is_riichi and new_tile:
            hand_tiles = [new_tile]
        self.show_tiles(hand_tiles, discard=True)
        print("Please select the tile you want to discard:")
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
        action_options_dict = {}
        for act, naki, possible_huros in action_list:
            if act == Action.NAKI:
                for huro in possible_huros:
                    huro_str = " ".join([unicode_block[h.index] for h in huro])
                    act_str = f"{naki.name} -> {huro_str}"
                    action_options.add(act_str)
                    action_options_dict[act_str] = [act, naki, huro]
            else:
                act_str = 'Cancel' if act == Action.NOACT else act.name
                action_options.add(act_str)
                action_options_dict[act_str] = [act, naki, possible_huros]

        return sorted(list(action_options)), action_options_dict

    def actions_with_new_tile(self, action_list):
        action_options, act_dict = self.parse_options(action_list)
        questions = [
            InquirerList(
                'action',
                message="Please select action",
                choices=action_options,),
        ]
        selected_action = inquirer.prompt(questions)['action']
        action, naki, huro = act_dict[selected_action]

        return action, naki, huro

    def select_discard(self, hand_tiles, kuikae_tiles, new_tile):
        tiles_dict = {}
        tiles_opt = set()
        for tile in hand_tiles:
            if tile not in kuikae_tiles:
                tiles_dict[unicode_block[tile.index]] = tile
                tiles_opt.add(unicode_block[tile.index])
        tiles_opt_ls = sorted(list(tiles_opt))
        # move new tile to the front
        if new_tile:
            tiles_opt_ls.insert(0, tiles_opt_ls.pop(
                tiles_opt_ls.index(unicode_block[new_tile.index])))
        if is_riichi and new_tile:
            tiles_opt_ls = [unicode_block[new_tile.index]]
        questions = [
            InquirerList(
                'tile_to_discard',
                message="Please select the tile you want to discard",
                choices=tiles_opt_ls,
                carousel=True,
                vertical=False),
        ]
        tile = inquirer.prompt(questions,
                               theme=BlueTheme())['tile_to_discard']
        discard_tile = tiles_dict[tile]

        print(f"Tile to discard: \n{unicode_block[discard_tile.index]}")

        return discard_tile


class DummyInput(CliInput):

    def actions_with_new_tile(self, action_list):
        # pick a random action
        action, naki, huro_list = action_list[randrange(len(action_list))]
        if huro_list:
            # pick a random huro
            huro = huro_list[randrange(len(huro_list))]
        else:
            huro = None
        return action, naki, huro

    def actions(self, player, new_tile, action_list, discard):
        if (action_list == [(Action.NOACT, Naki.NONE, [])]) and discard:
            return Action.NOACT, Naki.NONE, []
        else:
            if not discard:
                print("\n----------------------------------")
                print(f"A.I. player {player.name} draw a tile")
            return self.actions_with_new_tile(action_list)

    def select_discard(self, hand_tiles, kuikae_tiles):
        hand_tiles = [tile for tile in hand_tiles
                      if tile not in kuikae_tiles]
        # pick a random tile to discard
        discard_tile = hand_tiles[randrange(len(hand_tiles))]
        print(f"Tile to discard: \n{unicode_block[discard_tile.index]}")

        return discard_tile

    def discard(self, player, new_tile, kuikae_tiles):
        hand_tiles = convert_hand(player.hand)
        if new_tile:
            hand_tiles.append(new_tile)

        print(f"----------------------------------\nPlayer: {player.name}")
        print(f"Jikaze: {player.jikaze.name}")
        hand_representation = ""
        if player.kawa:
            hand_representation += "----- Tiles in kawa -----\n"
            for tile in player.kawa:
                tile_unicode = unicode_block[tile.index]
                if tile.index == 3:
                    hand_representation += f"{tile_unicode}"
                else:
                    hand_representation += f"{tile_unicode} "
            hand_representation += "\n"
        if player.kabe:
            hand_representation += "----- Kabe -----\n"
            for huro in player.kabe:
                for tile in huro.tiles:
                    tile_unicode = unicode_block[tile.index]
                    if tile.index == 3:
                        hand_representation += f"{tile_unicode}"
                    else:
                        hand_representation += f"{tile_unicode} "
        print(hand_representation)

        return self.select_discard(hand_tiles, kuikae_tiles)


def input_switch(input_method):
    if input_method == 'raw_input':
        return UserRawInput()
    elif input_method == 'inquirer':
        return UserInquirerInput()
    elif input_method == 'dummy':
        return DummyInput()
    else:
        raise ValueError('input method should be raw_input, inquirer or dummy')
