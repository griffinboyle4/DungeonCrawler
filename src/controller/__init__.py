from os import system

from pynput import keyboard
from pynput.keyboard import Controller as KeyBoardController
from pynput.keyboard import Key, KeyCode

from controller.repeat_timer import RepeatTimer
from model import GameState
from view import View

from threading import Thread


class Controller:
    def __init__(self, model):
        self._model = model
        self._view = View(self._model)
        self._cont = KeyBoardController()
        self._update_clock = RepeatTimer(0.5, self.update)
        _in_game_key_map = {KeyCode.from_char('w'): self._model.move_up,
                            KeyCode.from_char('s'): self._model.move_down,
                            KeyCode.from_char('a'): self._model.move_left,
                            KeyCode.from_char('d'): self._model.move_right,
                            Key.space: self._model.player_attack,
                            Key.esc: self._model.set_game_state_pause_menu}
        _main_menu_key_map = {KeyCode.from_char('w'): self._model.get_game_state_at(GameState.MAIN_MENU).move_up,
                              KeyCode.from_char('s'): self._model.get_game_state_at(GameState.MAIN_MENU).move_down,
                              Key.space: self._model.choose,
                              Key.shift: self._model.set_game_state_settings_menu}
        _load_menu_key_map = {KeyCode.from_char('w'): self._model.get_game_state_at(GameState.LOAD_MENU).move_up,
                              KeyCode.from_char('s'): self._model.get_game_state_at(GameState.LOAD_MENU).move_down,
                              KeyCode.from_char('c'): self._model.get_game_state_at(GameState.LOAD_MENU).delete_save,
                              Key.space: self._model.choose,
                              Key.esc: self._model.set_game_state_main_menu}
        _pause_menu_key_map = {KeyCode.from_char('w'): self._model.get_game_state_at(GameState.PAUSE_MENU).move_up,
                               KeyCode.from_char('s'): self._model.get_game_state_at(GameState.PAUSE_MENU).move_down,
                               Key.space: self._model.choose,
                               Key.esc: self._model.set_game_state_in_game}

        self._key_map = {GameState.MAIN_MENU: _main_menu_key_map,
                         GameState.PAUSE_MENU: _pause_menu_key_map,
                         GameState.LOAD_MENU: _load_menu_key_map,
                         GameState.IN_GAME: _in_game_key_map}
        self._listener = keyboard.Listener(on_press=self.on_press)


    def get_game_state(self):
        return self._model.get_game_state()

    def on_press(self, key):
        self._cont.press(Key.backspace)
        try:
            self._key_map[self.get_game_state()][key]()
        except KeyError:
            pass
        except NotImplementedError:
            pass

    def update(self):
        self._model.update_mobs()
        self._view.display()

        if self.get_game_state() == GameState.EXIT:
            self._cont.press(".")

    def go(self):
        system("clear")
        #self._view.display()
        with keyboard.Events() as events:
            self._update_clock.start()
            self._cont.press(Key.backspace)
            for event in events:
                if event.key == KeyCode.from_char("."):
                    self._cont.press(Key.backspace)
                    self._update_clock.cancel()
                    exit(0)
                elif event.key == Key.backspace:
                    continue
                else:
                    if isinstance(event, keyboard.Events.Press):
                       self.on_press(event.key)
                       self._view.display()

# The event listener will be running in this block
# with keyboard.Events() as events:
#    self._cont.press(Key.backspace)
#    for event in events:
#        if event.key == KeyCode.from_char("."):
#            self._cont.press(Key.backspace)
#            self._update_clock.cancel()
#            return
#        elif event.key == Key.backspace:
#            continue
#        else:
#            if isinstance(event, keyboard.Events.Press):
#               self.on_press(event.key)

# with keyboard.Events() as events:
#    self._cont.press(Key.backspace)
#    for event in events:
#        if event.key == KeyCode.from_char("Æ"):
#            self._cont.press(Key.backspace)
#            self._update_clock.cancel()
#            exit(0)
#        elif event.key == Key.backspace:
#            continue
#        else:
#            if isinstance(event, keyboard.Events.Press):
#                self.on_press(event.key)