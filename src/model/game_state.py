from enum import Enum


class GameState(Enum):
    IN_GAME = 0
    MAIN_MENU = 1
    LOAD_MENU = 2
    PAUSE_MENU = 3
    SETTINGS_MENU = 4
    EXIT = 5
