from os import system

from pynput import keyboard
from pynput.keyboard import Controller as KeyBoardController
from pynput.keyboard import Key, KeyCode

from controller.repeat_timer import RepeatTimer
from view import View


class Controller:
    def __init__(self, model):
        self._model = model
        self._view = View(self._model)
        self._cont = KeyBoardController()
        self._key_map = {KeyCode.from_char('w'): self._model.move_up,
                         KeyCode.from_char('s'): self._model.move_down,
                         KeyCode.from_char('a'): self._model.move_left,
                         KeyCode.from_char('d'): self._model.move_right,
                         Key.space: self._model.player_attack}

    def on_press(self, key):
        self._cont.press(Key.backspace)
        try:
            self._key_map[key]()
            self._view.display()
        except KeyError:
            pass
        except NotImplementedError:
            pass

    def update(self):
        self._model.update_mobs()
        self._view.display()

        if self._model.is_game_over():
            self._cont.press(Key.esc)

    def go(self):
        system("clear")
        self._view.display()
        timer = RepeatTimer(0.5, self.update)
        timer.start()
        # The event listener will be running in this block
        with keyboard.Events() as events:
            self._cont.press(Key.backspace)
            for event in events:
                if event.key == Key.esc:
                    self._cont.press(Key.backspace)
                    self._cont.press(Key.backspace)
                    self._cont.press(Key.backspace)
                    timer.cancel()
                    exit(0)
                elif event.key == Key.backspace:
                    continue
                else:
                    if isinstance(event, keyboard.Events.Press):
                        self.on_press(event.key)
