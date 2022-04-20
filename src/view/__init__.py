import os

from model import Model, GameState


class View:
    def __init__(self, model):
        self._model = model

    def display(self):
        if self._model.get_game_state() == GameState.IN_GAME:
            if self._model.get_current_game_state().need_update():
                hud = "\n\tHealth: " + health_to_string(self._model.get_player_health()) + "\t"

                if self._model.get_current_enemy_symbol() is not None:
                    hud += self._model.get_current_enemy_symbol() + ": "
                    hud += health_to_string(self._model.get_current_enemy_health())
                else:
                    hud += "\t\t"

                hud += "\tLevel: " + str(self._model.get_current_level())

                os.system('clear')

                print("\n\n\t" + '\n\t'.join([''.join(row)
                                              for row
                                              in self._model.data_grid_to_ascii()]) + hud)
        elif self._model.get_game_state() != GameState.EXIT:
            if self._model.get_current_game_state().need_update():
                os.system('clear')

                print("\n\n\t" + '\n\t'.join([''.join(row)
                                              for row
                                              in self._model.get_current_game_state().get_full_background()]))


def health_to_string(health: tuple):
    result = str()
    result += "♥" * health[0]
    result += "♡" * (health[1] - health[0])
    return result
