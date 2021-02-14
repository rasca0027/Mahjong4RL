from typing import List, Tuple

from .yaku_types import (
    JouKyouYaku, TeYaku, Yakuhai, Peikou, Chanta, Koutsu, Sanshoku, Somete,
)


class YakuCalculator():
    def __init__(self, player, stack, bakaze, is_ron):
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
        fu = self.calculate_fu()
        return final_hans, fu

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

    def calculate_fu(self):
        pass
