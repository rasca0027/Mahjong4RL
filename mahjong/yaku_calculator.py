import copy
import math
from typing import List, Tuple

from .components import Tile, Naki
from .helpers import separate_sets
from .naki_and_actions import check_tenpai
from .yaku_types import (
    JouKyouYaku, TeYaku, Yakuhai, Peikou, Chanta, Koutsu, Sanshoku, Somete,
)


class YakuCalculator():
    def __init__(self, player, stack, bakaze, is_ron):
        self.player = player
        self.bakaze = bakaze
        self.is_ron = is_ron
        self.joukyouyaku_eval = JouKyouYaku(player, stack, bakaze, is_ron)
        self.teyaku_eval = TeYaku(player, stack, bakaze, is_ron)
        self.yakuhai_eval = Yakuhai(player, stack, bakaze, is_ron)
        self.peikou_eval = Peikou(player, stack, bakaze, is_ron)
        self.chanta_eval = Chanta(player, stack, bakaze, is_ron)
        self.koutsu_eval = Koutsu(player, stack, bakaze, is_ron)
        self.sanshoku_eval = Sanshoku(player, stack, bakaze, is_ron)
        self.somete_eval = Somete(player, stack, bakaze, is_ron)
        self.evaluations = [
            self.joukyouyaku_eval,
            self.teyaku_eval,
            self.yakuhai_eval,
            self.peikou_eval,
            self.chanta_eval,
            self.koutsu_eval,
            self.sanshoku_eval,
            self.somete_eval,
        ]

    def calculate(self):
        """Iterate through yaku evaluations and calculate valid yakus.

        Start from the starting node of each type of yaku series, if it matches
        then stop iterating in that series; if not continue. Then filter out
        the mutually exclusive yakus, finally returning total han and fu.
        If `use_chain` is False, will continute even if current eval is True.

        :return: int, han and fu
        """
        possible_yakus: List[Tuple[str, int]] = []
        for evaluation in self.evaluations:
            all_evals = evaluation.get_all_evals()
            use_chain = evaluation.use_chain

            for current_eval in all_evals:
                if current_eval():
                    possible_yakus.append((
                        evaluation.total_yaku[-1], evaluation.total_han[-1]))
                    if use_chain:
                        break
        # filter contradictory yakus
        final_yakus = self.filter_yaku(possible_yakus)
        final_hans = sum(han for yaku_name, han in final_yakus)
        fu = self.calculate_fu(final_yakus, final_hans)
        return final_hans, fu

    def has_at_least_one_yaku(self):
        """Check if player has at least one yaku.

        Similar to the `calculate` method, but doesn't need to run all
        evaluations, can return if any of it is True.

        :return: bool, if player has at least one yaku
        """
        for evaluation in self.evaluations:
            all_evals = evaluation.get_all_evals()
            for current_eval in all_evals:
                if current_eval():
                    return True
        return False

    def filter_yaku(
            self, yakus: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
        """Filter out mutually exclusive yakus."""
        YAKU_EXCLUDE_TABLE = {
            'menzen_tsumo': [],
            'ryanpeikou': ['chiitoitsu'],
            # TODO: fill in table
        }
        yaku_list = [yaku for yaku, han in yakus]
        for yaku_name in yaku_list:
            if yaku_name in YAKU_EXCLUDE_TABLE:
                excluded_yakus = YAKU_EXCLUDE_TABLE[yaku_name]
                yakus = list(filter(
                    lambda x: x[0] not in excluded_yakus, yakus))
        return yakus

    def calculate_fu(self, final_yakus: List[Tuple[str, int]], total_han: int):

        total_yaku: List[str] = [yaku_name for yaku_name, han in final_yakus]

        if self.player.menzenchin and self.is_ron:
            fu = 30
        else:
            fu = 20

        if 'pinfu' in total_yaku:
            if total_han == 1:
                fu = 30  # avoid 1 han 20 fu
            return fu
        elif 'chiitoitsu' in total_yaku:
            fu = 25
            return fu

        honor_tiles, terminal_tiles = Tile.get_yaochuuhai()
        yaochuuhai = honor_tiles + terminal_tiles
        for huro in self.player.kabe:
            if huro.naki_type == Naki.PON:
                if huro.tiles[0] in yaochuuhai:
                    fu += 4
                else:
                    fu += 2
            elif huro.naki_type == Naki.ANKAN:
                if huro.tiles[0] in yaochuuhai:
                    fu += 32
                else:
                    fu += 16
            elif huro.naki_type in [Naki.DAMINKAN, Naki.CHAKAN]:
                if huro.tiles[0] in yaochuuhai:
                    fu += 16
                else:
                    fu += 8

        def calc_wait_pattern_fu(ankous: List[Tile],
                                 shuntsus: List[Tile],
                                 jantou: Tile) -> int:
            wait_pattern_fu = 0

            # 暗刻
            for tile in ankous:
                if tile in yaochuuhai:
                    wait_pattern_fu += 8
                else:
                    wait_pattern_fu += 4

            # 雀頭
            if jantou.suit == 0:
                if jantou.rank == self.bakaze.value:
                    wait_pattern_fu += 2
                if jantou.rank == self.player.jikaze.value:
                    wait_pattern_fu += 2

            # 聽牌形式
            def tenpai_add_fu() -> bool:
                if self.player.agari_tile == jantou:  # 單騎聽
                    return True
                for shuntsu in shuntsus:
                    if self.player.agari_tile == shuntsu[1]:  # 坎張聽
                        return True
                    elif (
                        (self.player.agari_tile == shuntsu[0]
                         and shuntsu[2].rank == 9)
                        or (self.player.agari_tile == shuntsu[2]
                            and shuntsu[0].rank == 1)
                    ):
                        return True  # 邊張聽
                return False

            if tenpai_add_fu():
                wait_pattern_fu += 2

            return wait_pattern_fu

        # separate sets
        tenpai_tiles = check_tenpai(self.player.hand, self.player.kabe)
        player_huro_n = len(self.player.kabe)
        wait_patterns = {}
        for idx, pot_agari_tile in enumerate(tenpai_tiles):
            tmp_agari_hand = copy.deepcopy(self.player.hand)
            tmp_agari_hand[pot_agari_tile.index] += 1

            ankous, shuntsus, jantou = separate_sets(tmp_agari_hand,
                                                     player_huro_n)
            wait_patterns[idx] = [ankous, shuntsus, jantou]

        wait_pattern_fus = []
        for idx in wait_patterns.keys():
            [ankous, shuntsus, jantou] = wait_patterns[idx]
            wait_pattern_fus.append(
                calc_wait_pattern_fu(ankous, shuntsus, jantou))

        wait_pattern_fu = max(wait_pattern_fus)
        fu += wait_pattern_fu
        # round up
        return int(math.ceil(fu / 10.0)) * 10
