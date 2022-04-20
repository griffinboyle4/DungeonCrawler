from model.position import Position


class Room:
    """This class represents a room in Dungeon Crawler"""
    def __init__(self, position: Position, width, height):
        """Constructs a new Room with the given position, width, and height.
        :param position: the position of the Room
        :param width: the width of the Room
        :param height: the height of the Room
        """
        self._position = position
        self._width = width
        self._height = height

    def __eq__(self, other):
        """Checks if this Room is equivalent to the given Room. Room equivalence
        is determined by position equivalence alone.
        :param other: the Room to compare with this Room for equality
        :return: True if this Room is equal to the given Room
        """
        if isinstance(other, Room):
            return self._position == other.get_position()
        return False

    def __lt__(self, other):
        """Determines whether this Room is closer to the origin than the given Room.
        :param other: the Room to compare to this Room
        :return: True if this Room is closer to the origin than the given Room, else False
        """
        if isinstance(other, Room):
            return self._position < other.get_position()
        else:
            raise TypeError("Cannot compare type Room to type " + str(type(other)))

    def get_x(self):
        """Retrieves the Room's x-position.
        :return: the Room's x-position
        """
        return self._position.get_x()

    def get_y(self):
        """Retrieves the Room's y-position.
        :return: the Room's y-position
        """
        return self._position.get_y()

    def get_position(self):
        """Returns the Room's position.
        :return: the Room's position
        """
        return self._position

    def get_width(self):
        """Returns the Room's width.
        :return: the Room's width
        """
        return self._width

    def get_height(self):
        """Returns the Room's height.
        :return: the Room's height
        """
        return self._height

    def overlaps(self, rooms: list):
        """Checks if the Room overlaps any other Rooms in rooms.
        :param rooms: the list of other rooms
        :return: True if the Room overlaps, else False
        """
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

    def lies_within(self, top_left_corner: Position, bottom_right_corner: Position):
        """Checks whether the Room lies entirely with the given boundaries.
        :param top_left_corner: the position of the top left corner of the boundary
        :param bottom_right_corner: the position of the bottom right corner of the boundary
        :return: True if Room lies entirely within the given boundaries, else False
        """
        x_min = self.get_x()
        x_max = self.get_x() + self._width
        y_min = self.get_y()
        y_max = self.get_y() + self._height

        return x_min > top_left_corner.get_x() and x_max < bottom_right_corner.get_x() and y_min > top_left_corner.get_y() and y_max < bottom_right_corner.get_y()

    def get_center_position(self):
        """Returns the position at the center of the Room.
        :return: the position at the center of the Room
        """
        return self._position + Position(self._width // 2, self._height // 2)

    def get_path_indices_to(self, other):
        """Returns a list of 2-D indices tracing a path from this Room to the given Room.
        :param other: the Room to find a path to from this Room
        :return: a list of 2-D indices tracing a path from this Room to the given Room
        """
        source = self.get_center_position()
        destination = other.get_center_position()
        path = []
        if source.get_y() != destination.get_y():
            if source.get_y() < destination.get_y():
                path.extend([(source.get_x(), y) for y in range(source.get_y(), destination.get_y())])
                path.extend([(source.get_x() - 1, y) for y in range(source.get_y(), destination.get_y())])
            else:
                path.extend([(destination.get_x(), y) for y in range(destination.get_y(), source.get_y())])
                path.extend([(destination.get_x() - 1, y) for y in range(destination.get_y(), source.get_y())])

        if source.get_x() != destination.get_x():
            y = None
            if path:
                y = path[-1][1]
            if source.get_x() < destination.get_x():
                if y is None:
                    y = source.get_y()
                path.extend([(x, y) for x in range(source.get_x(), destination.get_x())])
                path.extend([(x, y - 1) for x in range(source.get_x(), destination.get_x())])
            else:
                if y is None:
                    y = destination.get_y()
                path.extend([(x, y) for x in range(destination.get_x(), source.get_x())])
                path.extend([(x, y - 1) for x in range(destination.get_x(), source.get_x())])

        return path
