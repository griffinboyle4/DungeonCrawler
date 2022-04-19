import threading
from abc import ABC

from model.direction import Direction
from model.position import Position


class LivingEntity(ABC):
    def __init__(self, symbol, health, position, facing, weapon):
        self._health = health
        self._symbol = symbol
        self._position = position
        self._facing = facing
        self._weapon = weapon
        self._attacking = False
        self._max_health = health

    def get_position(self):
        return self._position

    def get_x(self):
        return self._position.get_x()

    def get_y(self):
        return self._position.get_y()

    def get_direction(self):
        return self._facing

    def set_direction(self, new_direction: Direction):
        self._facing = new_direction

    def move_left(self):
        self._position.move_left()

    def move_right(self):
        self._position.move_right()

    def move_up(self):
        self._position.move_up()

    def move_down(self):
        self._position.move_down()

    def set_symbol(self, symbol):
        self._symbol = symbol

    def get_symbol(self):
        return self._symbol

    def get_health(self):
        return self._health, self._max_health

    def take_damage(self, damage):
        self._health -= damage

    def get_attack(self):
        return self._weapon.get_attack()

    def get_weapon_symbol(self):
        return self._weapon.to_string(self._facing)

    def get_weapon_position(self):
        if self._facing == Direction.LEFT:
            return self._position - Position(1, 0)
        elif self._facing == Direction.UP:
            return self._position - Position(0, 1)
        elif self._facing == Direction.RIGHT:
            return self._position + Position(1, 0)
        elif self._facing == Direction.DOWN:
            return self._position + Position(0, 1)

    def is_attacking(self):
        return self._attacking

    def set_not_attacking(self):
        self._attacking = False

    def attack(self):
        self._attacking = True
        timer = threading.Timer(self._weapon.get_attack_rate(), self.set_not_attacking)
        timer.start()
