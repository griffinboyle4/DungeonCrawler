from controller import Controller
from model import Model


def main():
    """Run to play Dungeon Crawler.
    :return: None
    """
    model = Model()
    cont = Controller(model)
    cont.go()


if __name__ == '__main__':
    main()
