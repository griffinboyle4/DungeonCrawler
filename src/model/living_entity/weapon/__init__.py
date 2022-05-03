import itertools

from abc import ABC
from model.direction import Direction


class Weapon(ABC):
    """This abstract class represents a Weapon in Dungeon Crawler"""
    weapon_id = itertools.count(7, 2)

    def __init__(self, attack: int,
                 left_symbol: str,
                 right_symbol: str,
                 up_symbol: str,
                 down_symbol: str,
                 attack_rate=0.5):
        """Constructs a weapon with the given attack, orientation symbols, and attack_rate.
        If no attack_rate is specified, the attack rate is 0.5 by default.
        :param attack: the amount of damage dealt by the weapon
        :param left_symbol: the string representation of the left orientation of the weapon
        :param right_symbol: the string representation of the right orientation of the weapon
        :param up_symbol: the string representation of the up orientation of the weapon
        :param down_symbol: the string representation of down left orientation of the weapon
        :param attack_rate: the attack rate of the weapon
        """
        self._attack = attack
        self._attack_rate = attack_rate
        self._symbol = {Direction.LEFT: left_symbol,
                        Direction.UP: up_symbol,
                        Direction.RIGHT: right_symbol,
                        Direction.DOWN: down_symbol}
        self._weapon_id = next(Weapon.weapon_id)

    def get_attack(self):
        """Returns the amount of damage dealt by the weapon.
        :return: the amount of damage dealt by the weapon
        """
        return self._attack

    def get_attack_rate(self):
        """Returns the attack_rate of the weapon.
        :return: the attack_rate of the weapon
        """
        return self._attack_rate

    def get_symbol(self, facing: Direction):
        """Returns the orientation-specific string representation of the weapon.
        :param facing: the orientation of the weapon
        :return: the orientation-specific string representation of the weapon
        """
        return self._symbol.get(facing)

    def get_weapon_id(self):
        """Returns the weapon's weapon id.
        :return: the weapon's weapon id
        """
        return self._weapon_id
