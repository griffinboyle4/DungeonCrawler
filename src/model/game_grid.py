import numpy as np

from model.direction import Direction
from model.living_entity import LivingEntity
from model.living_entity.player import Player
from model.position import Position
from model.settings import LEVEL_HEIGHT, LEVEL_WIDTH, FOV_HEIGHT, FOV_WIDTH


class GameGrid:
    """This class represents a populated game data grid in Dungeon Crawler"""
    def __init__(self,
                 mobs={},
                 level_data=np.zeros((LEVEL_HEIGHT, LEVEL_WIDTH)),
                 player=Player(),
                 door_pos=Position(0, 0),
                 level=0,
                 hearts=set()):
        """Constructs a Game Grid with the given mobs, level data, player,
        door position, level, and hearts. If no mobs are provided, no mobs are placed in the
        Game Grid. If no level data is provided, the level data is set to a 2-D array of 0s (all walls).
        If no player is provided, a new player is created. If no door position is provided,
        the door position is set to the origin. If no level is provided, the level is set to 0.
        If no hearts are provided, no hearts will be included in the Game Grid.
        :param mobs: a dictionary mapping each mob id to its respective mob
        :param level_data: a 2-D numpy array of dtype int8 representing level data
        :param player: the player
        :param door_pos: the position of the door in the Game Grid
        :param level: the current level of the Game Grid
        :param hearts: a list of Positions corresponding to each heart in the Game Grid
        """
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
        """Retrieves the player's health and max health, as a size-2 tuple.
        :return: the player's health, the player's max health
        """
        return self._player.get_health()

    def get_rows(self):
        """Returns the number of rows in the Game Grid.
        :return: the number of rows in the Game Grid
        """
        return self._rows

    def get_columns(self):
        """Returns the number of columns in the Game Grid.
        :return: the number of columns in the Game Grid
        """
        return self._columns

    def get_level_data(self) -> np.ndarray:
        """Returns the level data from the Game Grid.
        :return: the level data from the Game Grid
        """
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

    def get_fov_grid(self) -> np.ndarray:
        """Returns the portion of the level data with the FOV.
        :return: the portion of the level data with the FOV
        """
        gg = self.get_level_data()
        upper, lower, left, right = self.get_fov()

        return gg[upper:lower, left:right]

    def data_grid_to_ascii(self):
        """Returns the Game Grid as Chararray of respective character-mapped translations.
        :return: the Game Grid as Chararray of respective character-mapped translations
        """
        data_grid = self.get_fov_grid()
        ascii_grid = np.ndarray(shape=data_grid.shape, dtype='<U1')
        for pos, val in np.ndenumerate(data_grid):
            ascii_grid[pos] = self._data_to_ascii[val]

        return ascii_grid

    def get_position(self):
        """Retrieves the current position of the player.
        :return: the current position of the player
        """
        return self._player.get_position()

    def get_x(self):
        """Retrieves the player's current x-position.
        :return: the player's current x-position
        """
        return self._player.get_x()

    def get_y(self):
        """Retrieves the player's current x-position.
        :return: the player's current x-position
        """
        return self._player.get_y()

    def left_possible(self, pos: Position):
        """Checks whether a left move is possible at the given position.
        :param pos: the position
        :return: True if left move is possible, else False
        """
        return pos.get_x() != 0 and self._level_data[pos.get_y(), pos.get_x() - 1] in (1, -1)

    def up_possible(self, pos: Position):
        """Checks whether an up move is possible at the given position.
        :param pos: the position
        :return: True if up move is possible, else False
        """
        return pos.get_y() != 0 and self._level_data[pos.get_y() - 1, pos.get_x()] in (1, -1)

    def right_possible(self, pos: Position):
        """Checks whether a right move is possible at the given position.
        :param pos: the position
        :return: True if right move is possible, else False
        """
        return pos.get_x() != self.get_columns() - 1 and self._level_data[pos.get_y(), pos.get_x() + 1] in (1, -1)

    def down_possible(self, pos: Position):
        """Checks whether a down move is possible at the given position.
        :param pos: the position
        :return: True if down move is possible, else False
        """
        return pos.get_y() != self.get_rows() - 1 and self._level_data[pos.get_y() + 1, pos.get_x()] in (1, -1)

    def move_left(self, entity: LivingEntity):
        """Moves the given entity left, if possible. Also
        faces left if not previously facing left.
        :param entity: the entity to move left
        :return: None
        """
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
        """Moves the given entity right, if possible. Also
        faces right if not previously facing right.
        :param entity: the entity to move right
        :return: None
        """
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
        """Moves the given entity up, if possible. Also
        faces up if not previously facing up.
        :param entity: the entity to move up
        :return: None
        """
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
        """Moves the given entity down, if possible. Also
        faces down if not previously facing down.
        :param entity: the entity to move dow
        :return: None
        """
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
        """Returns the FOV indices as a size-4 tuple of boundaries.
        :return: a size-4 tuple of form (upper, lower, left, right)
        """
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
        """Toggles whether player attacking.
        :return: None
        """
        self._player.attack()

        if self._current_enemy is not None:
            self._current_enemy.take_damage(self._player.get_attack())

    def update_dead_mobs(self):
        """Removes any dead mobs from the Game Grid.
        :return: None
        """
        for mob_id, mob in self._mobs.items():
            if mob.get_health()[0] <= 0:
                del self._mobs[mob_id]
                del self._data_to_ascii[mob_id]
                self._current_enemy = None
                self.set_need_update()
                break

    def move_mob(self, mob):
        """Exhibits mob behavior - either stationary, moving towards player, or attacking player - on given mob.
        :param mob: the mob to examine/manipulate
        :return: None
        """
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
        if abs(mob.get_position() - self.get_position()) == Position(1, 1):
            if mob.get_x() < self.get_x():
                self.move_right(mob)
            else:
                self.move_left(mob)

        if mob.get_position().distance_to(self.get_position()) == 1:
            if mob.get_weapon_position() == self.get_position():
                self._player.take_damage(mob.get_attack())
                if self._current_enemy is not mob:
                    self._current_enemy = mob
            else:
                mob.turn_to_face(self.get_position())
            self.set_need_update()

    def update_mobs(self):
        """Removes dead mobs from Game Grid and prompts
        each mob to exhibit appropriate behaviour.
        :return: None
        """
        self.update_dead_mobs()

        for mob in self._mobs.values():
            self.move_mob(mob)

    def get_current_enemy_health(self):
        """Retrieves the current enemy's health and max health, as a size-2 tuple.
        :return: the current enemy's health and max health,
        as a size-2 tuple - or None if no current enemy
        """
        if self._current_enemy is not None:
            return self._current_enemy.get_health()
        else:
            return None

    def get_current_enemy_symbol(self):
        """Retrieves the current enemy's symbol.
        :return: the current enemy's symbol
        """
        if self._current_enemy is not None:
            return self._data_to_ascii[self._current_enemy.get_mob_id()]
        else:
            return None

    def get_player(self):
        """Returns the player in the Game Grid.
        :return: the player in the Game Grid
        """
        return self._player

    def __copy__(self):
        """Creates a shallow copy of the Game Grid.
        :return: a shallow copy of the Game Grid
        """
        return GameGrid(mobs=self._mobs, level_data=self._level_data, player=self._player)

    def is_at_door(self):
        """Checks if player is at the door.
        :return: True if player is at the door, else False
        """
        return self.get_position().distance_to(self._door_pos) <= 1.6

    def get_current_level(self):
        """Returns the current level of the Game Grid.
        :return: the current level of the Game Grid
        """
        return self._level

    def is_at_heart(self):
        """Checks if player is at a heart in Game Grid.
        :return: True if player position is also a heart position, else False
        """
        return self.get_position() in self._hearts

    def need_update(self):
        """Checks if an update is necessary. If so, additionally resets update flag to False.
        :return: True if update flag is True, else False
        """
        if self._update_flag:
            self._update_flag = False
            return True
        return False

    def set_need_update(self):
        """Requests an update for the GameGrid by setting update flag to True.
        :return: None
        """
        self._update_flag = True

    def is_player_dead(self):
        """Checks if player is dead.
        :return: True if player is dead, else False
        """
        return self._player.get_health()[0] <= 0