import pygame
from settings import BG_IMG
from utils.utils_2d import Position


class Goal(pygame.sprite.Sprite):
    def __init__(self, pos, size):  # + img_path TODO
        super().__init__()
        self.image = pygame.image.load(BG_IMG)
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=pos)
        self.position = Position(pos[0], pos[1])
    
    def update(self, x_shift, y_shift):
        self.rect.x = self.position.x - x_shift
        self.rect.y = self.position.y - y_shift
