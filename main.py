from controller.controller import Controller
from model.model import Model
from pynput import keyboard


def main():
    model = Model()
    cont = Controller(model)
    cont.go()


if __name__ == '__main__':
    main()
