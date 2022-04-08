from model.model import Model


class View:
    def __init__(self, model=Model()):
        self._model = model

    def display(self):
        print(self._model.to_string())

# To-Do #
