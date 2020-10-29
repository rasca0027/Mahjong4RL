from typing import List

from .player import Player
from .components import Jihai
from .kyoku import Kyoku


class Game:
    def __init__(self, player_names: List[str]):
        self.bakaze = Jihai.TON
        self.kyoku_num = 1  # e.g.東1局
        self.players = self.get_init_players(player_names)
        self.current_kyoku = Kyoku(self.players, 0, self.bakaze, 0)

    def get_init_players(self, player_names):
        players = []
        for i, name in enumerate(player_names):
            players.append(Player(name, i))
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
            self.current_kyoku = Kyoku(self.players, honba,
                                       self.bakaze, kyotaku)
        # 遊戲結束
        self.end_game()

    def check_tobu(self):
        return any(filter(lambda p: p.points < 0, self.players))

    def end_game(self):
        ...
