from model.living_entity.weapon import Weapon


class Sword(Weapon):
    def __init__(self):
        super().__init__(2, "-", "-", "|", "|")
