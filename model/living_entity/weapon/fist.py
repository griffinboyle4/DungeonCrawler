from model.living_entity.weapon import Weapon


class Fist(Weapon):
    def __init__(self):
        super().__init__(1, "<", ">", "^", "v")
