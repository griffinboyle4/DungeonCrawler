import itertools

from model.direction import Direction


class Weapon:
    mob_id = itertools.count(7, 2)

    def __init__(self, attack: int,
                 left_symbol: str,
                 right_symbol: str,
                 up_symbol: str,
                 down_symbol: str,
                 attack_rate=0.5):
        self._attack = attack
        self._attack_rate = attack_rate
        self._symbol = {Direction.LEFT: left_symbol,
                        Direction.UP: up_symbol,
                        Direction.RIGHT: right_symbol,
                        Direction.DOWN: down_symbol}
        self._weapon_id = next(Weapon.mob_id)

    def get_attack(self):
        return self._attack

    def get_attack_rate(self):
        return self._attack_rate

    def to_string(self, facing: Direction):
        return self._symbol.get(facing)
