from sty import fg


class GameGrid:
    def __init__(self, background=[["#"] * 110 for _ in range(25)]):
        self._rows = len(background)
        self._columns = len(background[0])
        self._background = background

    def get_rows(self):
        return self._rows

    def get_columns(self):
        return self._columns

    def get_background(self):
        return [self._background[row].copy() for row in range(self._rows)]
