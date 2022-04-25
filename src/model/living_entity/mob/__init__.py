import itertools

from abc import ABC

from model import Fist
from model.direction import Direction
from model.living_entity import LivingEntity
from model.position import Position


class Mob(LivingEntity, ABC):
    """This abstract class represents a Mob in Dungeon Crawler"""
    mob_id = itertools.count(6, 2)

    def __init__(self, symbol, health, position, facing, weapon):
        """Constructs a Mob with the given symbol, health,
        position, facing direction, and weapon. If symbol is
        not specified, the default symbol is '&'. If health is
        is not specified, the default health is given by the the
        constant INITIAL_HEALTH. If facing is not specified, the
        default direction is LEFT. If weapon is not specified,
        the default weapon is a first.
        :param symbol: the string representation of the Mob
        :param health: the initial health of the Mob
        :param position: the initial position of the Mob
        :param facing: the initial facing direction of the Mob
        :param weapon: the weapon wielded by the Mob
        """
        super().__init__(symbol, health, position, facing, weapon)
        self._mob_id = next(Mob.mob_id)

    def get_mob_id(self):
        """Returns the mob's mob id.
        :return: the mob's mob id
        """
        return self._mob_id

    def turn_to_face(self, pos: Position):
        """Rotates mob to face the given position.
        :param pos: the position to face
        :return: None
        """
        diff = pos - self.get_position()

        if diff.get_x() == -1:
            self.set_direction(Direction.LEFT)
        elif diff.get_x() == 1:
            self.set_direction(Direction.RIGHT)
        elif diff.get_y() == 1:
            self.set_direction(Direction.DOWN)
        elif diff.get_y() == -1:
            self.set_direction(Direction.UP)


class Rat(Mob):
    """This class represents a Rat Mob in Dungeon Crawler"""
    def __init__(self, position, facing=Direction.LEFT):
        """Constructs a Rat with the given position and facing direction.
        If facing is not specified, the default direction is left.
        :param position: the initial position of the Rat
        :param facing: the initial facing direction of the Rat
        """
        super().__init__(symbol='@', health=4, position=position, facing=facing, weapon=Fist())
