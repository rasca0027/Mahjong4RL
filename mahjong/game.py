import json
import os
from typing import List, Optional

from pyfiglet import Figlet

from .player import Player
from .components import Jihai
from .kyoku import Kyoku


class Game:
    def __init__(
        self,
        player_names: List[str],
        config_file: Optional[str] = 'config.json'
    ):
        self.bakaze = Jihai.TON
        self.kyoku_num = 1  # e.g.東1局
        self.config_file = config_file
        self.game_config, self.custom_rules = self.load_config()
        self.players = self.get_init_players(player_names,
                                             self.game_config['input'],
                                             self.game_config['A.I. players'])
        self.current_kyoku = Kyoku(self.players,
                                   custom_rules=self.custom_rules,
                                   debug_mode=self.game_config['debug mode'])
        figlet = Figlet(font='slant')
        print(figlet.renderText('Mahjong 4 RL'))
        print('\n----------------------------------')
        print('Initiating a game...')
        print(f"Debug mode: {self.game_config['debug mode']}")
        print(f"Game type: {self.game_config['game type']}")
        print('Players in game:')
        for player in self.players:
            print(f'    {player.seating_position}-{player.name}')
        print('Rules in this game:')
        for k, v in self.custom_rules.items():
            print(f'    {k}: {v}')
        if self.game_config['debug mode']:
            input("\nPress enter to continue...")
            print(chr(27) + "[2J")

    def load_config(self):
        parent_directory = os.path.split(os.path.dirname(__file__))[0]
        with open(os.path.join(parent_directory,
                               'configs',
                               self.config_file)) as f:
            config = json.load(f)

        return config['Game Config'], config['Custom Rules']

    def get_init_players(self, player_names, input_method, ai_players):
        players = []
        for i, name in enumerate(player_names):
            if i in ai_players:
                players.append(Player(name, i, 'dummy'))
            else:
                players.append(Player(name, i, input_method))
        return players

    def start_game(self):
        while True:
            print('\n----------------------------------')
            print('Starting Kyoku...')
            print(f"{self.bakaze.name} {self.kyoku_num} Kyoku")
            renchan, kyotaku, honba = self.current_kyoku.start()
            if self.check_tobu():  # 有人被飛
                break
            if not renchan:
                if self.check_lask_kyoku():
                    break  # end game
                elif self.kyoku_num == 4:
                    self.bakaze == Jihai.NAN
                    self.kyoku_num = 1
                else:
                    self.kyoku_num += 1
                # advance player jikaze
                for player in self.players:
                    player.advance_jikaze()
            else:
                # 最後一局如果已經是第一名的話，不繼續連莊，直接結束遊戲
                # TODO: 是否考慮西入
                if self.is_all_last():
                    break
                else:
                    pass

            input("\nPress enter to enter next kyoku...")
            print(chr(27) + "[2J")
            for player in self.players:
                player.reset_state()

            self.current_kyoku = Kyoku(self.players,
                                       bakaze=self.bakaze,
                                       honba=honba,
                                       kyotaku=kyotaku,
                                       custom_rules=self.custom_rules)
        # 遊戲結束
        self.end_game()

    def check_tobu(self):
        return any(filter(lambda p: p.points < 0, self.players))

    def ckeck_last_kyoku(self) -> bool:
        is_last_kyoku = (
            (
                self.game_config["game type"] == "hanchan"
                and self.bakaze == Jihai.NAN
                and self.kyoku_num == 4
            )
            or (
                self.bakaze == Jihai.TON
                and self.kyoku_num == 4
            )
        )
        return is_last_kyoku

    def is_all_last(self):
        ranked_players = sorted(
            self.players,
            key=lambda p: p.points,
            reverse=True,
        )
        if self.ckeck_last_kyoku() and (
            ranked_players[0].jikaze == Jihai.TON
            and ranked_players[0].points > ranked_players[1].points
        ):
            return True
        return False

    def end_game(self):
        print('\n----------------------------------')
        print('End Game')
        ranked_players = sorted(
            self.players, key=lambda x: x.points, reverse=True)
        for i, player in enumerate(ranked_players):
            lname = f"No. {i + 1}: player {player.name} ".ljust(30)
            print(f"{lname}{player.points} points")
