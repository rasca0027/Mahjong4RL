import itertools
import random

suits_dict = {0: 'Jihai', 1: 'Manzu', 2: 'Souzu', 3: 'Pinzu'}
jihai_dict = {0: 'Haku', 1: 'Hatsu', 2: 'Chun', 3: 'Ton', 4: 'Nan', 5: 'Shaa', 6: 'Pei'}


class Tile:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.is_dora = False
        
    def __str__(self):
        if self._suit == 0:
            return f"Tile of { jihai_dict[self._rank] }"
        else:
            return f"Tile of { self._rank } { suits_dict[self._suit] }"
    
    @property
    def suit(self):
        return self._suit
        
    @suit.setter
    def suit(self, value):
        if not 0 <= value < 4:
            raise ValueError(f"Suit should be in: { suits_dict }")
        self._suit = value
        
    @property
    def rank(self):
        return self._rank
        
    @rank.setter
    def rank(self, value):
        if self._suit == 0: # Jihai
            if not 0 <= value < 7:
                raise ValueError(f"Value for Jihai should be in: { jihai_dict }")
        else:
            if not 1 <= value < 10:
                raise ValueError(f"Value for { suits_dict[self._suit] } should be in: 1-9")
        self._rank = value


class Stack:
    def __init__(self):
        self.stack = []
        self.initiate()
        self.playling_wall = iter(self.stack[:122])
        self.dead_wall = iter(self.stack[-14:]) # 嶺上牌
        self.set_dora()
        
    def initiate(self):
        for suit in range(0, 4):
            max_rank = 7 if suit == 0 else 10 # Jihai only have 7 values
            for rank in range(1, max_rank):
                for _ in itertools.repeat(None, 4):
                    self.stack.append(Tile(suit, rank))
                    
        random.shuffle(self.stack)

    def set_dora(self):
        dora_indicator = self.stack[-5]
        dora_suit = dora_indicator.suit
        if dora_indicator.suit != 0:
            dora_rank = dora_indicator.rank + 1
        elif dora_indicator.rank >= 0 and dora_indicator <= 2:
            dora_rank = (dora_indicator.rank + 1) % 3
        else:
            dora_rank = dora_indicator.rank + 1
            if dora_rank >= 6: dora_rank = 3
        for tile in self.stack:
            if tile.suit == dora_suit and tile.rank == dora_rank:
                tile.is_dora = True

