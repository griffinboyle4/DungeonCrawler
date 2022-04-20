from math import sqrt


class Position:
    """Represents a position on 2-D Grid"""
    def __init__(self, x, y):
        """Constructs a Position with the given x and y coordinates.
        :param x: the x-coordinate of the position
        :param y: the y-coordinate of the position
        """
        self._x = x
        self._y = y

    def get_x(self):
        """Retrieves the x-component of the position.
        :return: the x-component of the position
        """
        return self._x

    def get_y(self):
        """Retrieves the x-component of the position.
        :return: the x-component of the position
        """
        return self._y

    def __add__(self, other):
        """Returns the sum of this position and the the given position,
        as the sum of their individual components.
        :param other: the position to sum with this position.
        :return: the sum of this position and the the given position
        """
        if isinstance(other, Position):
            return Position(self._x + other.get_x(), self._y + other.get_y())
        else:
            raise TypeError("Cannot add object of type " + str(type(other)) + " to object of type Position")

    def __sub__(self, other):
        """Returns the difference between this position and the the given position,
        as the difference between their individual components.
        :param other: the position to subtract from this position.
        :return: the difference between this position and the the given position
        """
        if isinstance(other, Position):
            return Position(self._x - other.get_x(), self._y - other.get_y())
        else:
            raise TypeError("Cannot subtract object of type " + str(type(other)) + " to object of type Position")

    def __eq__(self, other):
        """Checks if this position is equivalent to the given position.
        Equality is determined by the equality of the individual components.
        :param other: the position to compare to this position
        :return: True if equal, else False
        """
        if isinstance(other, Position):
            return self._x == other.get_x() and self._y == other.get_y()

        return False

    def __lt__(self, other):
        """Determines whether this position is
        closer to the origin than the given position.
        :param other: the position to compare to this position
        :return: True if this position is closer to the origin than the given position, else False
        """
        if isinstance(other, Position):
            return self.distance_from_origin() < other.distance_from_origin()
        else:
            raise TypeError("Cannot compare type Position to type " + str(type(other)))

    def __str__(self):
        """Returns the position as a readable string.
        :return: the position as a readable string
        """
        return "(" + str(self._x) + ", " + str(self._y) + ")"

    def move_left(self):
        """Moves the position to left by 1.
        :return: None
        """
        self._x -= 1

    def move_right(self):
        """Moves the position to the right by 1.
        :return: None
        """
        self._x += 1

    def move_up(self):
        """Moves the position up by 1.
        :return: None
        """
        self._y -= 1

    def move_down(self):
        """Moves the position down by 1.
        :return: None
        """
        self._y += 1

    def distance_to(self, other):
        """Returns the distance from this position to the given position.
        :param other: the position to which the distance is determined
        :return: the distance from this position to the given position
        """
        return sqrt(((other.get_x() - self._x) ** 2) + ((other.get_y() - self._y) ** 2))

    def distance_from_origin(self):
        """Returns the distance from the origin to this position.
        :return: the distance from the origin to this position
        """
        return self.distance_to(Position(0, 0))

    def __hash__(self):
        """Returns a unique hashcode for the position.
        :return: a unique hashcode for the position
        """
        return (self._x, self._y).__hash__()

