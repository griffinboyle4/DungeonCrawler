from math import sqrt
from random import randrange

import numpy as np

from model.living_entity.weapon.sword import Sword
from model.game_grid import GameGrid
from model.level_generator.room import Room
from model.living_entity.mob import Rat
from model.living_entity.player import Player
from model.position import Position
from model.settings import LEVEL_HEIGHT, LEVEL_WIDTH

TILE_SIZE = 4
MIN_RECTANGLE_WIDTH = 10
MIN_RECTANGLE_HEIGHT = 4
MAX_RECTANGLE_WIDTH = 40
MAX_RECTANGLE_HEIGHT = 20

MIN_NUM_ROOMS = 6
MAX_NUM_ROOMS = 11
MIN_ROOM_WIDTH = 12
MIN_ROOM_HEIGHT = 12
MAX_ROOM_WIDTH = 40
MAX_ROOM_HEIGHT = 15


def init_level():
    """Returns an all-wall 2-D level data array (All 0s)
    with reduced shape to allow for border addition.
    :return: an all-wall 2-D level data array (All 0s)
    """
    return np.zeros((LEVEL_HEIGHT - 2, LEVEL_WIDTH - 2), dtype=np.int8)


def init_rooms(level_map):
    """Generates a list of Rooms with random position, width, and length,
    all of which lie within level boundaries and don't overlap each other.
    Each room is inserted/reflected into the level map, and the list of rooms is returned
    :param level_map: the level data, in which to insert rooms
    :return: the list of rooms
    """
    rooms = []
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

            if room.lies_within(Position(0, 0), Position(LEVEL_WIDTH, LEVEL_HEIGHT)) and not room.overlaps(rooms):
                rooms.append(room)

    for room in rooms:
        level_map[room.get_y():room.get_y() + room.get_height(), room.get_x():room.get_x() + room.get_width()] = 1

    return rooms


def connect_rooms(rooms, level_map):
    """Connects Rooms in level_map with paths, ensuring no unreachable Rooms.
    :param rooms: the list of rooms
    :param level_map: the level_data with isolated rooms
    :return: None
    """
    for i in range(len(rooms) - 1):
        room_a = rooms[i]
        room_b = rooms[i + 1]
        cols, rows = zip(*room_a.get_path_indices_to(room_b))
        level_map[rows, cols] = 1


def add_boarder_wall(level_map: np.ndarray):
    """Pads the given level map on all sides with walls,
    restricting movement to within level_map alone.
    :param level_map: the level data with connected rooms
    :return: the given level map with walls on all sides
    """
    return np.pad(level_map, pad_width=1, mode='constant', constant_values=0)


def add_door(level_map: np.ndarray, rooms: list):
    """Determines the door position from Room closest to origin,
    creates path in Room to door, inserts door into level data,
    and returns the position of the door.
    :param level_map: the level data with walls and connected rooms
    :param rooms: the list of rooms
    :return: the position of the door
    """
    highest_room = rooms[0]
    door_room_sentinel = Room(Position(highest_room.get_center_position().get_x(), 1), width=0, height=0)
    cols, rows = zip(*highest_room.get_path_indices_to(door_room_sentinel))
    level_map[rows, cols] = 1

    level_map[0, door_room_sentinel.get_x() - 1] = 2
    level_map[0, door_room_sentinel.get_x()] = 3

    return Position(door_room_sentinel.get_x(), 0)


def get_random_point_in_room(room: Room):
    """Returns a random Position within the given Room.
    :param room: the Room in which the point will reside
    :return: a random Position within the given Room.
    """
    offset = Position(randrange((room.get_width() - 4) // -2, (room.get_width() - 4) // 2),
                      randrange((room.get_height() - 4) // -2, (room.get_height() - 4) // 2))

    return room.get_center_position() + offset


def generate_mobs(rooms: list, level):
    """Generates a level-influenced randomized distribution
    of mobs with the given list of Rooms, and returns a dictionary
    mapping each Mob's id to its respective Mob.
    :param rooms: the list of rooms in which to spawn Mobs
    :param level: the current level, used to determine difficulty
    :return: a dictionary mapping each Mob's id to its respective Mob
    """
    other_rooms = rooms[0:len(rooms) - 1]

    mobs = dict()
    for room in other_rooms:
        for i in range(randrange(1, round(sqrt((level + 1) * 2.5)))):
            mob = Rat(position=get_random_point_in_room(room))
            mobs[mob.get_mob_id()] = mob

    return mobs


def generate_hearts(rooms: list, level):
    """Generates a level-influenced randomized distribution
    of hearts with the given list of Rooms, and returns a set
    containing each heart's position.
    :param rooms: the list of rooms in which to place hearts
    :param level: the current level, used to determine difficulty
    :return: a set containing each heart's position.
    """
    hearts = set()

    for room in rooms:
        for i in range(randrange(0, 2 + int(sqrt(level)))):
            heart = get_random_point_in_room(room)
            hearts.add(heart)

    return hearts


def generate_level(level=0, player=None):
    """Procedurally generates a Game Grid from the given level and player.
    If level is not specified, the default level is 0. If player
    is not specified, the defualt value is a Player with 10 Health,
    position spawn, and weapon fist. Spawn is determined as the center
    position of the last element of the sorted room array.
    :param level: the level to generate
    :param player: the player to place in Game Grid
    :return: a procedurally generated Game Grid
    """
    level_map = init_level()
    rooms = init_rooms(level_map)
    rooms.sort()
    level_map = add_boarder_wall(level_map)
    connect_rooms(rooms, level_map)
    spawn = rooms[len(rooms) - 1].get_center_position()
    mobs = generate_mobs(rooms, level=level)
    hearts = generate_hearts(rooms, level=level)
    door_pos = add_door(level_map, rooms)
    if player is None:
        player = Player(health=20, position=spawn, weapon=Sword())
    else:
        player.set_position(spawn)

    return GameGrid(level_data=level_map,
                    player=player,
                    mobs=mobs,
                    door_pos=door_pos,
                    level=level,
                    hearts=hearts)
