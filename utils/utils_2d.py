from typing import List
import numpy as np


class Utils2DException(Exception):
    """
    """


class Vector2D:
    def __init__(self, x, y):
        self._x = x
        self._y = y
    
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
        vit = np.sum([force.vector for force in self.force_list], axis = 0) * dt
        pos = self.vector + vit * dt / 2
        self._x = pos[0]
        self._y = pos[1]
