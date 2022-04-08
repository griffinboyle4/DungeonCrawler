from sty import fg


class Player:
    def __init__(self):
        self._symbol = "&"
        self._color = "white"

    def set_symbol(self, symbol):
        self._symbol = symbol

    def set_color(self, color):
        self._color = color

    def to_string(self):
        return fg(10, 255, 10) + self._symbol + fg.rs
