from controller import Controller
from model import Model


def main():
    model = Model()
    cont = Controller(model)
    cont.go()


if __name__ == '__main__':
    main()
