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

    def __init__(self, hp: int, lives: int, object_size: list):
        self.hp = hp
        self.lives = lives
        self.direction = self.Direction(0,0)
        self.hitbox = object_size
    def dynamics(self):
        # Not in accord with map update - To edit
        return {"x": self.direction.x, "y": self.direction.y}