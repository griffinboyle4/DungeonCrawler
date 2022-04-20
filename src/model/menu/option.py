from model.position import Position


class Option:
    """This class represents a menu option."""
    def __init__(self, name: str, left_position: Position, right_position: Position):
        """Constructs a menu option with the given name, left position, and right position.
        :param name: the unique name of the option
        :param left_position: the position of the left cursor when selected
        :param right_position: the position of the right cursor when selected
        """
        self._left_position = left_position
        self._right_position = right_position
        self._name = name

    def select(self):
        """Returns the left and right cursor positions for the option.
        :return: the left and right cursor positions for the option
        """
        return self._left_position, self._right_position

    def choose(self):
        """Returns the name of the option.
        :return: the name of the option
        """
        return self._name
