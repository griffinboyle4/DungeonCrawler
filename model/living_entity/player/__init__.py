from model.direction import Direction
from model.living_entity import LivingEntity
from model.living_entity.weapon.fist import Fist
from model.position import Position

INITIAL_HEALTH = 10


class Player(LivingEntity):
    def __init__(self, symbol='&',
                 health=INITIAL_HEALTH,
                 position=Position(0, 0),
                 facing=Direction.LEFT,
                 weapon=Fist()):
        super().__init__(symbol, health, position, facing, weapon)


