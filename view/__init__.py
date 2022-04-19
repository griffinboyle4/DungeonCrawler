import os

from model import Model


class View:
    def __init__(self, model=Model()):
        self._model = model

    def display(self):
        os.system('clear')
        ascii_grid = self._model.data_grid_to_ascii()

        for row in ascii_grid:
            for col in row:
                print(col, end="")

            print("\n")

        hud = "Health: " + health_to_string(self._model.get_player_health())

        if self._model.get_current_enemy_symbol() is not None:
            hud += "\t" + self._model.get_current_enemy_symbol() + ": "
            hud += health_to_string(self._model.get_current_enemy_health())

        print(hud)


def health_to_string(health: tuple):
    result = str()
    result += "♥" * health[0]
    result += "♡" * (health[1] - health[0])
    return result
