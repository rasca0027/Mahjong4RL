import copy
from typing import List, Optional, Callable, TYPE_CHECKING
from collections import defaultdict
from itertools import combinations
from abc import ABC, abstractmethod

from .helpers import (
    is_yaochuu, separate_sets, consists_jantou_and_sets
)
from .components import Suit, Jihai, Tile, Naki, Stack
from .utils import get_name
if TYPE_CHECKING:
    from .player import Player


class YakuTypes(ABC):

    def __init__(
        self, player: 'Player', stack: Stack, machi_tiles: List[Tile],
        bakaze: Jihai, ron: bool, agari_tile: Optional[Tile] = None,
        first_turn: Optional[bool] = False
    ):
        self._total_yaku = []
        self._total_han = []
        self.player = player
        self.machi_tiles = machi_tiles
        self.stack = stack
        self.bakaze = bakaze
        self.is_ron = ron
        self.first_turn = first_turn
        self.agari_tile = agari_tile
        self.agari_hand = copy.deepcopy(self.player.hand)
        self.agari_hand = defaultdict(
            int, {k: v for k, v in self.agari_hand.items() if v > 0})
        if self.player.agari_tile:
            self.agari_tile = self.player.agari_tile
        self.agari_hand[self.agari_tile.index] += 1
        self.huro_tiles = [
            tile for huro in self.player.kabe for tile in huro.tiles]
        self.use_chain = True

    @property
    @abstractmethod
    def total_yaku(self):
        return NotImplemented

    @total_yaku.setter
    @abstractmethod
    def total_yaku(self, yaku):
        return NotImplemented

    @property
    @abstractmethod
    def total_han(self):
        return NotImplemented

    @total_han.setter
    @abstractmethod
    def total_han(self, han):
        return NotImplemented

    @abstractmethod
    def get_all_evals(self):
        return NotImplemented

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, player: 'Player'):
        self._player = player

    @property
    def bakaze(self):
        return self._bakaze

    @bakaze.setter
    def bakaze(self, bakaze):
        self._bakaze = bakaze


class JouKyouYaku(YakuTypes):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_chain = False

    @property
    def total_yaku(self):
        return self._total_yaku

    @total_yaku.setter
    def total_yaku(self, yaku_name):
        self._total_yaku.append(yaku_name)

    @property
    def total_han(self):
        return self._total_han

    @total_han.setter
    def total_han(self, han):
        self._total_han.append(han)

    def get_all_evals(self) -> List[Callable]:
        return [
            self.menzen_tsumo,
            self.chankan,
            self.houtei_raoyui,
            self.riichi,
            self.ippatsu,
            self.haitei_raoyue,
            self.rinshan_kaihou,
            self.daburu_riichi,
            self.tenhou,
            self.chiihou,
        ]

    def menzen_tsumo(self):  # 門前清自摸和
        """A player with a closed tenpai hand may win with tsumo.
        1 han (closed only)
        http://arcturus.su/wiki/Menzenchin_tsumohou
        """
        if self.player.menzenchin and not self.is_ron:
            self.total_yaku = 'menzen_tsumo'
            self.total_han = 1
            return True
        return False

    def chankan(self):  # 搶槓
        """A player may declare ron while a player calls to upgrade
        a minkou (pon) to a kan.
        1 han
        http://arcturus.su/wiki/Chankan
        """
        return False

    def houtei_raoyui(self):  # 河底撈魚
        """Win by last discard.
        1 han
        http://arcturus.su/wiki/Haitei_raoyue_and_houtei_raoyui
        """
        if self.is_ron and self.stack.is_haitei:
            self.total_yaku = 'houtei_raoyui'
            self.total_han = 1
            return True
        return False

    def riichi(self):  # 立直
        """When a player has a closed tenpai hand, the player may declare riichi.
        1 han (closed only)
        http://arcturus.su/wiki/Riichi
        """
        if self.player.is_riichi:
            self.total_yaku = 'riichi'
            self.total_han = 1
            return True
        return False

    def ippatsu(self):  # 一発
        """Winning on or before the next tile draw after riichi.
        1 han
        http://arcturus.su/wiki/Ippatsu
        """
        return False

    def haitei_raoyue(self):  # 海底撈月
        """A player wins with the tsumo on the haiteihai, the last
        drawable tile from the live wall.
        1 han
        http://arcturus.su/wiki/Haitei_raoyue_and_houtei_raoyui
        """
        if not self.is_ron and self.stack.is_haitei:
            self.total_yaku = 'haitei_raoyue'
            self.total_han = 1
            return True
        return False

    def rinshan_kaihou(self):  # 嶺上開花
        """A player wins with the rinshanpai.
        1 han
        http://arcturus.su/wiki/Rinshan_kaihou
        """
        return False

    def daburu_riichi(self):  # 両立直
        """This is a special case for riichi. In this case, the player's start
        hand is already at tenpai from the dealt tiles, or the initial draw
        produces a tenpai hand.
        2 han
        http://arcturus.su/wiki/Daburu_riichi
        """
        return False

    def tenhou(self):  # 天和
        """The dealer hand is a winning hand even before discarding a tile.
        yakuman
        http://arcturus.su/wiki/Tenhou
        """
        if (
            self.player.jikaze == self.bakaze
            and self.first_turn and not self.is_ron
        ):
            self.total_yaku = 'tenhou'
            self.total_han = 13
            return True
        return False

    def chiihou(self):  # 地和
        """The non-dealer hand is a winning hand with the first tile draw.
        yakuman
        http://arcturus.su/wiki/Chiihou
        """
        if self.first_turn and self.is_ron:
            self.total_yaku = 'chiihou'
            self.total_han = 13
            return True
        return False


class TeYaku(YakuTypes):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_chain = False

    @property
    def total_yaku(self):
        return self._total_yaku

    @total_yaku.setter
    def total_yaku(self, yaku_name):
        self._total_yaku.append(yaku_name)

    @property
    def total_han(self):
        return self._total_han

    @total_han.setter
    def total_han(self, han):
        self._total_han.append(han)

    def get_all_evals(self) -> List[Callable]:
        return [
            self.ryuuiisou,
            self.kokushi_musou,
            self.chuuren_poutou,
            self.tsuuiisou,
            self.yakuhai,
            self.toitoihou,
            self.chiitoitsu,
            self.ikkitsuukan,
            self.pinfu,
            self.tanyao,
        ]

    def ryuuiisou(self):  # 緑一色
        """A hand composed entirely of green tiles: 2, 3, 4, 6 and 8 Sou and/or Hatsu.
        yakuman
        http://arcturus.su/wiki/Ryuuiisou
        """
        green_tiles_idx = {Tile(Suit.SOUZU.value, 2).index,
                           Tile(Suit.SOUZU.value, 3).index,
                           Tile(Suit.SOUZU.value, 4).index,
                           Tile(Suit.SOUZU.value, 6).index,
                           Tile(Suit.SOUZU.value, 8).index,
                           Tile(Suit.JIHAI.value, Jihai.HATSU.value).index}

        agari_hand_and_kabe = copy.deepcopy(self.agari_hand)
        for tile in self.huro_tiles:
            agari_hand_and_kabe[tile.index] += 1

        for tile_idx in agari_hand_and_kabe.keys():
            if tile_idx not in green_tiles_idx:
                return False

        self.total_yaku = 'ryuuiisou'
        self.total_han = 13
        return True

    def kokushi_musou(self):  # 国士無双 or 国士無双１３面待ち
        """This hand has one of each of the 13 different terminal
        and honor tiles plus one extra terminal or honour tile.
        Some rules may allow double yakuman for a 13-wait set.
        yakuman
        http://arcturus.su/wiki/Kokushi_musou
        """
        honor_tiles, terminal_tiles = Tile.get_yaochuuhai()
        yaochuuhai = honor_tiles + terminal_tiles

        yaochuu_in_hand = {k: v for (k, v) in self.agari_hand.items()
                           if Tile.from_index(k) in yaochuuhai}
        single_yaochuu_n = sum(v == 1 for v in yaochuu_in_hand.values())
        pair_yaochuu_keys = [k for (k, v) in yaochuu_in_hand.items() if v == 2]
        if (single_yaochuu_n == 12) and (len(pair_yaochuu_keys) == 1):
            if pair_yaochuu_keys[0] == self.agari_tile.index:
                # 13-way wait
                self.total_yaku = 'kokushi musou 13-way wait'
                self.total_han = 26
            else:  # single wait
                self.total_yaku = 'kokushi musou'
                self.total_han = 13
            return True

        return False

    def chuuren_poutou(self):  # 九連宝燈 or 純正九蓮宝燈
        """A hand consisting of the tiles 1112345678999 in the same suit plus
        any one extra tile of the same suit.
        yakuman
        http://arcturus.su/wiki/Chuuren_poutou
        """
        suit_in_hand = set([Tile.suit_from_idx(k)
                            for k in self.agari_hand.keys()])
        if len(suit_in_hand) == 1 and (suit_v := list(suit_in_hand)[0]) != 0:
            tmp_hand = copy.deepcopy(self.agari_hand)
            for i in [1, 9]:
                if tmp_hand[Tile(suit_v, i).index] < 3:
                    return False
                else:
                    tmp_hand[Tile(suit_v, i).index] -= 3
            for i in range(2, 9):
                if tmp_hand[Tile(suit_v, i).index] < 1:
                    return False
                else:
                    tmp_hand[Tile(suit_v, i).index] -= 1

            remain_tile = [k for k, v in tmp_hand.items() if v > 0][0]
            if self.agari_tile.index == remain_tile:
                self.total_yaku = 'junsei chuuren poutou'
                self.total_han = 26
            else:
                self.total_yaku = 'chuuren poutou'
                self.total_han = 13
            return True

        return False

    def tsuuiisou(self):  # 字一色
        """Every group of tiles are composed of honor tiles.
        yakuman
        http://arcturus.su/wiki/Tsuuiisou
        """
        suit_in_hand = set([Tile.suit_from_idx(k)
                            for k in self.agari_hand.keys()])
        suit_in_huro = set([tile.suit for tile in self.huro_tiles])
        suit = suit_in_hand | suit_in_huro

        if len(suit) == 1 and list(suit)[0] == 0:
            self.total_yaku = 'tsuuiisou'
            self.total_han = 13
            return True
        return False

    def yakuhai(self):  # 役牌
        """A group of 1 han yaku scored for completing a group of certain
        honour tiles:
        1. sangenpai (三元牌)
        2. bakaze (場風)
        3. jikaze (自風)
        1 han per counted triplet
        http://arcturus.su/wiki/Yakuhai
        """
        yakuhai = {'sangenpai': [Jihai.HAKU, Jihai.HATSU, Jihai.CHUN],
                   'bakaze': [self.bakaze],
                   'jikaze': [self.player.jikaze]}

        agari_hand_and_kabe = copy.deepcopy(self.agari_hand)
        for tile in self.huro_tiles:
            agari_hand_and_kabe[tile.index] += 1

        found_yakuhai = False
        for tile_type, tile_list in yakuhai.items():
            for tile in tile_list:
                tile_index = Tile(Suit.JIHAI.value, tile.value).index
                if agari_hand_and_kabe[tile_index] >= 3:
                    self.total_yaku = f"{tile_type}_{get_name(Jihai, tile)}"
                    self.total_han = 1
                    found_yakuhai = True

        return found_yakuhai

    def toitoihou(self):  # 対々和
        """All triplets.
        2 han
        http://arcturus.su/wiki/Toitoihou
        """
        appear_twice = 0
        for idx, cnt in self.agari_hand.items():
            if cnt == 1:
                return False
            elif cnt == 2:
                appear_twice += 1
            elif cnt == 3:
                continue
            else:
                return False
        # check with huro
        for huro in self.player.kabe:
            if huro.tiles[0] == huro.tiles[1]:
                continue
            else:
                return False
        if appear_twice != 1:
            return False
        self.total_yaku = "toitoihou"
        self.total_han = 2
        return True

    def chiitoitsu(self):  # 七対子
        """This hand is composed of seven pairs.
        It is one of two exceptions to the standard 4 tile groups and
        a pair pattern.
        2 han
        http://arcturus.su/wiki/Chiitoitsu
        """
        if len([k for k, v in self.agari_hand.items() if v == 2]) == 7:
            self.total_yaku = 'chiitoitsu'
            self.total_han = 2
            return True

        return False

    def ikkitsuukan(self):  # 一気通貫
        """Three distinct tile groups containing 123, 456, 789 of one suit.
        2 han
        1 han (open)
        http://arcturus.su/wiki/Ikkitsuukan
        """
        agari_hand_and_kabe = copy.deepcopy(self.agari_hand)
        for tile in self.huro_tiles:
            agari_hand_and_kabe[tile.index] += 1

        for suit in Suit:
            if suit != Suit.JIHAI:
                tmp_hand = copy.deepcopy(agari_hand_and_kabe)

                for i in range(1, 10):
                    if tmp_hand[Tile(suit.value, i).index] < 1:
                        break
                    else:
                        tmp_hand[Tile(suit.value, i).index] -= 1
                else:
                    if consists_jantou_and_sets(tmp_hand, 3):
                        self.total_yaku = 'ikkitsuukan'
                        if self.player.menzenchin:
                            self.total_han = 2
                        else:
                            self.total_han = 1
                        return True

        return False

    def pinfu(self):  # 平和
        """Defined by having 0 fu aside from the base 20 fu, or 30 fu in
        the case of a closed ron.
        1 han (closed only)
        http://arcturus.su/wiki/Pinfu
        """
        huro_count = len(self.player.kabe)
        _, shuntsus, jantou = separate_sets(self.agari_hand, huro_count)

        yakuhai_v = [Jihai.HAKU.value, Jihai.HATSU.value, Jihai.CHUN.value,
                     self.bakaze.value, self.player.jikaze.value]

        def is_ryanmen() -> bool:  # 两面听牌
            wait_patterns = {}
            for idx, pot_agari_tile in enumerate(self.machi_tiles):
                tmp_agari_hand = copy.deepcopy(self.player.hand)
                tmp_agari_hand[pot_agari_tile.index] += 1

                _, shuntsus, jantou = separate_sets(tmp_agari_hand, 0)
                wait_patterns[idx] = [shuntsus, jantou]

            ryanmen = False
            for idx in wait_patterns.keys():
                [shuntsus, jantou] = wait_patterns[idx]
                if self.agari_tile == jantou:  # 單騎聽
                    continue
                for shuntsu in shuntsus:
                    if self.agari_tile == shuntsu[1]:  # 坎張聽
                        continue
                    elif (
                        (self.agari_tile == shuntsu[0]
                         and shuntsu[2].rank == 9)
                        or (self.agari_tile == shuntsu[2]
                            and shuntsu[0].rank == 1)
                    ):
                        continue  # 邊張聽
                ryanmen = True

            return ryanmen

        if (
            len(shuntsus) == 4  # 四個順子
            and jantou.rank not in yakuhai_v  # 雀頭不是役牌
            and is_ryanmen()  # 两面听牌
        ):
            self.total_yaku = "pinfu"
            self.total_han = 1
            return True

        return False

    def tanyao(self):  # 断么九
        """A hand contain only numbered tiles 2-8 from any of the three main suits.
        1 han
        https://riichi.wiki/Tanyao
        """
        # check player's hand
        for k in self.agari_hand.keys():
            suit = Tile.suit_from_idx(k)
            rank = Tile.rank_from_idx(k)
            if is_yaochuu(suit=suit, rank=rank):
                return False

        # check player's kabe
        for tile in self.huro_tiles:
            if is_yaochuu(suit=tile.suit, rank=tile.rank):
                return False

        self.total_yaku = 'tanyao'
        self.total_han = 1
        return True


class Yakuhai(TeYaku):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_all_evals(self) -> List[Callable]:
        return [
            self.daisangen,
            self.daisuushii,
            self.shousuushii,
            self.shousangen,
        ]

    def daisangen(self):  # 大三元
        """This hand possesses three groups (triplets or quads) of all the dragons.
        yakuman
        http://arcturus.su/wiki/Daisangen
        """
        for rank in [Jihai.HAKU, Jihai.HATSU, Jihai.CHUN]:
            tile = Tile(Suit.JIHAI.value, rank.value)
            index = tile.index
            if self.agari_hand[index] >= 3:
                continue
            elif tile in self.huro_tiles:
                continue
            else:
                return False
        self.total_yaku = "daisangen"
        self.total_han = 13
        return True

    def daisuushii(self):  # 大四喜
        """This hand has four groups (triplets or quads) of
        all four wind tiles.
        yakuman
        http://arcturus.su/wiki/Daisuushii
        """
        four_winds = [Jihai.TON, Jihai.NAN, Jihai.SHAA, Jihai.PEI]
        for rank in four_winds:
            tile = Tile(Suit.JIHAI.value, rank.value)
            index = tile.index
            if self.agari_hand[index] >= 3:
                continue
            elif tile in self.huro_tiles:
                continue
            else:
                return False
        self.total_yaku = "daisuushii"
        self.total_han = 13
        return True

    def shousuushii(self):  # 小四喜
        """This hand has three groups (triplets or quads)
        of the wind tiles plus a pair of the fourth kind.
        yakuman
        http://arcturus.su/wiki/Shousuushii
        """
        four_winds = [Jihai.TON, Jihai.NAN, Jihai.SHAA, Jihai.PEI]
        has_small_flag = False
        for rank in four_winds:
            tile = Tile(Suit.JIHAI.value, rank.value)
            index = tile.index
            tile_cnt = self.agari_hand.get(index, 0)
            if tile_cnt == 3:
                continue
            elif tile in self.huro_tiles:
                continue
            elif tile_cnt == 2 and not has_small_flag:
                has_small_flag = True
                continue
            elif tile_cnt == 2 and has_small_flag:
                return False
            else:
                return False
        self.total_yaku = "shousuushii"
        self.total_han = 13
        return True

    def shousangen(self):  # 小三元
        """The hand is composed of two koutsu (triplet) and a jantou (pair)
        of the three sangenpai (三元牌)
        2 han (the hand will almost always score at least mangan,
        see the link below)
        http://arcturus.su/wiki/Shousangen
        """
        has_small_flag = False
        for rank in [Jihai.HAKU, Jihai.HATSU, Jihai.CHUN]:
            tile = Tile(Suit.JIHAI.value, rank.value)
            index = tile.index
            tile_cnt = self.agari_hand.get(index, 0)
            if tile_cnt >= 3:
                continue
            elif tile in self.huro_tiles:
                continue
            elif tile_cnt == 2 and not has_small_flag:
                has_small_flag = True
            elif tile_cnt == 2:
                return False
            else:
                return False
        self.total_yaku = "shousangen"
        self.total_han = 2
        return True


class Peikou(TeYaku):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_all_evals(self) -> List[Callable]:
        return [
            self.ryanpeikou,
            self.iipeikou,
        ]

    def ryanpeikou(self):  # 二盃口
        """A hand consisting of two "iipeikou"
        3 han (closed only)
        http://arcturus.su/wiki/Ryanpeikou
        """
        huro_count = len(self.player.kabe)
        _, shuntsu, _ = separate_sets(self.agari_hand, huro_count)

        peikou = 0
        for i in combinations(shuntsu, 2):
            if i[0] == i[1]:
                peikou += 1

        if peikou == 2:
            self.total_yaku = "ryanpeikou"
            self.total_han = 3
            return True
        else:
            return False

    def iipeikou(self):  # 一盃口
        """A hand contain two identical sequences.
        1 han (closed only)
        http://arcturus.su/wiki/Iipeikou
        """
        huro_count = len(self.player.kabe)
        _, shuntsu, _ = separate_sets(self.agari_hand, huro_count)

        peikou = 0
        for i in combinations(shuntsu, 2):
            if i[0] == i[1]:
                peikou += 1

        if peikou == 1:
            self.total_yaku = "iipeikou"
            self.total_han = 1
            return True
        else:
            return False


class Chanta(TeYaku):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_all_evals(self) -> List[Callable]:
        return [
            self.chinroutou,
            self.honroutou,
            self.junchantaiyaochuu,
            self.chanta,
        ]

    def chinroutou(self):  # 清老頭
        """Every group of tiles are composed of terminal tiles.
        yakuman
        http://arcturus.su/wiki/Chinroutou
        """
        for k in self.agari_hand.keys():
            suit = Tile.suit_from_idx(k)
            rank = Tile.rank_from_idx(k)
            if not is_yaochuu(suit=suit, rank=rank) or suit == 0:
                return False

        for tile in self.huro_tiles:
            if (not is_yaochuu(suit=tile.suit, rank=tile.rank)
                    or tile.suit == 0):
                return False

        self.total_yaku = 'chinroutou'
        self.total_han = 13
        return True

    def honroutou(self):  # 混老頭
        """A hand contain only honors and terminals.
        2 han (It is impossible to score this yaku without at least either
        toitoi or chiitoitsu. So, this yaku is actually at minimum, the
        equivalent of 4 han)
        http://arcturus.su/wiki/Honroutou
        """
        for k in self.agari_hand.keys():
            suit = Tile.suit_from_idx(k)
            rank = Tile.rank_from_idx(k)
            if not is_yaochuu(suit=suit, rank=rank):
                return False

        for tile in self.huro_tiles:
            if not is_yaochuu(suit=tile.suit, rank=tile.rank):
                return False

        self.total_yaku = 'honroutou'
        self.total_han = 2
        return True

    def junchantaiyaochuu(self):  # 純全帯么九
        """Every tile group and the pair must contain at least one terminal.
        3 han
        2 han (open)
        http://arcturus.su/wiki/Junchantaiyaochuu
        """
        _, terminal_tiles = Tile.get_yaochuuhai()
        koutsus, shuntsus, jantou = separate_sets(self.agari_hand,
                                                  len(self.player.kabe),
                                                  koutsu_first=False)

        if jantou not in terminal_tiles:
            return False

        for shuntsu in shuntsus:
            if (
                shuntsu[0] not in terminal_tiles
                and shuntsu[2] not in terminal_tiles
            ):
                return False

        for koutsu in koutsus:
            if koutsu not in terminal_tiles:
                return False

        for huru in self.player.kabe:
            if huru.naki_type == Naki.CHII:
                if (
                    huru.tiles[0] not in terminal_tiles
                    and huru.tiles[2] not in terminal_tiles
                ):
                    return False
            else:
                if huru.tiles[0] not in terminal_tiles:
                    return False

        self.total_yaku = 'junchantaiyaochuu'
        if self.player.menzenchin:
            self.total_han = 3
        else:
            self.total_han = 2
        return True

    def chanta(self):  # 混全帯么九
        """Every tile group and the pair must contain at least one terminal or
        honor tile.
        2 han
        1 han (open)
        http://arcturus.su/wiki/Chanta
        """
        honor_tiles, terminal_tiles = Tile.get_yaochuuhai()
        koutsus, shuntsus, jantou = separate_sets(self.agari_hand,
                                                  len(self.player.kabe),
                                                  koutsu_first=False)

        if jantou not in (terminal_tiles + honor_tiles):
            return False

        for shuntsu in shuntsus:
            if (
                shuntsu[0] not in terminal_tiles
                and shuntsu[2] not in terminal_tiles
            ):
                return False

        for koutsu in koutsus:
            if koutsu not in (terminal_tiles + honor_tiles):
                return False

        for huru in self.player.kabe:
            if huru.naki_type == Naki.CHII:
                if (
                    huru.tiles[0] not in terminal_tiles
                    and huru.tiles[2] not in terminal_tiles
                ):
                    return False
            else:
                if huru.tiles[0] not in (terminal_tiles + honor_tiles):
                    return False

        self.total_yaku = 'chanta'
        if self.player.menzenchin:
            self.total_han = 2
        else:
            self.total_han = 1
        return True


class Koutsu(TeYaku):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_all_evals(self) -> List[Callable]:
        return [
            self.suuankou,
            self.suukantsu,
            self.sanankou,
            self.sankantsu,
        ]

    def suuankou(self):  # 四暗刻 or 四暗刻単騎
        """This hand is composed of four groups of closed triplets.
        When this hand has a shanpon pattern and the win is via ron,
        then it would not be counted as such;
        only as the lesser toitoi with sanankou.
        yakuman
        http://arcturus.su/wiki/Suuankou
        """
        huro_count = len(self.player.kabe)
        koutsus, _, jantou = separate_sets(self.agari_hand, huro_count)
        kantsus = [huro for huro in self.player.kabe
                   if huro.naki_type == Naki.ANKAN]
        ankou = len(koutsus) + len(kantsus)

        if ankou == 4:
            if jantou == self.agari_tile:
                self.total_yaku = 'suuankou tanki'
                self.total_han = 26
                return True
            elif not self.is_ron:
                self.total_yaku = 'suuankou'
                self.total_han = 13
                return True

        return False

    def suukantsu(self):  # 四槓子
        """Any hand with four calls of kan.
        yakuman
        http://arcturus.su/wiki/Suukantsu
        """
        kan = [Naki.DAMINKAN, Naki.CHAKAN, Naki.ANKAN]
        kantsus = [huro for huro in self.player.kabe if huro.naki_type in kan]
        if len(kantsus) == 4:
            self.total_yaku = 'suukantsu'
            self.total_han = 13
            return True

        return False

    def sanankou(self):  # 三暗刻
        """A hand contain three concealed triplets.
        2 han
        http://arcturus.su/wiki/Sanankou
        """
        huro_count = len(self.player.kabe)
        koutsus, _, jantou = separate_sets(self.agari_hand, huro_count)
        kantsus = [huro for huro in self.player.kabe
                   if huro.naki_type == Naki.ANKAN]
        ankou = len(koutsus) + len(kantsus)

        if ankou == 3 and self.agari_tile not in koutsus:
            self.total_yaku = 'sanankou'
            self.total_han = 2
            return True

        return False

    def sankantsu(self):  # 三槓子
        """This yaku requires kan to be called three times by one player.
        2 han
        http://arcturus.su/wiki/Sankantsu
        """
        kan = [Naki.DAMINKAN, Naki.CHAKAN, Naki.ANKAN]
        kantsus = [huro for huro in self.player.kabe if huro.naki_type in kan]
        if len(kantsus) == 3:
            self.total_yaku = 'sankantsu'
            self.total_han = 2
            return True

        return False


class Sanshoku(TeYaku):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_all_evals(self) -> List[Callable]:
        return [
            self.sanshoku_doukou,
            self.sanshoku_doujun,
        ]

    def sanshoku_doukou(self):  # 三色同刻
        """A hand contain three koutsu of the same numbered tiles across
        the three main suits.
        2 han
        http://arcturus.su/wiki/Sanshoku_doukou
        """
        huro_count = len(self.player.kabe)
        koutsu, _, _ = separate_sets(self.agari_hand, huro_count)
        for huro in self.player.kabe:
            if huro.naki_type == Naki.PON:
                koutsu.append(huro.tiles[0])

        counter = {1: [], 2: [], 3: []}
        for tile in koutsu:
            if tile.suit > 0:
                counter[tile.suit].append(tile.rank)

        for man_rank in counter[1]:
            for sou_rank in counter[2]:
                for pin_rank in counter[3]:
                    if man_rank == sou_rank == pin_rank:
                        self.total_yaku = 'sanshoku_doukou'
                        self.total_han = 2
                        return True
        return False

    def sanshoku_doujun(self):  # 三色同順
        """A hand contain sequences of the same numbered tiles across the
        three numbered suits.
        2 han
        1 han (open)
        http://arcturus.su/wiki/Sanshoku_doujun
        """
        huro_count = len(self.player.kabe)
        _, shuntsu, _ = separate_sets(self.agari_hand, huro_count)
        for huro in self.player.kabe:
            if huro.naki_type == Naki.CHII:
                shuntsu.append(huro.tiles)

        counter = {1: [], 2: [], 3: []}
        for tile_list in shuntsu:
            suit = tile_list[0].suit
            shuntsu_rank_tuple = tuple(
                sorted([tile.rank for tile in tile_list])
            )
            counter[suit].append(shuntsu_rank_tuple)

        for man_rank_tuple in counter[1]:
            for sou_rank_tuple in counter[2]:
                for pin_rank_tuple in counter[3]:
                    if man_rank_tuple == sou_rank_tuple == pin_rank_tuple:
                        self.total_yaku = 'sanshoku_doujun'
                        if self.player.menzenchin:
                            self.total_han = 2
                        else:
                            self.total_han = 1
                        return True
        return False


class Somete(TeYaku):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_all_evals(self) -> List[Callable]:
        return [
            self.chiniisou,
            self.honiisou,
        ]

    def chiniisou(self):  # 清一色
        """A hand is composed of tiles in one suit only.
        6 han
        5 han (open)
        http://arcturus.su/wiki/Chiniisou
        """
        suit_in_hand = set([Tile.suit_from_idx(k)
                            for k in self.agari_hand.keys()])
        suit_in_huro = set([tile.suit for tile in self.huro_tiles])
        suit = suit_in_hand | suit_in_huro

        if len(suit) == 1 and list(suit)[0] != 0:
            self.total_yaku = 'chiniisou'
            if self.player.menzenchin:
                self.total_han = 6
            else:
                self.total_han = 5
            return True
        return False

    def honiisou(self):  # 混一色
        """A hand composed only of honour tiles and tiles of a single suit.
        3 han
        2 han (open)
        http://arcturus.su/wiki/Honiisou
        """
        suit_not_jihai_in_hand = set(
            [Tile.suit_from_idx(k) for k in self.agari_hand.keys()
             if Tile.suit_from_idx(k) != 0])
        suit_not_jihai_in_huro = set(
            [tile.suit for tile in self.huro_tiles if tile.suit != 0])
        suit_not_jihai = suit_not_jihai_in_hand | suit_not_jihai_in_huro
        if len(suit_not_jihai) == 1:
            self.total_yaku = 'honiisou'
            if self.player.menzenchin:
                self.total_han = 3
            else:
                self.total_han = 2
            return True
        return False
