import pygame
from settings import BG_IMG


class Goal(pygame.sprite.Sprite):
    def __init__(self, pos, size):  # + img_path TODO
        super().__init__()
        self.image = pygame.image.load(BG_IMG)
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=pos)
    
    def update(self, x_shift):
        self.rect.x += x_shift
