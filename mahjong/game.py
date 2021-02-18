import json
import os
import sys
from typing import List

from .player import Player
from .components import Jihai
from .kyoku import Kyoku


class Game:
    def __init__(self, player_names: List[str]):
        self.bakaze = Jihai.TON
        self.kyoku_num = 1  # e.g.東1局
        self.game_config, self.custom_rules = self.load_config()
        self.players = self.get_init_players(player_names,
                                             self.game_config['input'])
        self.current_kyoku = Kyoku(self.players,
                                   custom_rules=self.custom_rules)

    def load_config(self):
        with open(os.path.join(sys.path[0], 'mahjong/config.json')) as f:
            config = json.load(f)

        return config['Game Config'], config['Custom Rules']

    def get_init_players(self, player_names, input_method):
        players = []
        for i, name in enumerate(player_names):
            players.append(Player(name, i, input_method))
        return players

    def start_game(self):
        while True:
            renchan, kyotaku, honba = self.current_kyoku.start()
            if self.check_tobu():  # 有人被飛
                break
            if not renchan:
                if self.kyoku_num == 4:
                    if self.bakaze == Jihai.NAN:
                        break  # end game
                    elif self.bakaze == Jihai.TON:
                        self.bakaze = Jihai.NAN
                        self.kyoku_num = 1
                else:
                    self.kyoku_num += 1
                # advance player jikaze
                for player in self.players:
                    player.jikaze = Jihai((player.jikaze.value - 3) % 4 + 4)
            self.current_kyoku = Kyoku(self.players,
                                       bakaze=self.bakaze,
                                       honba=honba,
                                       kyotaku=kyotaku,
                                       custom_rules=self.custom_rules)
        # 遊戲結束
        self.end_game()

    def check_tobu(self):
        return any(filter(lambda p: p.points < 0, self.players))

    def end_game(self):
        ...
