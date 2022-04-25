import os

from model import GameState


class View:
    """This class represents a view in Dungeon Crawler."""
    def __init__(self, model):
        """Constructs a view from the given model.
        :param model: the model from which the view is constructed
        """
        self._model = model

    def display(self):
        """Prints the current Game State in a user-friendly format.
        :return: None
        """
        if self._model.get_game_state() == GameState.IN_GAME:
            if self._model.get_current_game_state().need_update():
                hud = "\n\n\n\t\tHealth: " + health_to_string(self._model.get_player_health()) + "\t"

                if self._model.get_current_enemy_symbol() is not None:
                    hud += self._model.get_current_enemy_symbol() + ": "
                    hud += health_to_string(self._model.get_current_enemy_health()) + "\t"
                else:
                    hud += "\t"

                hud += "\tLevel: " + str(self._model.get_current_level() + 1)

                print("\n\n\n\t\t" + '\n\t\t'.join([''.join(row)
                                              for row
                                              in self._model.data_grid_to_ascii()]) + hud)
        elif self._model.get_game_state() != GameState.EXIT:
            if self._model.get_current_game_state().need_update():
                os.system("clear")
                print("\n\n\n\t\t" + '\n\t\t'.join([''.join(row)
                                              for row
                                              in self._model.get_current_game_state().get_full_background()]))


def health_to_string(health: tuple):
    """Returns a health tuple as a user-friendly string.
    :param health: the health and max_health, as a size-2 tuple
    :return: a user-friendly string representation of health
    """
    result = str()
    result += "♥" * health[0]
    result += "♡" * (health[1] - health[0])
    return result
