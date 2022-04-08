from sty import fg

from model.game_grid import GameGrid
from model.player import Player


class Model:
    def __init__(self, level=0, game_grid=GameGrid(), x_pos=0, y_pos=0, player=Player()):
        self._level = level
        self._gameGrid = game_grid
        if x_pos >= 0 or x_pos < self._gameGrid.get_columns():
            self._x_pos = x_pos
        else:
            raise ValueError("Invalid x Position: must be on interval [0, columns)")
        if y_pos >= 0 or y_pos < self._gameGrid.get_rows():
            self._y_pos = y_pos
        else:
            raise ValueError("Invalid y Position: must be on interval [0, rows)")
        self._player = player

    def get_position(self) -> (int, int):
        return self._x_pos, self._y_pos

    def get_position_x(self):
        return self._x_pos

    def get_position_y(self):
        return self._y_pos

    def left_possible(self):
        return self._x_pos != 0

    def up_possible(self):
        return self._y_pos != 0

    def right_possible(self):
        return self._x_pos != self._gameGrid.get_columns() - 1

    def down_possible(self):
        return self._y_pos != self._gameGrid.get_rows() - 1

    def move_left(self):
        if self.left_possible():
            self._x_pos -= 1
        else:
            raise NotImplementedError("Cannot move left: position is currently along left border")

    def move_right(self):
        if self.right_possible():
            self._x_pos += 1
        else:
            raise NotImplementedError("Cannot move right: position is currently along right border")

    def move_up(self):
        if self.up_possible():
            self._y_pos -= 1
        else:
            raise NotImplementedError("Cannot move up: position is currently along top border")

    def move_down(self):
        if self.down_possible():
            self._y_pos += 1
        else:
            raise NotImplementedError("Cannot move down: position is currently along bottom border")

    def to_string(self):
        background = self._gameGrid.get_background()
        background[self._y_pos][self._x_pos] = self._player.to_string()

        return '\n'.join([''.join(row) for row in background])
