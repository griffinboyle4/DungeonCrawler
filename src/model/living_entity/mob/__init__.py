import itertools

from model import Fist
from model.direction import Direction
from model.living_entity import LivingEntity
from model.position import Position


class Mob(LivingEntity):
    mob_id = itertools.count(6, 2)

    def __init__(self, symbol, health, position, facing, weapon):
        super().__init__(symbol, health, position, facing, weapon)
        self._mob_id = next(Mob.mob_id)

    def get_mob_id(self):
        return self._mob_id

    def turn_to_face(self, pos: Position):
        diff = pos - self.get_position()

        if diff.get_x() == -1:
            self.set_direction(Direction.LEFT)
        elif diff.get_x() == 1:
            self.set_direction(Direction.RIGHT)
        elif diff.get_y() == 1:
            self.set_direction(Direction.DOWN)
        elif diff.get_y() == -1:
            self.set_direction(Direction.UP)

    def __str__(self):
        return "Mob(" + str(self.get_position()) + ", " + self.get_health() + ")"


class Rat(Mob):
    def __init__(self, position, facing=Direction.LEFT):
        super().__init__(symbol='@', health=4, position=position, facing=facing, weapon=Fist())

