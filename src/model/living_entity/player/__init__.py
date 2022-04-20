from model.direction import Direction
from model.living_entity import LivingEntity
from model.living_entity.weapon.fist import Fist
from model.position import Position

INITIAL_HEALTH = 10


class Player(LivingEntity):
    """This class represents a Player in Dungeon Crawler"""
    def __init__(self, symbol='&',
                 health=INITIAL_HEALTH,
                 position=Position(0, 0),
                 facing=Direction.LEFT,
                 weapon=Fist()):
        """Constructs a Player with the given symbol, health,
        position, facing direction, and weapon. If symbol is
        not specified, the defualt symbol is '&'. If health is
        is not specified, the default health is given by the the
        constant INITIAL_HEALTH. If facing is not specified, the
        defualt direction is LEFT. If weapon is not specified,
        the default weapon is a first.
        :param symbol: the string representation of the player
        :param health: the initial health of the player
        :param position: the initial position of the player
        :param facing: the initial facing direction of the player
        :param weapon: the weapon wielded by the player
        """
        super().__init__(symbol, health, position, facing, weapon)

