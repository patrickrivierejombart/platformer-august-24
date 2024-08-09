import pygame
from settings import BG_IMG
from pygame.math import Vector2


class Tile(pygame.sprite.Sprite):  # add sprite path
    def __init__(self, pos, size, img_path):
        super().__init__()
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=pos)
        self.mask = pygame.mask.from_surface(self.image)
        self.position = Vector2(pos[0], pos[1])
    
    def update(self, x_shift, y_shift):
        self.rect.x += x_shift
        self.rect.y += y_shift


class TopTile(Tile):  # add sprite path
    def __init__(self, pos, size):
        super().__init__(pos, size, 'assets/textures/terrain/top_sand.png')

class MidTile(Tile):  # add sprite path
    def __init__(self, pos, size):
        super().__init__(pos, size, 'assets/textures/terrain/mid_sand.png')
