from typing import Literal
from ENVIRONMENT.elements.collisions import CollisionMap
import pygame
from pygame import Surface


class LevelHandle:
    def __init__(self):
        self._level_name = '?'
        self._collision_map = CollisionMap()
        self._level_front_layer = None
    
    def _load_layer(self, path):
        img = pygame.image.load(path).convert()
        img.set_colorkey((0, 0, 0))
        return img

    def load_level(self, level_name: Literal['level-1']):
        self._level_name = level_name
        self._collision_map.load(f"assets/level_saves/{level_name}_collisions.json")
        self._level_front_layer = self._load_layer(f"assets/level_saves/{level_name}_tiles.png")
    
    def render(self, surf: Surface, offset=(0, 0)):
        surf.blit(self.front_layer, (0 - offset[0], 0 - offset[1]))
    
    @property
    def collision_map(self):
        return self._collision_map

    @property
    def front_layer(self):
        return self._level_front_layer
    
    @property
    def level(self):
        return self._level_name
