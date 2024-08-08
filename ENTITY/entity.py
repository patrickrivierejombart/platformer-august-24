import pygame
from utils.sprite_utils import import_sprite
from utils.utils_2d import Action
from pygame.math import Vector2
from typing import Tuple, Dict
from settings import gravity, dt


class Entity(pygame.sprite.Sprite):
    def __init__(self, 
                 position: Vector2,
                 lives: int, 
                 base_size: Tuple[int, int],
                 sprite_path: str,
                 action_list: Dict[str, Action],
                 animation_speed: float = 0.15,
                 base_hp: int = 5,
                 base_speed: int = 5,
                 base_jump: int = 18,
                 base_strength: int = 5,
                 base_intelligence: int = 5,
                 base_defense: int = 5,
                 base_attack: int = 5
                 ):
        super().__init__()
        # position
        self.position = position
        self.velocity = Vector2(0, 0)
        self.velocity_float_x: float = 0
        self.velocity_float_y: float = 0
        self.gravity = Vector2(0, gravity)
        self.velocity_goal = Vector2(0, 0)
        # sprite
        self._import_character_assets(sprite_path)
        self.frame_index = 0
        self.animation_speed = animation_speed
        self.image = self.animations["idle"][self.frame_index]
        self.rect = self.image.get_rect(topleft=position)
        self.mask = pygame.mask.from_surface(self.image)
        self.base_size = base_size
        # player actions
        self.action_list = action_list
        # player movement
        self.direction = pygame.math.Vector2(0, 0)
        self.base_hp = base_hp
        self.hp = base_hp
        self.base_speed = base_speed
        self.speed = base_speed
        self.base_jump = base_jump
        self.jump = base_jump
        self.base_strength = base_strength
        self.base_intelligence = base_intelligence
        self.base_defense = base_defense
        self.base_attack = base_attack
        # player status
        self.lives = lives
        self.status = "idle"
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
    
    def _import_character_assets(self, sprite_path):
        """REDEFINE IN HERITAGE : use self.animations"""
        character_path = sprite_path
        self.animations = {
            "idle": [],
            "walk": [],
            "hit": [],
            "attack": [],
            "dead": [],
            "revive": []
        }
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_sprite(full_path)

    def _animate(self):
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        image = pygame.transform.scale(image, (self.base_size[0], self.base_size[1]))
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
        # set the rect (boundary)
        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright=self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom=self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright=self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(bottomleft=self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop=self.rect.midtop)

    def take_damage(self, attack):
        self.hp -= attack**2 / self.base_defense
        if self.hp < 1:
            self.lives -= 1
        if self.lives < 1:
            self.status = "dead"
        elif self.lives > 0:
            self.status = "revive"
            self.hp = self.base_hp

    def _get_status(self):
        """DEFINE IN HERITAGE : use self.status
        when going from one status to the other, reset self.frame_index"""

    def _act(self, event):
        """DEFINE IN HERITAGE : use self.action_list"""

    def _approachX(self, goal: float, current: float):
        _dt = dt
        _dt *= self.speed  # * 40 / 100
        diff = goal - current
        if diff > _dt:
            return current + _dt
        if diff < -_dt:
            return current - _dt
        return goal

    def _approachY(self, goal: float, current: float):
        _dt = dt
        _dt *= self.base_jump  # * 40 / 100
        diff = goal - current
        if diff > _dt:
            return current + _dt
        if diff < -_dt:
            return current - _dt
        return goal

    def update(self, event, x_shift):
        self._act(event)
        self.velocity_float_x = round(self._approachX(self.velocity_goal.x, self.velocity_float_x), 2)
        self.velocity_float_y = round(self._approachY(self.velocity_goal.y, self.velocity_float_y), 2)
        self.velocity.x, self.velocity.y = int(self.velocity_float_x), int(self.velocity_float_y)
        self.rect.x += x_shift 
        self._get_status()
        self._animate()
