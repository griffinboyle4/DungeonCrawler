from random import randrange, shuffle

import numpy as np

from model.game_grid import GameGrid
from model.level_generator.room import Room
from model.living_entity import Rat
from model.living_entity.player import Player
from model.living_entity.weapon.sword import Sword
from model.position import Position

TILE_SIZE = 4
MIN_RECTANGLE_WIDTH = 10
MIN_RECTANGLE_HEIGHT = 4
MAX_RECTANGLE_WIDTH = 40
MAX_RECTANGLE_HEIGHT = 20
MAX_LEVEL_WIDTH = 202
MAX_LEVEL_HEIGHT = 62

LEVEL_WIDTH = 202
LEVEL_HEIGHT = 62
MIN_NUM_ROOMS = 4
MAX_NUM_ROOMS = 10
MIN_ROOM_WIDTH = 12
MIN_ROOM_HEIGHT = 12
MAX_ROOM_WIDTH = 40
MAX_ROOM_HEIGHT = 15


def init_level():
    return np.zeros((LEVEL_HEIGHT, LEVEL_WIDTH), dtype=np.uint8)


def init_rooms(level_map):
    rooms = list()
    num_rooms = randrange(MIN_NUM_ROOMS, MAX_NUM_ROOMS)

    for i in range(MIN_NUM_ROOMS):
        for j in range(num_rooms):
            if len(rooms) >= MAX_NUM_ROOMS:
                break

            x = randrange(0, LEVEL_WIDTH - 2)
            y = randrange(0, LEVEL_HEIGHT - 2)

            width = randrange(MIN_ROOM_WIDTH, MAX_ROOM_WIDTH)
            height = randrange(MIN_ROOM_HEIGHT, MAX_ROOM_HEIGHT)
            room = Room(Position(x, y), width, height)

            if not room.overlaps(rooms):
                rooms.append(room)

    for room in rooms:
        level_map[room.get_y():room.get_y() + room.get_height(), room.get_x():room.get_x() + room.get_width()] = 1

    return rooms


# noinspection DuplicatedCode
def connect_rooms(rooms, level_map):
    shuffle(rooms)

    # noinspection DuplicatedCode
    for i in range(len(rooms) - 1):
        room_a = rooms[i]
        room_b = rooms[i + 1]

        for x in range(room_a.get_x(), room_b.get_x()):
            level_map[room_a.get_y(), x] = 1
            if room_a.get_y() > 0:
                level_map[room_a.get_y() - 1, x] = 1
            else:
                level_map[room_a.get_y() + 1, x] = 1

        for y in range(room_a.get_y(), room_b.get_y()):
            level_map[y, room_a.get_x()] = 1
            if room_a.get_x() > 0:
                level_map[y, room_a.get_x() - 1] = 1
            else:
                level_map[y, room_a.get_x() + 1] = 1

        for x in range(room_b.get_x(), room_a.get_x()):
            level_map[room_a.get_y(), x] = 1
            if room_a.get_y() > 0:
                level_map[room_a.get_y() - 1, x] = 1
            else:
                level_map[room_a.get_y() + 1, x] = 1

        for y in range(room_b.get_y(), room_a.get_y()):
            level_map[y, room_a.get_x()] = 1
            if room_a.get_x() > 0:
                level_map[y, room_a.get_x() - 1] = 1
            else:
                level_map[y, room_a.get_x() + 1] = 1


def add_boarder_wall(level_map: np.array):
    return np.pad(level_map, 1, mode='constant')


def add_door(level_map: np.array, rooms: list):
    highest_room = rooms[0]
    highest_wall = highest_room.get_position() + Position(highest_room.get_width(), -highest_room.get_height() // 2)

    for y in range(highest_wall.get_y()):
        level_map[y, highest_wall.get_x():highest_wall.get_x() + 2] = 1

    level_map[0, highest_room.get_x()] = 4
    level_map[0, highest_wall.get_x() + 1] = 5


def get_random_point_in_room(room: Room):
    x = randrange(start=room.get_x() + 1, stop=room.get_x() + room.get_width())
    y = room.get_y()

    return Position(x, y)


def generate_mobs(rooms: list, mobs_per_room: int):
    other_rooms = rooms[0:len(rooms) - 1]

    mobs = dict()
    for room in other_rooms:
        for i in range(mobs_per_room):
            mob = Rat(position=room.get_position())
            mobs[mob.get_mob_id()] = mob

    return mobs


def generate_level():
    level_map = init_level()
    rooms = init_rooms(level_map)
    connect_rooms(rooms, level_map)
    rooms.sort()
    spawn = rooms[len(rooms) - 1].get_position()
    level_map = add_boarder_wall(level_map)
    mobs = generate_mobs(rooms, mobs_per_room=1)
    # add_door(level_map, rooms)
    return GameGrid(level_data=level_map,
                    player=Player(health=30, position=Position(spawn.get_x(), spawn.get_y()),
                                  weapon=Sword()),
                    mobs=mobs)
