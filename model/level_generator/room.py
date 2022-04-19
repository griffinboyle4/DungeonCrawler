from model.position import Position


class Room:
    def __init__(self, position: Position, width, height):
        self._position = position
        self._width = width
        self._height = height

    def __eq__(self, other):
        if isinstance(other, Room):
            return self._position == other.get_position()
        return False

    def __lt__(self, other):
        if isinstance(other, Room):
            return self._position < other.get_position()
        else:
            raise TypeError("Cannot compare type Room to type " + str(type(other)))

    def get_x(self):
        return self._position.get_x()

    def get_y(self):
        return self._position.get_y()

    def get_position(self):
        return self._position

    def get_width(self):
        return self._width

    def get_height(self):
        return self._height

    def overlaps(self, rooms: list):
        for current_room in rooms:
            x_min_1 = self.get_x()
            x_max_1 = self.get_x() + self._width
            x_min_2 = current_room.get_x()
            x_max_2 = current_room.get_x() + current_room.get_width()
            y_min_1 = self.get_y()
            y_max_1 = self.get_y() + self._height
            y_min_2 = current_room.get_y()
            y_max_2 = current_room.get_y() + current_room.get_height()

            if (x_min_1 <= x_max_2 and x_max_1 >= x_min_2) and (y_min_1 <= y_max_2 and y_max_1 >= y_min_2):
                return True
        return False
