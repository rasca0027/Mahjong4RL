
positions = {0: 'Ton', 1: 'Nan', 2: 'Shaa', 3: 'Pei'}


class Player:
    
    def __init__(self, name, seating_position):
        self.name = name
        self.seating_position = seating_position
        self.points = 25_000
        self.is_riichi = False
        
    def __str__(self):
        return f'Player: { self.name }, Seating Position: { positions[self.seating_position] }'

    @property
    def seating_position(self):
        return self._seating_position
        
    @seating_position.setter
    def seating_position(self, value):
        if not 0 <= value < 4:
            raise ValueError(f"Seating Position should be in: { positions }")
        self._seating_position = value
