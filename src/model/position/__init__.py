from math import sqrt

class Position:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def __add__(self, other):
        if isinstance(other, Position):
            return Position(self._x + other.get_x(), self._y + other.get_y())
        else:
            raise TypeError("Cannot add object of type " + str(type(other)) + " to object of type Position")

    def __sub__(self, other):
        if isinstance(other, Position):
            return Position(self._x - other.get_x(), self._y - other.get_y())
        else:
            raise TypeError("Cannot subtract object of type " + str(type(other)) + " to object of type Position")

    def __eq__(self, other):
        if isinstance(other, Position):
            return self._x == other.get_x() and self._y == other.get_y()

        return False

    def __lt__(self, other):
        if isinstance(other, Position):
            return self.distance_from_origin() < other.distance_from_origin()
        else:
            raise TypeError("Cannot compare type Position to type " + str(type(other)))

    def __str__(self):
        return "(" + str(self._x) + ", " + str(self._y) + ")"

    def move_left(self):
        self._x -= 1

    def move_right(self):
        self._x += 1

    def move_up(self):
        self._y -= 1

    def move_down(self):
        self._y += 1

    def distance_to(self, other):
        return sqrt(((other.get_x() - self._x) ** 2) + ((other.get_y() - self._y) ** 2))

    def distance_from_origin(self):
        return self.distance_to(Position(0, 0))

    def __hash__(self):
        return (self._x, self._y).__hash__()

