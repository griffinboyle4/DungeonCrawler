from model.settings import FOV_WIDTH, FOV_HEIGHT
from model.position import Position
from model.menu.option import Option

import numpy as np

import os.path


class Menu:
    def __init__(self, background: np, options: tuple):
        self._background = background
        self._options = options
        self._current_option = 0
        self._update_flag = True

    def get_current_option(self):
        return self._current_option

    def move_down(self, _=None):
        if self._current_option >= len(self._options) - 1:
            self._current_option = 0
        else:
            self._current_option += 1

        self.set_need_update()

    def move_up(self, _=None):
        if self._current_option <= 0:
            self._current_option = len(self._options) - 1
        else:
            self._current_option -= 1

        self.set_need_update()

    def move_left(self, _=None):
        raise NotImplemented()

    def move_right(self, _=None):
        raise NotImplemented()

    def choose(self):
        return self._options[self._current_option].choose()

    def get_full_background(self):
        (left_pos, right_pos) = self._options[self._current_option].select()

        bg = self._background.copy()
        bg[left_pos.get_y(), left_pos.get_x()] = "="
        bg[right_pos.get_y(), right_pos.get_x()] = "="

        return bg

    def need_update(self):
        if self._update_flag:
            self._update_flag = False
            return True

        return False

    def set_need_update(self):
        self._update_flag = True


class MainMenu(Menu):
    background = np.loadtxt("model/menu/main_menu.txt", dtype='<U1')

    def __init__(self):
        load_option = Option("load", Position(61, 20), Position(89, 20))
        exit_option = Option("exit", Position(68, 24), Position(81, 24))
        super().__init__(background=MainMenu.background, options=(load_option, exit_option))


def get_saves():
    return (os.path.exists("save_data/save1.dat"),
            os.path.exists("save_data/save2.dat"),
            os.path.exists("save_data/save3.dat"))


class LoadMenu(Menu):
    background = np.loadtxt("model/menu/load_menu.txt", dtype='<U1')

    def __init__(self):
        slot1 = Option("slot1", Position(62, 15), Position(87, 15))
        slot2 = Option("slot2", Position(62, 19), Position(88, 19))
        slot3 = Option("slot3", Position(59, 23), Position(90, 23))
        super().__init__(background=LoadMenu.background, options=(slot1, slot2, slot3))

    def get_full_background(self):
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
        curr = self.get_current_option()
        save = get_saves()[curr]
        if save:
            os.remove("save_data/save" + str(curr + 1) + ".dat")
            self.set_need_update()


class PauseMenu(Menu):
    background = np.loadtxt("model/menu/pause_menu.txt", dtype='<U1')

    def __init__(self):
        resume = Option("resume", Position(65, 15), Position(85, 15))
        save = Option("save", Position(67, 19), Position(82, 19))
        quit_option = Option("quit", Position(68, 23), Position(81, 23))
        super().__init__(background=PauseMenu.background, options=(resume, save, quit_option))


class SettingsMenu(Menu):
    background = np.loadtxt("model/menu/settings_menu.txt", dtype='<U1')

    def __init__(self):
        width = Option("width", Position(67, 17), Position(83, 17))
        height = Option("height", Position(66, 22), Position(84, 22))
        super().__init__(background=SettingsMenu.background, options=(width, height))

    def get_full_background(self):
        bg = super().get_full_background()
        return bg
