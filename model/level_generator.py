from math import pi, cos, sin, floor, sqrt
from random import random, randint

TILE_SIZE = 4
MIN_RECTANGLE_WIDTH = 10
MIN_RECTANGLE_HEIGHT = 4
MAX_RECTANGLE_WIDTH = 40
MAX_RECTANGLE_HEIGHT = 20
MIN_ROOM_WIDTH = 12
MIN_ROOM_HEIGHT = 12
MAX_LEVEL_WIDTH = 140
MAX_LEVEL_HEIGHT = 100


def park_miller_normal_distribution(seed, lower_bound, upper_bound):
    m = (upper_bound - lower_bound) / 2147483947
    while True:
        seed = (16807 * seed) % 2147483947
        yield m * seed + lower_bound


def distance_between(p1, p2):
    return sqrt(((p2[0] - p1[0]) ** 2) ((p2[1] - p1[1]) ** 2))


pm_rand_width = park_miller_normal_distribution(randint(1, 999), MIN_RECTANGLE_WIDTH, MAX_RECTANGLE_WIDTH)
pm_rand_height = park_miller_normal_distribution(randint(1, 999), MIN_RECTANGLE_HEIGHT, MAX_RECTANGLE_HEIGHT)


def generate_level(level: int):
    pass


def minimum_spanning_tree(rooms: dict):
    edges = list()
    vertices = rooms.copy()
    source = vertices.pop(min(vertices.keys()))
    current_vertex = source
    vertex_num = 0
    while len(vertices) != 0:
        min_dist = 999
        min_vertex = (99, 99)
        for vertex in vertices:
            dist = distance_between(current_vertex, vertex)
            if dist < min_dist:
                min_dist = dist
                min_vertex = vertex

        edges[vertex_num] = [current_vertex, min_vertex]
        current_vertex = vertices.pop(min_vertex)
        vertex_num += 1

    

    for current_room in rooms:
        for room in rooms:
            if room in edges


def get_rooms(rectangles: dict):
    return {pos: rect for pos, rect in rectangles if is_room(rect)}


def is_room(rectangle):
    return rectangle[0] >= MIN_ROOM_WIDTH and rectangle[1] >= MIN_ROOM_HEIGHT


def separation_steering(rectangles: dict):
    for current_position, current_rect in rectangles.items():
        rectangles[current_position] = steer_rectangle(rectangles, current_position)


def steer_rectangle(rectangles: dict, current_position):
    vector = [0, 0]
    neighbors = 0
    for position, rectangle in rectangles.items():
        if position != current_position:
            has_neighbor = False
            x_dist = position[0] - current_position[0]
            y_dist = position[1] - current_position[1]
            if abs(x_dist) < MAX_RECTANGLE_WIDTH / 2:
                vector[0] += x_dist
                has_neighbor = True
            if abs(y_dist) < MAX_RECTANGLE_HEIGHT / 2:
                vector[1] += y_dist
                has_neighbor = True
            if has_neighbor:
                neighbors += 1

    if neighbors == 0:
        return vector
    else:
        #dist = distance_between(vector, [0, 0])

        # divide by neighbors
        vector[0] /= neighbors * -1
        vector[1] /= neighbors * -1

        #vector[0] -= current_position[0]
        #vector[1] -= current_position[1]

        # normalizing
        #vector[0] /= dist
        #vector[1] /= dist
        return [vector[0] + current_position[0], vector[1] + current_position[1]]



def generate_rectangles(num_rooms: int):
    return {random_point_in_ellipse(MAX_LEVEL_WIDTH, MAX_LEVEL_HEIGHT): random_rectangle() for _ in range(num_rooms)}


def random_rectangle():
    return next(pm_rand_width), next(pm_rand_height)


def random_point_in_ellipse(width: int, height: int):
    theta = 2 * pi * random()
    unit_radius = random() + random()

    if unit_radius > 1:
        unit_radius = 2 - unit_radius

    return [snap_to_grid(width * unit_radius * cos(theta)), snap_to_grid(height * unit_radius * sin(theta))]


def snap_to_grid(n: float):
    return floor(((n + TILE_SIZE - 1) / TILE_SIZE)) * TILE_SIZE
