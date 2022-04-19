from model.living_entity.weapon.fist import Fist
from model.direction import Direction
from model.level_generator import generate_level


class Model:
    def __init__(self, level=0, game_grid=generate_level()):
        self._level = level
        self._gameGrid = game_grid

    def get_columns(self):
        return self._gameGrid.get_columns()

    def get_rows(self):
        return self._gameGrid.get_rows()

    def get_position(self):
        return self._gameGrid.get_position()

    def get_x(self):
        return self._gameGrid.get_x()

    def get_y(self):
        return self._gameGrid.get_x()

    def move_left(self):
        self._gameGrid.move_left(self._gameGrid.get_player())

    def move_right(self):
        self._gameGrid.move_right(self._gameGrid.get_player())

    def move_up(self):
        self._gameGrid.move_up(self._gameGrid.get_player())

    def move_down(self):
        self._gameGrid.move_down(self._gameGrid.get_player())

    def data_grid_to_ascii(self):
        return self._gameGrid.data_grid_to_ascii()

    def player_attack(self):
        self._gameGrid.player_attack()

    def is_game_over(self):
        return self.get_player_health()[0] <= 0

    def update_mobs(self):
        return self._gameGrid.update_mobs()

    def get_player_health(self):
        return self._gameGrid.get_player_health()

    def get_current_enemy_health(self):
        return self._gameGrid.get_current_enemy_health()

    def get_current_enemy_symbol(self):
        return self._gameGrid.get_current_enemy_symbol()
