from player import positions, Player

class Turn:
    """ A portion of the kyoku, starting from one player discarding tile and ends with the next palyer selecting tile to discard.
    From dealer's initial discard onward, each player gets a turn to draw a tile from the wall,
    all players, except the discarder, has the option of claiming a discarded tile by chii, pon, kan, or ron.
    If no claims of the discard are made, then the next player draws from the wall and makes a discard, 
    unless the hand is a winning hand with the declaration of tsumo. 
    see flowchart in README
    """

   pass


class Kyoku:
    """A portion of the game, starting from the dealing of tiles and ends with the declaration of a win, aborted hand, or draw. 
    """
    def __init__(self):
        self.winner = None
        # set four players
        self.players = []
        for player in range(4):
            player = Player('', positions[i]) 
            self.players.append(player)
        # initiate tile stack
        self.tile_stack = Stack()
        # deal tiles to each player to produce their starting hands
        # 要計算骰子嗎？
        pass

    # The game begins with the dealer's initial discard.    
    # while self.winner, repeat Turn
