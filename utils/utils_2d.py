from typing import List, Tuple
import numpy as np
from settings import gravity
from pygame.math import Vector2


class Utils2DException(Exception):
    """
    """


class Vector2D:
    def __init__(self, x: float = 0, y: float = 0):
            self._x = x
            self._y = y

    @classmethod
    def from_tuple(cls, x_y: Tuple[float,float]):
        return cls(x=x_y[0], y=x_y[1])
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    @property
    def vector(self):
        return np.array([self._x, self._y])

    def update(self, x: float, y: float):
            self._x = x
            self._y = y


class Force(Vector2D):
    """
    """


class Speed(Vector2D):
    """
    """


class Position(Vector2D):
    """
    """
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed_list = [Speed(0, 0)]
        self.force_list = [Force(0, 0)]
        self.gravity = Force(0, gravity)
        self._direction_x = 0
        self._direction_y = 0

    @property
    def dir_x(self):
        return self._direction_x

    @property
    def dir_y(self):
        return self._direction_y

    def update_speed(self, speed_list: List[Speed]):
        self.speed_list = speed_list

    def append_speed(self, speed: Speed):
        self.speed_list.append(speed)

    def clear_speed(self):
        self.speed_list = [Speed(0, 0)]
    
    def update_force(self, force_list: List[Force]):
        self.force_list = force_list

    def append_force(self, force: Force):
        self.force_list.append(force)

    def append_forces(self, forces: List[Force]):
        self.force_list.extend(forces)

    def clear_force_x(self):
        for force in self.force_list:
            force._x = 0

    def clear_force_y(self):
        for force in self.force_list:
            force._y = 0

    def get_speed(self):
        return np.sum([speed.vector for speed in self.speed_list], axis = 0)

    def get_force(self):
        return np.sum([force.vector for force in self.force_list], axis = 0)
    
    def increment_position(self):
        speed = self.get_speed()
        force = self.get_force()
        # vit = [force, speed]
        # increment_pos = vit[0] * dt / 2 + vit[1] * dt
        increment_pos = force / 2 + speed
        pos = self.vector + increment_pos
        self._direction_x = increment_pos[0]
        self._direction_y = increment_pos[1]
        return pos
        self._x = pos[0]
        self._y = pos[1]


class Action:
    """
    """
    def __init__(self, action_name: str, vector_list: List[Vector2]):
        self.action_name = action_name
        self.action_list: List[Vector2] = vector_list
        self.active_action_list: List[Vector2] = [Vector2(0, 0)]
        self.was_triggered = False
    
    def trigger(self):
        self.was_triggered = True
        self.active_action_list = self.action_list.copy()
    
    def load(self):
        self.was_triggered = False
        self.active_action_list = self.action_list.copy()
    
    def unload(self):
        self.active_action_list = [Vector2(0, 0)]

    def play(self):
        if not self.was_triggered:
            return self.active_action_list[0]
        if self.active_action_list:
            play_force: Vector2 = self.active_action_list.pop(0)
            return play_force
        return Vector2(0, 0)
        if self.active_action_list:
            play_force: Vector2 = self.active_action_list.pop(0)
            return play_force
        return Vector2(0, 0)
