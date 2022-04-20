from model.position import Position


class Option:
    def __init__(self, name: str, left_position: Position, right_position: Position):
        self._left_position = left_position
        self._right_position = right_position
        self._name = name

    def select(self):
        return self._left_position, self._right_position

    def choose(self):
        return self._name
