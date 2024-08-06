from typing import List, Tuple
import numpy as np


class Utils2DException(Exception):
    """
    """


class Vector2D:
    def __init__(self, x = 0, y = 0):
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
        self.speed_list = None
        self.force_list = None

    def update_speed(self, speed_list: List[Speed]):
        self.speed_list = speed_list
    
    def update_force(self, force_list: List[Force]):
        self.force_list = force_list
    
    def increment_position(self, dt):
        vit = np.sum([force.vector for force in self.force_list], axis = 0) * dt + np.sum([speed.vector for speed in self.speed_list], axis = 0)
        pos = self.vector + vit * dt / 2
        self._x = pos[0]
        self._y = pos[1]


class Action:
    """
    """
    def __init__(self, action_name: str, vector_list: List[Force]):
        self.action_name = action_name
        self.action_list: List[Force] = vector_list
        self.active_action_list: List[Force] = list()
    
    def trigger(self):
        if not self.active_action_list:
            self.active_action_list = self.action_list

    def play(self):
        if self.active_action_list:
            play_force: Force = self.active_action_list.pop(0)
            return play_force
