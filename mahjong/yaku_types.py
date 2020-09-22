# Yaku compatibility
# http://arcturus.su/wiki/Yaku_compatibility

# Discard based

def chankan():  # 搶槓
    """A player may declare ron while a player calls to upgrade
    a minkou (pon) to a kan.

    1 han
    http://arcturus.su/wiki/Chankan
    """
    ...


def houtei_raoyui():  # 河底撈魚
    """A player wins with the tsumo on the haiteihai, the last
    drawable tile from the live wall.

    1 han
    http://arcturus.su/wiki/Haitei_raoyue_and_houtei_raoyui
    """
    ...


# Discretionary

def riichi():  # 立直
    """When a player has a closed tenpai hand, the player may declare riichi.

    1 han (closed only)
    http://arcturus.su/wiki/Riichi
    """


def aburu_riichi():  # 両立直
    """This is a special case for riichi. In this case, the player's start
    hand is already at tenpai from the dealt tiles, or the initial draw
    produces a tenpai hand.

    2 han
    http://arcturus.su/wiki/Daburu_riichi
    """
    ...


# Riichi dependent

def ippatsu():  # 一発
    """Winning on or before the next tile draw after riichi.

    1 han
    http://arcturus.su/wiki/Ippatsu
    """
    ...


# Draw based

def haitei_raoyue():  # 海底撈月
    """Win by last discard.

    1 han
    http://arcturus.su/wiki/Haitei_raoyue_and_houtei_raoyui
    """
    ...


def menzen_tsumo():  # 門前清自摸和
    """A player with a closed tenpai hand may win with tsumo.

    1 han (closed only)
    http://arcturus.su/wiki/Menzenchin_tsumohou
    """
    ...


def rinshan_kaihou():  # 嶺上開花
    """A player wins with the rinshanpai.

    1 han
    http://arcturus.su/wiki/Rinshan_kaihou
    """
    ...


# Honor based

def honiisou():  # 混一色
    """A hand composed only of honour tiles and tiles of a single suit.

    3 han
    2 han (open)
    http://arcturus.su/wiki/Honiisou
    """
    ...


def honroutou():  # 混老頭
    """A hand contain only honors and terminals.

    2 han (It is impossible to score this yaku without at least either
    toitoi or chiitoitsu. So, this yaku is actually at minimum, the
    equivalent of 4 han)
    http://arcturus.su/wiki/Honroutou
    """
    ...


def shousangen():  # 小三元
    """The hand is composed of two koutsu (triplet) and a jantou (pair)
    of the three sangenpai (三元牌)

    2 han (the hand will almost always score at least mangan,
    see the link below)
    http://arcturus.su/wiki/Shousangen
    """
    ...


def tanyao():  # 断么九
    """A hand contain only numbered tiles 2-8 from any of the three main suits.

    1 han
    http://arcturus.su/wiki/Honroutou
    """
    ...


def yakuhai():  # 役牌
    """A group of 1 han yaku scored for completing a group of certain
    honour tiles:
    1. sangenpai (三元牌)
    2. bakaze (場風)
    3. jikaze (自風)

    1 han per counted triplet
    http://arcturus.su/wiki/Honroutou
    """
    ...


# Sequential

def iipeikou():  # 一盃口
    """A hand contain two identical sequences.

    1 han (closed only)
    http://arcturus.su/wiki/Iipeikou
    """
    ...


def ryanpeikou():  # 二盃口
    """A hand consisting of two "iipeikou"

    3 han (closed only)
    http://arcturus.su/wiki/Ryanpeikou
    """
    ...


def ikkitsuukan():  # 一気通貫
    """Three distinct tile groups containing 123, 456, 789 of one suit.

    2 han
    1 han (open)
    http://arcturus.su/wiki/Ikkitsuukan
    """
    ...


def pinfu():  # 平和
    """Defined by having 0 fu aside from the base 20 fu, or 30 fu in
    the case of a closed ron.

    1 han (closed only)
    http://arcturus.su/wiki/Pinfu
    """
    ...


def sanshoku_doujun():  # 三色同順
    """A hand contain sequences of the same numbered tiles across the
    three numbered suits.

    2 han
    1 han (open)
    http://arcturus.su/wiki/Sanshoku_doujun
    """
    ...


# Terminal based

def chanta():  # 混全帯么九
    """Every tile group and the pair must contain at least one terminal or
    honor tile.

    2 han
    1 han (open)
    http://arcturus.su/wiki/Chanta
    """
    ...


def junchantaiyaochuu():  # 純全帯么九
    """Every tile group and the pair must contain at least one terminal.

    3 han
    2 han (open)
    http://arcturus.su/wiki/Junchantaiyaochuu
    """
    ...


def nagashi_mangan():  # 流し満貫
    """
    http://arcturus.su/wiki/Nagashi_mangan
    """
    ...


# Triplet based

def sanankou():  # 三暗刻
    """A hand contain three concealed triplets.

    2 han
    http://arcturus.su/wiki/Sanankou
    """
    ...


def sankantsu():  # 三槓子
    """This yaku requires kan to be called three times by one player.

    2 han
    http://arcturus.su/wiki/Sankantsu
    """
    ...


def sanshoku_doukou():  # 三色同刻
    """A hand contain three koutsu of the same numbered tiles across
    the three main suits.

    2 han
    http://arcturus.su/wiki/Sanshoku_doukou
    """
    ...


def toitoihou():  # 対々和
    """All triplets.

    2 han
    http://arcturus.su/wiki/Toitoihou
    """
    ...


# Suit based

def chiniisou():  # 清一色
    """A hand is composed of tiles in one suit only.

    6 han
    5 han (open)
    http://arcturus.su/wiki/Sanankou
    """
    ...


# Yakuman

def yakuman():  # 役満
    """
    Tenhou (天和)
    Chiihou (地和)
    Kokushi musou (国士無双)
    Chuuren poutou (九連宝燈)
    Suukantsu (四槓子)
    Suuankou (四暗刻)
    Chinroutou (清老頭)
    Ryuuiisou (緑一色)
    Tsuuiisou (字一色)
    Suushiihou (四喜和)
    Daisangen (大三元)
    """
    ...
