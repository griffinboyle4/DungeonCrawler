from model.living_entity.weapon import Weapon


class Fist(Weapon):
    """This class represents a First in Dungeon Crawler"""
    def __init__(self):
        """Constructs a Fist"""
        super().__init__(1, "<", ">", "^", "v")
