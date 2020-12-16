from .components import Naki, Action, Tile, Huro


class ActionLog:
    def __init__(
        self, p_pos: int,
        action: Action,
        action_tile: Tile = None,
        naki_type: Naki = None,
        huro: Huro = None,
    ):
        self.p_pos = p_pos
        self.action = action
        self.action_tile = action_tile
        self.naki_type = naki_type
        self.huro = huro
        return

    def __str__(self):
        str_ = f"Player {self.p_pos} {self.action.value}"
        if self.action == Action.RYUUKYOKU:
            return "Ryuukyoku"

        if self.action != Action.NAKI:
            if self.action_tile:
                return str_ + f" with {self.action_tile}"
            return str_

        if self.naki_type:
            str_ += f" {self.naki_type}"
            if self.action_tile:
                str_ += f" with {self.action_tile}"
            if self.huro:
                str_ += f" forms {self.huro}"
        return


class KyokuLogger:
    def __init__(self):
        self.logger = []

    def log(self, **kwargs):
        self.logger.append(ActionLog(kwargs))

    def __str__(self):
        return "\n".join(self.single_log.__str__)
