
# Class for all entities


class Entity():

    class Speed():
        def __init__(self, x, y):
            self._x = x
            self._y = y

        @property
        def x(self) -> int:
            return self._x
        
        @property
        def y(self) -> int:
            return self._y
        
        def update(self, x: int = None, y: int = None):
            """
                Changes the speed
            """
            if not x: x = self._x
            if not y: y = self._y
            self._x = x
            self._y = y


    class Direction():
        def __init__(self, x, y):
            self._x = x
            self._y = y
        
        @property
        def x(self) -> int:
            return self._x
        
        @property
        def y(self) -> int:
            return self._y
        
        def update(self, x, y):
            self._x = x
            self._y = y

        def updateX(self, x: int):
            self._x = x

        def updateY(self, y: int):
            self._y = y

        def right(self):
            self._x = 1

        def left(self):
            self._x = -1

        def up(self):
            self._y = 1

        def down(self):
            self._y = -1

        def inactive(self):
            self._x = 0
            self._y = 0

    def __init__(self, hp: int, lives: int, object_size: list, pos: list, speed = (0,0)):
        self.hp = hp
        self.lives = lives
        self.direction = self.Direction(0,0)
        self.speed = self.Speed(speed[0], speed[1])
        self.object_size = object_size
        self.pos = pos
        self.vel = [0.0, 0.0]
        self.on_ground = False

    def go_forward(self, speed: int = None):
        if not speed: speed = self.speed.x
        self.pos[0] += speed*self.direction.x

    def update(self, pos: list = None, hp: int = None, lives: int = None, object_size: list = None, speed: tuple = None):
            """
                Makes it possible to edit every important information on the entity
            """
            if not pos: pos = self.pos
            if not hp: hp = self.hp
            if not lives: lives = self.lives
            if not object_size: object_size = self.object_size
            if not speed: speed = self.speed
            self.pos = pos
            self.hp = hp
            self.lives = lives
            self.object_size = object_size
            self.speed = speed
    
    def tick(self, dt: float, gravity: int = 300):
        # Add the velocity to the player's position
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        # Update the vertical movement based on gravity
        if self.on_ground:
            self.vel[1] = 0.0 # Prevent velocity from accumulating when on the ground
        else:
            self.vel[1] += gravity*dt
        
        # Drag (not necessary)
        self.vel[0] -= self.vel[0] / 10.0
        self.vel[1] -= self.vel[1] / 10.0
    
    def jump(self, force: float):
        self.vel[1] -= force

    def is_in_hitbox(self, point: tuple):
        """
            Tells if a certain point is in the players hitbox
        """
        # x2/a2 + y2/b2 = 1 is the formula of the bounderies of an ellipse
        # x2/a2 + y2/b2 <= 1 is the formula of the inside of an ellipse
        # [x,y] -> position of the point we want to check
        # a -> half of the longest side of the ellipse
        # b -> half of the shortest side of the ellipse
        pointX = point[0]-self.pos[0]
        pointY = point[1]-self.pos[1]
        if ((pointX**2)/(self.object_size[1]**2))+((pointY**2)/(self.object_size[0]**2)) <= 1:
            return True
        else: return False

    def is_in_object(self, pos: tuple, point: tuple):
        """
            Tells if a certain point is in the players hitbox in a specific position
        """
        pointX = point[0]-pos[0]
        pointY = point[1]-pos[1]
        if ((pointX**2)/(self.object_size[1]**2))+((pointY**2)/(self.object_size[0]**2)) <= 1:
            return True
        else: return False
    
    def is_not_in_object(self, pos: tuple, point: tuple):
        """
            Tells if a certain point is in the players hitbox in a specific position
        """
        pointX = point[0]-pos[0]
        pointY = point[1]-pos[1]
        if ((pointX**2)/(self.object_size[1]**2))+((pointY**2)/(self.object_size[0]**2)) > 1:
            return True
        else: return False

    def dynamics(self):
        # Not in accord with map update - To edit
        return {
            {"dir_x": self.direction.x, "dir_y": self.direction.y},
            {"speed_x": self.speed.x, "speed_y": self. direction.y},
            {"pos-x": self.pos[0], "pos_y": self.pos[1]},
        }
