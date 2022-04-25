from abc import ABC
from model.position import Position
from model.menu.option import Option

import numpy as np

import os.path


class Menu(ABC):
    """This abstract class represents a Menu."""

    def __init__(self, background: np, options: tuple):
        """Constructs a menu with the given background and options.
        :param background: the menu background
        :param options: the menu options
        """
        self._background = background
        self._options = options
        self._current_option = 0
        self._update_flag = True

    def get_current_option(self):
        """Returns the current option index.
        :return: the current option index
        """
        return self._current_option

    def move_down(self, _=None):
        """Moves the selection cursor down, or back to top if at bottom.
        :return: None
        """
        if self._current_option >= len(self._options) - 1:
            self._current_option = 0
        else:
            self._current_option += 1

        self.set_need_update()

    def move_up(self, _=None):
        """Moves the selection cursor up, or back to bottom if at top.
        :return: None
        """
        if self._current_option <= 0:
            self._current_option = len(self._options) - 1
        else:
            self._current_option -= 1

        self.set_need_update()

    def move_left(self, _=None):
        """Moves the selection cursor left, or back to right if at left.
        :return: None
        """
        raise NotImplemented()

    def move_right(self, _=None):
        """Moves the selection cursor right, or back to left if at right.
        :return: None
        """
        raise NotImplemented()

    def choose(self):
        """Retrieves the name of the currently selected option.
        :return: the name of the currently selected option
        """
        return self._options[self._current_option].choose()

    def get_full_background(self):
        """Returns the menu background with selection cursors included.
        :return: the menu background with selection cursors included
        """
        (left_pos, right_pos) = self._options[self._current_option].select()

        bg = self._background.copy()
        bg[left_pos.get_y(), left_pos.get_x()] = "="
        bg[right_pos.get_y(), right_pos.get_x()] = "="

        return bg

    def need_update(self):
        """Checks if an update is necessary. If so, additionally resets update flag to False.
        :return: True if update flag is True, else False
        """
        if self._update_flag:
            self._update_flag = False
            return True

        return False

    def set_need_update(self):
        """Requests an update for the GameGrid by setting update flag to True.
        :return: None
        """
        self._update_flag = True


class MainMenu(Menu):
    """This class represents the Main Menu"""
    background = np.loadtxt("model/menu/main_menu.txt", dtype='<U1')

    def __init__(self):
        """Constructs a Main Menu"""
        load_option = Option("load", Position(61, 20), Position(89, 20))
        exit_option = Option("exit", Position(68, 24), Position(81, 24))
        super().__init__(background=MainMenu.background, options=(load_option, exit_option))


def get_saves():
    """Retrieves the attendance of the three save slots as a size-3 tuple of boolean values.
    :return: the attendance of the three save slots as a size-3 tuple of boolean values
    """
    return (os.path.exists("save_data/save1.dat"),
            os.path.exists("save_data/save2.dat"),
            os.path.exists("save_data/save3.dat"))


class LoadMenu(Menu):
    """This class represents the Load Menu"""
    background = np.loadtxt("model/menu/load_menu.txt", dtype='<U1')

    def __init__(self):
        """Constructs a Load Menu"""
        slot1 = Option("slot1", Position(62, 15), Position(87, 15))
        slot2 = Option("slot2", Position(62, 19), Position(88, 19))
        slot3 = Option("slot3", Position(59, 23), Position(90, 23))
        super().__init__(background=LoadMenu.background, options=(slot1, slot2, slot3))

    def get_full_background(self):
        """Returns the menu background with selection cursors and save slot state included.
        :return: the menu background with selection cursors and save slot state included
        """
        bg = super().get_full_background()
        saves = get_saves()
        for i in range(len(saves)):
            if saves[i]:
                bg[17 + (i * 4), 72] = "S"
                bg[17 + (i * 4), 73] = "A"
                bg[17 + (i * 4), 74] = "V"
                bg[17 + (i * 4), 75] = "E"
                bg[17 + (i * 4), 76] = str(i + 1)
            else:
                bg[17 + (i * 4), 72] = "E"
                bg[17 + (i * 4), 73] = "M"
                bg[17 + (i * 4), 74] = "P"
                bg[17 + (i * 4), 75] = "T"
                bg[17 + (i * 4), 76] = "Y"

        return bg

    def delete_save(self):
        """Deletes the currently selected save, if it exists
        :return: None
        """
        curr = self.get_current_option()
        save = get_saves()[curr]
        if save:
            os.remove("save_data/save" + str(curr + 1) + ".dat")
            self.set_need_update()


class PauseMenu(Menu):
    """This class represents the Pause Menu"""
    background = np.loadtxt("model/menu/pause_menu.txt", dtype='<U1')

    def __init__(self):
        """Constructs a Pause Menu"""
        resume = Option("resume", Position(65, 15), Position(85, 15))
        save = Option("save", Position(67, 19), Position(82, 19))
        quit_option = Option("quit", Position(68, 23), Position(81, 23))
        super().__init__(background=PauseMenu.background, options=(resume, save, quit_option))


class DeathMenu(Menu):
    """This class represents the Death Menu"""
    background = np.loadtxt("model/menu/death_menu.txt", dtype='<U1')

    def __init__(self):
        """Constructs a Death Menu"""
        new_game = Option("new_game", Position(62, 17), Position(88, 17))
        main_menu = Option("main_menu", Position(62, 22), Position(90, 22))
        super().__init__(background=DeathMenu.background, options=(new_game, main_menu))
