import threading
from abc import ABC

from model.direction import Direction
from model.position import Position


class LivingEntity(ABC):
    """This abstract class represents a living entity in Dungeon Crawler"""
    def __init__(self, symbol, health, position, facing, weapon):
        """Constructs a Living Entity with the given symbol, health, position, facing direction, and weapon.
        :param symbol: a string representing the entity
        :param health: the initial health of the entity
        :param position: the initial position of the entity
        :param facing: the initial direction the entity
        :param weapon: the weapon wielded by the entity
        """
        self._health = health
        self._symbol = symbol
        self._position = position
        self._facing = facing
        self._weapon = weapon
        self._attacking = False
        self._max_health = health

    def get_position(self):
        """Retrieves the current position of the entity.
        :return: the current position of the entity
        """
        return self._position

    def get_x(self):
        """Retrieves the entity's current x-position.
        :return: the entity's current x-position
        """
        return self._position.get_x()

    def get_y(self):
        """Retrieves the entity's current y-position.
        :return: the entity's current y-position
        """
        return self._position.get_y()

    def get_direction(self):
        """Retrieves the entity's current facing direction.
        :return: the entity's current facing direction
        """
        return self._facing

    def set_position(self, position: Position):
        """Sets the entity's position to the given position
        :param position: the new position to assign
        :return: None
        """
        self._position = position

    def set_direction(self, new_direction: Direction):
        """Sets the entity's position to the given position
        :param new_direction: the new position to assign
        :return: None
        """
        self._facing = new_direction

    def move_left(self):
        """Moves the entity to the left by 1.
        :return: None
        """
        self._position.move_left()

    def move_right(self):
        """Moves the entity to the right by 1.
        :return: None
        """
        self._position.move_right()

    def move_up(self):
        """Moves the entity up by 1.
        :return: None
        """
        self._position.move_up()

    def move_down(self):
        """Moves the entity down by 1.
        :return: None
        """
        self._position.move_down()

    def set_symbol(self, symbol):
        """Sets the string representation of the entity to the given symbol.
        :param symbol: the new symbol to assign
        :return: None
        """
        self._symbol = symbol

    def get_symbol(self):
        """Retrieves the string representation of the entity.
        :return: the string representation of the entity
        """
        return self._symbol

    def get_health(self):
        """Retrieves the entity's health and max health, as a size-2 tuple.
        :return: the entity's health, the entity's max health
        """
        return self._health, self._max_health

    def take_damage(self, damage):
        """Imparts the given damage on the entity's health.
        :param damage: the amount of damage to deal
        :return: None
        """
        self._health -= damage

    def gain_health(self, health):
        """Adds the given health to the entity's health.
        :param health: the amount of health to gain
        :return: None
        """
        self._health += health

    def get_attack(self):
        """Returns the attack damage of the entity's weapon.
        :return: the attack damage of the entity's weapon
        """
        return self._weapon.get_attack()

    def get_weapon_symbol(self):
        """Retrieves the string representation of the entity's weapon.
        :return: the string representation of the entity's weapon
        """
        return self._weapon.get_symbol(self._facing)

    def get_weapon_position(self):
        """Returns the position of the entity's weapon, based on the
        current position and facing direction.
        :return: the position of the entity's weapon
        """
        if self._facing == Direction.LEFT:
            return self._position - Position(1, 0)
        elif self._facing == Direction.UP:
            return self._position - Position(0, 1)
        elif self._facing == Direction.RIGHT:
            return self._position + Position(1, 0)
        elif self._facing == Direction.DOWN:
            return self._position + Position(0, 1)

    def is_attacking(self):
        """Checks if the entity is currently attacking.
        :return: True if the entity is attacking, else False
        """
        return self._attacking

    def set_not_attacking(self):
        """Stops entity from attacking.
        :return: None
        """
        self._attacking = False

    def attack(self):
        """Makes the entity attack for the duration of its weapon attack rate,
        then stops attacking. Uses threading to make non-blocking.
        :return: None
        """
        self._attacking = True
        timer = threading.Timer(self._weapon.get_attack_rate(), self.set_not_attacking)
        timer.start()
