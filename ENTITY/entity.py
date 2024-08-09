import pygame
from utils.sprite_utils import import_sprite
from pygame.math import Vector2
from typing import Tuple
from settings import gravity, dt


class Entity(pygame.sprite.Sprite):
    def __init__(self, 
                 position: Vector2,
                 lives: int, 
                 base_size: Tuple[int, int],
                 sprite_path: str,
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
        self.position_float_x = position.x
        self.position_float_y = position.y
        self.velocity_float_x: float = 0
        self.velocity_float_y: float = 0
        self.gravity = gravity
        self.velocity_goal = Vector2(0, 0)
        self.velocity_goal_float_x = 0
        self.velocity_goal_float_y = 0
        # sprite
        self._import_character_assets(sprite_path)
        self.frame_index = 0
        self.animation_speed = animation_speed
        self.image = self.animations["idle"][self.frame_index].convert_alpha()
        self.rect = self.image.get_rect(topleft=position)
        self.mask = pygame.mask.from_surface(self.image)
        self.base_size = base_size
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
        # update time
        self.previous_time = 0
    
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
        # Animate the entity sprite
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
        # Deal damage to the entity
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
        """DEFINE IN HERITAGE"""

    def _approachX(self, goal: float, current: float, _dt: float):
        # Interpolate velocity towards a velocity_goal along X
        _dt *= 80
        diff = goal - current
        if diff > _dt:
            return current + _dt
        if diff < -_dt:
            return current - _dt
        return goal

    def _approachY(self, goal: float, current: float, _dt: float):
        # Interpolate velocity towards a velocity_goal along Y
        _dt *= 80
        diff = goal - current
        if diff > _dt:
            return current + _dt
        if diff < -_dt:
            return current - _dt
        return goal

    def update(self, event):
        current_time = pygame.time.get_ticks() / 1000
        delta_time = current_time - self.previous_time
        self.previous_time = current_time
        _dt = delta_time
        if delta_time > dt:
            _dt = dt
        # Update entity position and velocity : operate active actions
        self._act(event)
        self.velocity_float_x = round(self._approachX(self.velocity_goal.x, self.velocity_float_x, _dt), 2)
        self.velocity_float_y = round(self._approachY(self.velocity_goal.y, self.velocity_float_y, _dt), 2)
        self.position_float_x += round(self.velocity_float_x * _dt, 2)
        self.position_float_y += round(self.velocity_float_y * _dt, 2)
        self.velocity_goal_float_y += self.gravity * _dt
        self.velocity_goal.update(int(self.velocity_goal_float_x), int(self.velocity_goal_float_y))
        # self.velocity.x, self.velocity.y = int(self.velocity_float_x), int(self.velocity_float_y)
        self._get_status()
        self._animate()
        print(self.position_float_y)
