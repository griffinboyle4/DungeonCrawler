from controller import RepeatTimer
from model.living_entity.weapon.fist import Fist
from model.direction import Direction
from model.game_state import GameState
from model.level_generator import generate_level
from model.menu import MainMenu, PauseMenu, LoadMenu, SettingsMenu
from dill import dump, load


class Model:
    def __init__(self, game_grid=generate_level(), current_game_state=GameState.MAIN_MENU):
        self._game_state = current_game_state
        self._game_grid = game_grid
        self._save_slot = -1
        self._main_menu = MainMenu()
        self._pause_menu = PauseMenu()
        self._load_menu = LoadMenu()
        self._settings_menu = SettingsMenu()
        self._game_states = {GameState.MAIN_MENU: self.get_main_menu,
                             GameState.PAUSE_MENU: self.get_pause_menu,
                             GameState.LOAD_MENU: self.get_load_menu,
                             GameState.IN_GAME: self.get_game_grid,
                             GameState.SETTINGS_MENU: self.get_settings_menu}
        self._menu_operations = {"load": self.set_game_state_load_menu,
                                 "exit": self.set_game_state_exit,
                                 "slot1": self.load_save_1,
                                 "slot2": self.load_save_2,
                                 "slot3": self.load_save_3,
                                 "resume": self.set_game_state_in_game,
                                 "save": self.save_game,
                                 "quit": self.set_game_state_main_menu}

    def get_main_menu(self):
        return self._main_menu

    def get_pause_menu(self):
        return self._pause_menu

    def get_load_menu(self):
        return self._load_menu

    def get_game_grid(self):
        return self._game_grid

    def set_game_grid(self, game_grid):
        self._game_grid = game_grid

    #def toggle_mob_clock_state(self):
    #    if not self._mob_clock.is_alive():
    #        self._mob_clock.start()
    #    else:
    #        self._mob_clock.cancel()
    #        self._mob_clock = RepeatTimer(0.5, self.update_mobs)

    def get_current_level(self):
        return self._game_grid.get_current_level()

    def get_game_state_at(self, game_state: GameState):
        return self._game_states[game_state]()

    def choose(self):
        self._menu_operations[self.get_current_game_state().choose()]()

    def get_game_state(self):
        return self._game_state

    def get_current_game_state(self):
        return self._game_states[self._game_state]()

    def set_game_state(self, new_state: GameState):
        self._game_state = new_state
        self.request_update()

    def set_game_state_load_menu(self):
        self.set_game_state(GameState.LOAD_MENU)

    def set_game_state_exit(self):
        self.set_game_state(GameState.EXIT)

    def set_game_state_in_game(self):
        self.set_game_state(GameState.IN_GAME)

    def set_game_state_main_menu(self):
        self.set_game_state(GameState.MAIN_MENU)

    def set_game_state_pause_menu(self):
        self.set_game_state(GameState.PAUSE_MENU)

    def set_game_state_settings_menu(self):
        self.set_game_state(GameState.SETTINGS_MENU)

    def get_settings_menu(self):
        return self._settings_menu

    def get_columns(self):
        return self._game_grid.get_columns()

    def get_rows(self):
        return self._game_grid.get_rows()

    def get_position(self):
        return self._game_grid.get_position()

    def get_x(self):
        return self._game_grid.get_x()

    def get_y(self):
        return self._game_grid.get_x()

    def move_left(self):
        self._game_grid.move_left(self._game_grid.get_player())

    def move_right(self):
        self._game_grid.move_right(self._game_grid.get_player())

    def move_up(self):
        self._game_grid.move_up(self._game_grid.get_player())

        if self._game_grid.is_at_door():
            self._game_grid = generate_level(self.get_current_level() + 1, self._game_grid.get_player())

    def move_down(self):
        self._game_grid.move_down(self._game_grid.get_player())

    def data_grid_to_ascii(self):
        return self._game_grid.data_grid_to_ascii()

    def player_attack(self):
        self._game_grid.player_attack()

    def game_state_is_exit(self):
        return self._game_state == GameState.EXIT

    def update_mobs(self):
        if self._game_state == GameState.IN_GAME:
            self._game_grid.update_mobs()

    def get_player_health(self):
        return self._game_grid.get_player_health()

    def get_current_enemy_health(self):
        return self._game_grid.get_current_enemy_health()

    def get_current_enemy_symbol(self):
        return self._game_grid.get_current_enemy_symbol()

    def save_game(self):
        with open("save_data/save" + str(self._save_slot) + ".dat", "wb") as save_file:
            dump(self.get_game_grid(), save_file)

        self.set_game_state_main_menu()

    def load_save_1(self):
        if menu.get_saves()[0]:
            with open("save_data/save1.dat", "rb") as save_file:
                self.set_game_grid(load(save_file))
        else:
            with open("save_data/save1.dat", "wb") as save_file:
                self.set_game_grid(generate_level())
                dump(self.get_game_grid(), save_file)

        self._save_slot = 1
        self.set_game_state(GameState.IN_GAME)
        self.request_update()

    def load_save_2(self):
        if menu.get_saves()[1]:
            with open("save_data/save2.dat", "rb") as save_file:
                self.set_game_grid(load(save_file))
        else:
            with open("save_data/save2.dat", "wb") as save_file:
                self.set_game_grid(generate_level())
                dump(self.get_game_grid(), save_file)

        self._save_slot = 2
        self.set_game_state(GameState.IN_GAME)
        self.request_update()

    def load_save_3(self):
        if menu.get_saves()[2]:
            with open("save_data/save3.dat", "rb") as save_file:
                self.set_game_grid(load(save_file))
                self.set_game_state(GameState.IN_GAME)
        else:
            with open("save_data/save3.dat", "wb") as save_file:
                self.set_game_grid(generate_level())
                dump(self.get_game_grid(), save_file)

        self._save_slot = 3
        self.set_game_state(GameState.IN_GAME)
        self.request_update()

    def request_update(self):
        self.get_current_game_state().set_need_update()
