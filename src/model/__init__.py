from model.living_entity.weapon.fist import Fist
from model.direction import Direction
from model.game_state import GameState
from model.level_generator import generate_level
from model.menu import MainMenu, PauseMenu, LoadMenu, SettingsMenu
from dill import dump, load


class Model:
    """This class represents a model in Dungeon Crawler"""
    def __init__(self, game_grid=generate_level(), current_game_state=GameState.MAIN_MENU):
        """Contructs a new model from the given Game Grid and Game State. If
        no Game Grid is provided, the a Game Grid is generated at level 0.
        If no Game State is provided, the Game State defaults to Main Menu.
        :param game_grid: the Game Grid from which the model is constructed
        :param current_game_state: the Game State to which the model is initialized.
        """
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
        """Retrieves the Main Menu Game State.
        :return: the Main Menu Game State
        """
        return self._main_menu

    def get_pause_menu(self):
        """Retrieves the Pause Menu Game State.
        :return: the Pause Menu Game State
        """
        return self._pause_menu

    def get_load_menu(self):
        """Retrieves the Load Menu Game State.
        :return: the Load Menu Game State
        """
        return self._load_menu

    def get_game_grid(self):
        """Retrieves the Game Grid Game State.
        :return: the Game Grid Game State
        """
        return self._game_grid

    def set_game_grid(self, game_grid):
        """Assigns the Game Grid to the provided Game Grid.
        :param game_grid: the Game Grid to assign.
        :return: None
        """
        self._game_grid = game_grid

    def get_current_level(self):
        """Retrieves the current level of the Game Grid Game State.
        :return: the current level of the Game Grid Game State
        """
        return self._game_grid.get_current_level()

    def get_game_state_at(self, game_state: GameState):
        """Retrieves the specified Game State.
        :param game_state: the Game State to retrieve
        :return: the specified Game State
        """
        return self._game_states[game_state]()

    def choose(self):
        """Performs the selected menu option.
        :return: None
        """
        self._menu_operations[self.get_current_game_state().choose()]()

    def get_game_state(self):
        """Retrieves the current Game State type.
        :return: the current Game State type
        """
        return self._game_state

    def get_current_game_state(self):
        """Retrieves the current Game State.
        :return: the current Game State
        """
        return self._game_states[self._game_state]()

    def set_game_state(self, new_state: GameState):
        """Assigns the Game State to the provided Game State Type.
        :param new_state: the Game State type to assign
        :return: None
        """
        self._game_state = new_state
        self.request_update()

    def set_game_state_load_menu(self):
        """Sets the Game State to Load Menu.
        :return: None
        """
        self.set_game_state(GameState.LOAD_MENU)

    def set_game_state_exit(self):
        """Sets the Game State to Exit.
        :return: None
        """
        self.set_game_state(GameState.EXIT)

    def set_game_state_in_game(self):
        """Sets the Game State to In Game.
        :return: None
        """
        self.set_game_state(GameState.IN_GAME)

    def set_game_state_main_menu(self):
        """Sets the Game State to Main Menu.
        :return: None
        """
        self.set_game_state(GameState.MAIN_MENU)

    def set_game_state_pause_menu(self):
        """Sets the Game State to Pause Menu.
        :return: None
        """
        self.set_game_state(GameState.PAUSE_MENU)

    def set_game_state_settings_menu(self):
        """Sets the Game State to Settings Menu.
        :return: None
        """
        self.set_game_state(GameState.SETTINGS_MENU)

    def get_settings_menu(self):
        """Retrieves the Settings Menu Game State.
        :return: the Settings Menu Game State
        """
        return self._settings_menu

    def get_position(self):
        """Retrieves the current player position.
        :return: the current player position
        """
        return self._game_grid.get_position()

    def get_x(self):
        """Retrieves the player's current x-position.
        :return: the player's current x-position
        """
        return self._game_grid.get_x()

    def get_y(self):
        """Retrieves the player's current y-position.
        :return: the player's current y-position
        """
        return self._game_grid.get_x()

    def move_left(self):
        """Moves the player left in Game Grid.
        :return: None
        """
        self._game_grid.move_left(self._game_grid.get_player())

    def move_right(self):
        """Moves the player right in Game Grid.
        :return: None
        """
        self._game_grid.move_right(self._game_grid.get_player())

    def move_up(self):
        """Moves the player up in Game Grid.
        :return: None
        """
        self._game_grid.move_up(self._game_grid.get_player())

        if self._game_grid.is_at_door():
            self._game_grid = generate_level(self.get_current_level() + 1, self._game_grid.get_player())

    def move_down(self):
        """Moves the player down in Game Grid.
        :return: None
        """
        self._game_grid.move_down(self._game_grid.get_player())

    def data_grid_to_ascii(self):
        """Returns the Game Grid as Chararray of respective character-mapped translations.
        :return: the Game Grid as Chararray of respective character-mapped translations
        """
        return self._game_grid.data_grid_to_ascii()

    def player_attack(self):
        """Toggles whether player is attacking.
        :return: None
        """
        self._game_grid.player_attack()
        self.request_update()

    def game_state_is_exit(self):
        """Determines whether the current Game State is Exit.
        :return: True if the current Game State is Exit, else False
        """
        return self._game_state == GameState.EXIT

    def update_mobs(self):
        """Updates mobs if Game State is In Game.
        :return: None
        """
        if self._game_state == GameState.IN_GAME:
            self._game_grid.update_mobs()

    def get_player_health(self):
        """Retrieves the player's health and max health, as a size-2 tuple.
        :return: the player's health, the player's max health
        """
        return self._game_grid.get_player_health()

    def get_current_enemy_health(self):
        """Retrieves the current enemy's health and max health, as a size-2 tuple.
        :return: the current enemy's health and max health, as a size-2 tuple
        """
        return self._game_grid.get_current_enemy_health()

    def get_current_enemy_symbol(self):
        """Retrieves the current enemy's symbol.
        :return: the current enemy's symbol
        """
        return self._game_grid.get_current_enemy_symbol()

    def save_game(self):
        """Saves the current Game Grid to the current save slot and returns to the Main Menu.
        :return: None
        """
        with open("save_data/save" + str(self._save_slot) + ".dat", "wb") as save_file:
            dump(self.get_game_grid(), save_file)

        self.set_game_state_main_menu()

    def load_save_1(self):
        """Loads Game Grid from slot 1 if exists, else generates new
        Game Grid at level 0 and saves to slot 1. Goes to In Game after.
        :return: None
        """
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
        """Loads Game Grid from slot 2 if exists, else generates new
        Game Grid at level 0 and saves to slot 2. Goes to In Game after.
        :return: None
        """
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
        """Loads Game Grid from slot 3 if exists, else generates new
        Game Grid at level 0 and saves to slot 3. Goes to In Game after.
        :return: None
        """
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
        """Sets update flag in current Game State to True.
        :return: None
        """
        self.get_current_game_state().set_need_update()
