import pygame
from settings import BG_IMG
from pygame.math import Vector2


class Goal(pygame.sprite.Sprite):  # add sprite path
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.image.load(BG_IMG)
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=pos)
        self.position = Vector2(pos[0], pos[1])
    
    def update(self, x_shift):
        self.rect.x += x_shift
