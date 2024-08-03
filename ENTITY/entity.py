# Importing math.py
import math
from turtle import pos

# Class for all entities

class Entity():

    class Direction():
        def __init__(self, x, y):
            self.x = x
            self.y = y
        @property
        def x(self) -> int:
            return self.x
        @property
        def y(self) -> int:
            return self.y
        def update(self, x, y):
            self.x = x
            self.y = y
        def updateX(self, x: int):
            self.x = x
        def updateY(self, y: int):
            self.y = y
        def right(self):
            self.x = 1
        def left(self):
            self.x = -1
        def up(self):
            self.y = 1
        def down(self):
            self.y = -1
        def inactive(self):
            self.x = 0
            self.y = 0

    def __init__(self, hp: int, lives: int, object_size: list, pos: list):
        self.hp = hp
        self.lives = lives
        self.direction = self.Direction(0,0)
        self.object_size = object_size
        self.pos = pos
    def is_in_hitbox(self, point: tuple):
        # x2/a2 + y2/b2 = 1 is the formula of the bounderies of an ellipse
        # x2/a2 + y2/b2 <= 1 is the formula of the inside of an ellipse
        # [x,y] -> position of the point we want to check
        # a -> half of the longest side of the ellipse
        # b -> half of the shortest side of the ellipse
        pointX = point[0]-pos[0]
        pointY = point[1]-pos[1]
        if ((pointX**2)/(self.object_size[1]**2))+((pointY**2)/(self.object_size[0]**2)) <= 1:
            return True
        else: return False
    def update(self):
        pass
    def dynamics(self):
        # Not in accord with map update - To edit
        return {"x": self.direction.x, "y": self.direction.y}
