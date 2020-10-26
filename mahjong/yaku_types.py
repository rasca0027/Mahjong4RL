import copy
from collections import defaultdict
from abc import ABC, abstractmethod

from .player import Player
from .utils import isYaochuu
from .components import Suit, Jihai, Tile


class YakuTypes(ABC):
    _total_yaku = []
    _total_han = 0
    _yakuman_count = 0
    _player = None
    _bakaze = None

    def __init__(self, player: Player, bakaze):
        self.player = player
        self.bakaze = bakaze
        self.agari_hand = copy.deepcopy(self.player.hand)
        self.agari_hand = defaultdict(
            int, {k: v for k, v in self.agari_hand.items() if v > 0})
        self.agari_hand[self.player.agari_tile.index] += 1
        self.huro_tiles = [
            tile for huro in self.player.kabe for tile in huro.tiles]

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

    @property
    def player(self):
        return self._player

    @player.setter
    def player(self, player: Player):
        self._player = player

    @property
    def bakaze(self):
        return self._bakaze

    @bakaze.setter
    def bakaze(self, bakaze):
        self._bakaze = bakaze

    @property
    def yakuman_count(self):
        return self._yakuman_count

    @yakuman_count.setter
    def yakuman_count(self, yakuman_count):
        self._yakuman_count += yakuman_count


class JouKyouYaku(YakuTypes):
    @property
    def total_yaku(self):
        return self._total_yaku

    @total_yaku.setter
    def total_yaku(self, yaku):
        self._total_yaku = yaku

    def menzen_tsumo(self):  # 門前清自摸和
        """A player with a closed tenpai hand may win with tsumo.
        1 han (closed only)
        http://arcturus.su/wiki/Menzenchin_tsumohou
        """
        return NotImplemented

    def chankan(self):  # 搶槓
        """A player may declare ron while a player calls to upgrade
        a minkou (pon) to a kan.
        1 han
        http://arcturus.su/wiki/Chankan
        """
        return NotImplemented

    def houtei_raoyui(self):  # 河底撈魚
        """A player wins with the tsumo on the haiteihai, the last
        drawable tile from the live wall.
        1 han
        http://arcturus.su/wiki/Haitei_raoyue_and_houtei_raoyui
        """
        return NotImplemented

    def riichi(self):  # 立直
        """When a player has a closed tenpai hand, the player may declare riichi.
        1 han (closed only)
        http://arcturus.su/wiki/Riichi
        """
        return NotImplemented

    def ippatsu(self):  # 一発
        """Winning on or before the next tile draw after riichi.
        1 han
        http://arcturus.su/wiki/Ippatsu
        """
        return NotImplemented

    def haitei_raoyue(self):  # 海底撈月
        """Win by last discard.
        1 han
        http://arcturus.su/wiki/Haitei_raoyue_and_houtei_raoyui
        """
        return NotImplemented

    def rinshan_kaihou(self):  # 嶺上開花
        """A player wins with the rinshanpai.
        1 han
        http://arcturus.su/wiki/Rinshan_kaihou
        """
        return NotImplemented

    def aburu_riichi(self):  # 両立直
        """This is a special case for riichi. In this case, the player's start
        hand is already at tenpai from the dealt tiles, or the initial draw
        produces a tenpai hand.
        2 han
        http://arcturus.su/wiki/Daburu_riichi
        """
        return NotImplemented

    def tenhou(self):  # 天和
        """The dealer hand is a winning hand even before discarding a tile.
        yakuman
        http://arcturus.su/wiki/Tenhou
        """
        return NotImplemented

    def chiihou(self):  # 地和
        """The non-dealer hand is a winning hand with the first tile draw.
        yakuman
        http://arcturus.su/wiki/Chiihou
        """
        return NotImplemented

    def nagashi_mangan(self):  # 流し満貫
        """All the discards are terminals and/or honors.
        In addition, none of these discards were called by other players.
        yakuman
        http://arcturus.su/wiki/Nagashi_mangan
        """
        return NotImplemented


class TeYaku(YakuTypes):
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
        self._total_han += han

    def ryuuiisou(self):  # 緑一色
        """A hand composed entirely of green tiles: 2, 3, 4, 6 and 8 Sou and/or Hatsu.
        yakuman
        http://arcturus.su/wiki/Ryuuiisou
        """
        return NotImplemented

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
            if pair_yaochuu_keys[0] == self.player.agari_tile.index:
                # 13-way wait
                self.total_yaku = 'kokushi musou 13-way wait'
                self.yakuman_count = 2
            else:  # single wait
                self.total_yaku = 'kokushi musou'
                self.yakuman_count = 1
            return True

        return False

    def chuuren_poutou(self):  # 九連宝燈 or 純正九蓮宝燈
        """A hand consisting of the tiles 1112345678999 in the same suit plus
        any one extra tile of the same suit.
        yakuman
        http://arcturus.su/wiki/Chuuren_poutou
        """
        return NotImplemented

    def toitoihou(self):  # 対々和
        """All triplets.
        2 han
        http://arcturus.su/wiki/Toitoihou
        """
        return NotImplemented

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
        return NotImplemented

    def pinfu(self):  # 平和
        """Defined by having 0 fu aside from the base 20 fu, or 30 fu in
        the case of a closed ron.
        1 han (closed only)
        http://arcturus.su/wiki/Pinfu
        """
        return NotImplemented

    def tanyao(self):  # 断么九
        """A hand contain only numbered tiles 2-8 from any of the three main suits.
        1 han
        http://arcturus.su/wiki/Honroutou
        """
        # check player's hand
        for k in self.agari_hand.keys():
            suit = k // 10
            rank = k % 10
            if isYaochuu(suit=suit, rank=rank):
                return False

        # check player's kabe
        for tile in self.huro_tiles:
            if isYaochuu(suit=tile.suit, rank=tile.rank):
                return False

        self.total_yaku = 'tanyao'
        self.total_han = 1
        return True


class Yakuhai(TeYaku):
    def daisangen(self):  # 大三元
        """This hand possesses three groups (triplets or quads) of all the dragons.
        yakuman
        http://arcturus.su/wiki/Daisangen
        """
        for rank in [Jihai.HAKU, Jihai.HATSU, Jihai.CHUN]:
            tile = Tile(Suit.JIHAI, rank.value)
            index = tile.index
            if self.agari_hand[index] >= 3:
                continue
            elif tile in self.huro_tiles:
                continue
            else:
                return False
        self.total_yaku = "daisangen"
        self.yakuman_count = 1
        return True

    def tsuuiisou(self):  # 字一色
        """Every group of tiles are composed of honor tiles.
        yakuman
        http://arcturus.su/wiki/Tsuuiisou
        """
        suit_in_hand = set([k // 10 for k in self.agari_hand.keys()])
        suit_in_huro = set([tile.suit for tile in self.huro_tiles])
        suit = suit_in_hand | suit_in_huro

        if len(suit) == 1 and list(suit)[0] == 0:
            self.total_yaku = 'tsuuiisou'
            self.yakuman_count = 1
            return True
        return False

    def daisuushii(self):  # 大四喜
        """This hand has four groups (triplets or quads) of
        all four wind tiles.
        yakuman
        http://arcturus.su/wiki/Daisuushii
        """
        four_winds = [Jihai.TON, Jihai.NAN, Jihai.SHAA, Jihai.PEI]
        for rank in four_winds:
            tile = Tile(Suit.JIHAI, rank.value)
            index = tile.index
            if self.agari_hand[index] >= 3:
                continue
            elif tile in self.huro_tiles:
                continue
            else:
                return False
        self.total_yaku = "daisuushii"
        self.yakuman_count = 1
        return True

    def shousuushii(self):  # 小四喜
        """This hand has three groups (triplets or quads)
        of the wind tiles plus a pair of the fourth kind.
        yakuman
        http://arcturus.su/wiki/Shousuushii
        """
        return NotImplemented

    def shousangen(self):  # 小三元
        """The hand is composed of two koutsu (triplet) and a jantou (pair)
        of the three sangenpai (三元牌)
        2 han (the hand will almost always score at least mangan,
        see the link below)
        http://arcturus.su/wiki/Shousangen
        """
        return NotImplemented

    def yakuhai(self):  # 役牌
        """A group of 1 han yaku scored for completing a group of certain
        honour tiles:
        1. sangenpai (三元牌)
        2. bakaze (場風)
        3. jikaze (自風)
        1 han per counted triplet
        http://arcturus.su/wiki/Yakuhai
        """
        return NotImplemented


class Peikou(TeYaku):
    def ryanpeikou(self):  # 二盃口
        """A hand consisting of two "iipeikou"
        3 han (closed only)
        http://arcturus.su/wiki/Ryanpeikou
        """
        return NotImplemented

    def iipeikou(self):  # 一盃口
        """A hand contain two identical sequences.
        1 han (closed only)
        http://arcturus.su/wiki/Iipeikou
        """
        return NotImplemented


class Chanta(TeYaku):
    def chinroutou(self):  # 清老頭
        """Every group of tiles are composed of terminal tiles.
        yakuman
        http://arcturus.su/wiki/Chinroutou
        """
        return NotImplemented

    def honroutou(self):  # 混老頭
        """A hand contain only honors and terminals.
        2 han (It is impossible to score this yaku without at least either
        toitoi or chiitoitsu. So, this yaku is actually at minimum, the
        equivalent of 4 han)
        http://arcturus.su/wiki/Honroutou
        """
        return NotImplemented

    def junchantaiyaochuu(self):  # 純全帯么九
        """Every tile group and the pair must contain at least one terminal.
        3 han
        2 han (open)
        http://arcturus.su/wiki/Junchantaiyaochuu
        """
        return NotImplemented

    def chanta(self):  # 混全帯么九
        """Every tile group and the pair must contain at least one terminal or
        honor tile.
        2 han
        1 han (open)
        http://arcturus.su/wiki/Chanta
        """
        return NotImplemented


class Koutsu(TeYaku):
    def suuankou(self):  # 四暗刻 or 四暗刻単騎
        """This hand is composed of four groups of closed triplets.
        When this hand has a shanpon pattern and the win is via ron,
        then it would not be counted as such;
        only as the lesser toitoi with sanankou.
        yakuman
        http://arcturus.su/wiki/Suuankou
        """
        return NotImplemented

    def suukantsu(self):  # 四槓子
        """Any hand with four calls of kan.
        yakuman
        http://arcturus.su/wiki/Suukantsu
        """
        return NotImplemented

    def sanankou(self):  # 三暗刻
        """A hand contain three concealed triplets.
        2 han
        http://arcturus.su/wiki/Sanankou
        """
        return NotImplemented

    def sankantsu(self):  # 三槓子
        """This yaku requires kan to be called three times by one player.
        2 han
        http://arcturus.su/wiki/Sankantsu
        """
        return NotImplemented


class Sanshoku(TeYaku):
    def sanshoku_doukou(self):  # 三色同刻
        """A hand contain three koutsu of the same numbered tiles across
        the three main suits.
        2 han
        http://arcturus.su/wiki/Sanshoku_doukou
        """
        return NotImplemented

    def sanshoku_doujun(self):  # 三色同順
        """A hand contain sequences of the same numbered tiles across the
        three numbered suits.
        2 han
        1 han (open)
        http://arcturus.su/wiki/Sanshoku_doujun
        """
        return NotImplemented


class Somete(TeYaku):
    def chiniisou(self):  # 清一色
        """A hand is composed of tiles in one suit only.
        6 han
        5 han (open)
        http://arcturus.su/wiki/Sanankou
        """
        suit_in_hand = set([k // 10 for k in self.agari_hand.keys()])
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
            [k // 10 for k in self.agari_hand.keys() if k // 10 != 0])
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
