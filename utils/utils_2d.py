from typing import List
import numpy as np


class Utils2DException(Exception):
    """
    """


class Force:
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


def acceleration(mass, forces: List[Force]) -> Force:
    try:
        assert mass > 0
    except AssertionError:
        raise Utils2DException(f'Mass ({mass}) must be a positive number.')
    impossible_value = -9999
    acc_list = np.sum([force.vector/mass for force in forces], axis=0)
    acc = Force(acc_list[0], acc_list[1]) if len(acc_list) == 2 else impossible_value
    if acc == impossible_value:
        raise Utils2DException('Acceleration calculus failed for an unkown reason.')
    return acc
