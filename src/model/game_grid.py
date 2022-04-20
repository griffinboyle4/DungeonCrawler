import numpy as np

from controller import RepeatTimer
from model.direction import Direction
from model.living_entity import LivingEntity
from model.living_entity.player import Player
from model.living_entity.weapon.sword import Sword
from model.position import Position
from model.settings import LEVEL_HEIGHT, LEVEL_WIDTH, FOV_HEIGHT, FOV_WIDTH


class GameGrid:
    def __init__(self,
                 mobs: dict,
                 level_data=np.zeros((LEVEL_HEIGHT, LEVEL_WIDTH)),
                 player=Player(),
                 door_pos=Position(0, 0),
                 level=0,
                 hearts=set()):
        self._rows = len(level_data)
        self._columns = len(level_data[0])
        self._level_data = level_data
        self._level = level
        self._door_pos = door_pos
        self._player = player
        self._data_to_ascii = {-1: '♥',
                               0: '#',
                               1: '.',
                               2: '/',
                               3: '\\',
                               4: self._player.get_symbol(),
                               5: self._player.get_weapon_symbol()}
        self._mobs = mobs
        self._hearts = hearts
        for mob in self._mobs.values():
            self._data_to_ascii[mob.get_mob_id()] = mob.get_symbol()
        self._current_enemy = None
        self._update_flag = True

    def get_player_health(self):
        return self._player.get_health()

    def get_rows(self):
        return self._rows

    def get_columns(self):
        return self._columns

    def get_level_data(self) -> np.array:
        bg = self._level_data.copy()
        bg[self.get_y(), self.get_x()] = 4

        for mob in self._mobs.values():
            bg[mob.get_y(), mob.get_x()] = mob.get_mob_id()

        for heart in self._hearts:
            bg[heart.get_y(), heart.get_x()] = -1

        if self._player.is_attacking():
            weapon_position = self._player.get_weapon_position()
            bg[weapon_position.get_y(), weapon_position.get_x()] = 5
            self._data_to_ascii[5] = self._player.get_weapon_symbol()
        return bg

    def get_fov_grid(self) -> np.array:
        gg = self.get_level_data()
        upper, lower, left, right = self.get_fov()

        return gg[upper:lower, left:right]

    def data_grid_to_ascii(self):
        data_grid = self.get_fov_grid()
        ascii_grid = np.ndarray(shape=data_grid.shape, dtype='<U1')
        for pos, val in np.ndenumerate(data_grid):
            ascii_grid[pos] = self._data_to_ascii[val]

        return ascii_grid

    def get_position(self):
        return self._player.get_position()

    def get_x(self):
        return self._player.get_x()

    def get_y(self):
        return self._player.get_y()

    def left_possible(self, pos: Position):
        return pos.get_x() != 0 and self._level_data[pos.get_y(), pos.get_x() - 1] in (1, -1)

    def up_possible(self, pos: Position):
        return pos.get_y() != 0 and self._level_data[pos.get_y() - 1, pos.get_x()] in (1, -1)

    def right_possible(self, pos: Position):
        return pos.get_x() != self.get_columns() - 1 and self._level_data[pos.get_y(), pos.get_x() + 1] in (1, -1)

    def down_possible(self, pos: Position):
        return pos.get_y() != self.get_rows() - 1 and self._level_data[pos.get_y() + 1, pos.get_x()] in (1, -1)

    def move_left(self, entity: LivingEntity):
        if entity.get_direction() != Direction.LEFT:
            entity.set_direction(Direction.LEFT)

        if self.left_possible(entity.get_position()):
            entity.move_left()

            if isinstance(entity, Player):
                health, max_health = self.get_player_health()
                if health != max_health and self.is_at_heart():
                    self._hearts.remove(entity.get_position())
                    self._player.gain_health(1)

            self.set_need_update()

    def move_right(self, entity: LivingEntity):
        if entity.get_direction() != Direction.RIGHT:
            entity.set_direction(Direction.RIGHT)

        if self.right_possible(entity.get_position()):
            entity.move_right()

            if isinstance(entity, Player):
                health, max_health = self.get_player_health()
                if health != max_health and self.is_at_heart():
                    self._hearts.remove(entity.get_position())
                    self._player.gain_health(1)

            self.set_need_update()

    def move_up(self, entity: LivingEntity):
        if entity.get_direction() != Direction.UP:
            entity.set_direction(Direction.UP)

        if self.up_possible(entity.get_position()):
            entity.move_up()

            if isinstance(entity, Player):
                health, max_health = self.get_player_health()
                if health != max_health and self.is_at_heart():
                    self._hearts.remove(entity.get_position())
                    self._player.gain_health(1)

            self.set_need_update()

    def move_down(self, entity: LivingEntity):
        if entity.get_direction() != Direction.DOWN:
            entity.set_direction(Direction.DOWN)

        if self.down_possible(entity.get_position()):
            entity.move_down()

            if isinstance(entity, Player):
                health, max_health = self.get_player_health()
                if health != max_health and self.is_at_heart():
                    self._hearts.remove(entity.get_position())
                    self._player.gain_health(1)

            self.set_need_update()

    def get_fov(self) -> (int, int, int, int):
        pos = self.get_position()
        upper = (pos.get_y() - (FOV_HEIGHT // 2))
        lower = (pos.get_y() + (FOV_HEIGHT // 2))
        left = (pos.get_x() - (FOV_WIDTH // 2))
        right = (pos.get_x() + (FOV_WIDTH // 2))

        if upper < 0:
            upper = 0
            lower = FOV_HEIGHT
        elif lower > LEVEL_HEIGHT:
            lower = LEVEL_HEIGHT
            upper = lower - FOV_HEIGHT

        if left < 0:
            left = 0
            right = FOV_WIDTH
        elif right > LEVEL_WIDTH:
            right = LEVEL_WIDTH
            left = right - FOV_WIDTH

        return upper, lower, left, right

    def player_attack(self):
        self._player.attack()

        if self._current_enemy is not None:
            self._current_enemy.take_damage(self._player.get_attack())

    def update_dead_mobs(self):
        for mob_id, mob in self._mobs.items():
            if mob.get_health()[0] <= 0:
                del self._mobs[mob_id]
                del self._data_to_ascii[mob_id]
                self._current_enemy = None
                self.set_need_update()
                break

    def move_mob(self, mob):
        if mob.get_position().distance_to(self.get_position()) <= 18 and mob.get_position().distance_to(
                self.get_position()) != 1:
            if abs(mob.get_y() - self.get_y()) > 1:
                if mob.get_y() > self.get_y():
                    self.move_up(mob)
                if mob.get_y() < self.get_y():
                    self.move_down(mob)
            if abs(mob.get_x() - self.get_x()) > 1:
                if mob.get_x() > self.get_x():
                    self.move_left(mob)
                if mob.get_x() < self.get_x():
                    self.move_right(mob)
        if mob.get_position().distance_to(self.get_position()) == 1:
            if mob.get_weapon_position() == self.get_position():
                self._player.take_damage(mob.get_attack())
                if self._current_enemy is not mob:
                    self._current_enemy = mob
            else:
                mob.turn_to_face(self.get_position())
            self.set_need_update()

    def update_mobs(self):
        self.update_dead_mobs()

        for mob in self._mobs.values():
            self.move_mob(mob)

    def get_current_enemy_health(self):
        if self._current_enemy is not None:
            return self._current_enemy.get_health()
        else:
            return None

    def get_current_enemy_symbol(self):
        if self._current_enemy is not None:
            return self._data_to_ascii[self._current_enemy.get_mob_id()]
        else:
            return None

    def get_player(self):
        return self._player

    def __copy__(self):
        return GameGrid(mobs=self._mobs, level_data=self._level_data, player=self._player)

    def is_at_door(self):
        return self.get_position().distance_to(self._door_pos) <= 1.6

    def get_current_level(self):
        return self._level

    def is_at_heart(self):
        return self.get_position() in self._hearts

    def need_update(self):
        if self._update_flag:
            self._update_flag = False
            return True
        return False

    def set_need_update(self):
        self._update_flag = True
