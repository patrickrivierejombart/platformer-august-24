import pygame
vec = pygame.math.Vector2
from settings import WIDTH, HEIGHT
from abc import ABC, abstractmethod


class Camera:
    def __init__(self, player):
        self.player = player
        self.offset_float_x = 0
        self.offset_float_y = 0
        self.offset = vec(int(self.offset_float_x), int(self.offset_float_y))
        self.DISPLAY_W, self.DISPLAY_H = WIDTH, HEIGHT
        self.CONST = vec(0, 0)
        # self.CONST = vec(-self.DISPLAY_W / 2 + player.rect.w / 2, -self.player.rect.y + 20)
    
    def setmethod(self, method):
        self.method = method

    def scroll(self):
        self.method.scroll()


class CamScroll(ABC):
    def __init__(self, camera, player):
        self.camera = camera
        self.player = player

    @abstractmethod
    def scroll(self):
        pass


class Follow(CamScroll):
    def __init__(self, camera, player):
        CamScroll.__init__(self, camera, player)
    
    def scroll(self):
        self.camera.offset_float_x = (self.player.position_float_x - self.player.rect.x + self.camera.CONST.x)
        self.camera.offset_float_y = (self.player.position_float_y - self.player.rect.y + self.camera.CONST.y)
        self.camera.offset.x, self.camera.offset.y = int(self.camera.offset_float_x), int(self.camera.offset_float_y)
