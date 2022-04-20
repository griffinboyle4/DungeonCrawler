from model.living_entity.weapon import Weapon


class Sword(Weapon):
    """This class represents a Sword in Dungeon Crawler"""
    def __init__(self):
        """Constructs a Sword"""
        super().__init__(2, "-", "-", "|", "|")
