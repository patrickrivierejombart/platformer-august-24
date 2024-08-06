from typing import List, Tuple
import numpy as np
from settings import gravity


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

    def clear_force(self):
        self.force_list = [Force(0, 0)]

    def get_speed(self):
        return np.sum([speed.vector for speed in self.speed_list], axis = 0)

    def get_force(self):
        return np.sum([force.vector for force in self.force_list], axis = 0) + self.gravity.vector
    
    def increment_position(self, dt):
        speed = self.get_speed()
        force = self.get_force()
        vit = [force * dt, speed]
        increment_pos = vit[0] * dt / 2 + vit[1] * dt
        pos = self.vector + increment_pos
        self._x = pos[0]
        self._y = pos[1]
        self._direction_x = increment_pos[0]
        self._direction_y = increment_pos[1]


class Action:
    """
    """
    def __init__(self, action_name: str, vector_list: List[Force]):
        self.action_name = action_name
        self.action_list: List[Force] = vector_list
        self.active_action_list: List[Force] = list()
    
    def trigger(self):
        if not self.active_action_list:
            self.active_action_list = self.action_list.copy()

    def play(self):
        if self.active_action_list:
            play_force: Force = self.active_action_list.pop(0)
            return play_force
        return Force(0, 0)
