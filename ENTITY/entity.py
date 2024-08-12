import pygame
from utils.texture_utils import import_sprite
from typing import Tuple
from settings import gravity, dt, player_walk_speed, player_jump_speed, tile_to_character_ratio, tile_size
from ENVIRONMENT.elements.tilemap import Tilemap
from math import cos, sin


class PhysicsEntity:
    def __init__(self, 
                 position: Tuple[int, int],
                 lives: int, 
                 base_size: Tuple[int, int],
                 sprite_path: str,
                 animation_speed: float = 0.15,
                 base_hp: int = 5,
                 base_speed: int = player_walk_speed,
                 base_jump: int = player_jump_speed,
                 base_strength: int = 5,
                 base_intelligence: int = 5,
                 base_defense: int = 5,
                 base_attack: int = 5
                 ):
        self._import_character_assets(sprite_path)
        # position
        self.position_int = list(position)
        self.position_float = [float(self.position_int[0]), float(self.position_int[1])]
        self.velocity_float = [0.0, 0.0]
        self.velocity_goal_int = [0, 0]
        self.velocity_goal_float = [0.0, 0.0]
        # sprite
        self.frame_index = 0
        self.animation_speed = animation_speed
        self.image = self.animations["idle"][self.frame_index].convert_alpha()
        self.base_size = base_size
        self.size = [self.base_size[0], self.base_size[1]]
        self.moving_left = False
        # player movement
        self.moving_x = [False, False]
        self.moving_y = [False, False]
        # player stats
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
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        # update time
        self.previous_time = 0
    
    def rect(self):
        return pygame.Rect(self.position_int[0], self.position_int[1], self.size[0] // tile_to_character_ratio, self.size[1] // tile_to_character_ratio)
    
    def update(self, tilemap: Tilemap, event, surf, offset):
        self._act(event)
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        # delta time
        current_time = pygame.time.get_ticks() / 1000
        delta_time = current_time - self.previous_time
        self.previous_time = current_time
        _dt = delta_time
        if delta_time > dt:
            _dt = dt

        self.velocity_float[0] = round(self._approachX(self.velocity_goal_int[0], self.velocity_float[0], _dt), 2)
        self.velocity_float[1] = round(self._approachY(self.velocity_goal_int[1], self.velocity_float[1], _dt), 2)
        frame_movement = (round(self.velocity_float[0] * _dt, 2), round(self.velocity_float[1] * _dt, 2))
        self.position_float[0] += frame_movement[0]
        self.position_float[1] += frame_movement[1]

        self.position_int[0] = int(self.position_float[0])
        entity_rect = self.rect()
        for rect in tilemap.physics_rects_around(self.position_int):
            if entity_rect.colliderect(rect):
                if frame_movement[0] > 0:
                    entity_rect.right = rect.left
                    self.collisions['right'] = True
                if frame_movement[0] < 0:
                    entity_rect.left = rect.right
                    self.collisions['left'] = True
                self.position_float[0] = entity_rect.x
                self.position_int[0] = entity_rect.x
        
        self.position_int[1] = int(self.position_float[1])
        entity_rect = self.rect()
        e_surf = pygame.Surface((entity_rect.w, entity_rect.h))
        e_surf.fill((255, 0, 0))
        e_surf.fill((0, 0, 0, 0), e_surf.get_rect().inflate(-2, 2))
        surf.blit(e_surf, (entity_rect.x - offset[0], entity_rect.y - offset[1]))
        for rect in tilemap.physics_rects_around(self.position_float):
            r_surf = pygame.Surface((rect.w, rect.h))
            r_surf.fill((0, 255, 0))
            surf.blit(r_surf, (rect.x - offset[0], rect.y - offset[1]))
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.position_float[1] = entity_rect.y
                self.position_int[1] = entity_rect.y
        
        self.velocity_goal_float[1] = self.velocity_goal_float[1] + gravity * _dt
        self.velocity_goal_int[0] = int(self.velocity_goal_float[0])
        self.velocity_goal_int[1] = int(self.velocity_goal_float[1])
        
        if self.collisions['down'] or self.collisions['up']:
            self.velocity_goal_float[1] = 0
            self.velocity_float[1] = 0
        
        self._get_status(tilemap=tilemap)
        self._animate()

        
    def render(self, surf, offset=(0, 0)):
        posX = self.position_int[0] - offset[0] #  tile_to_character_ratio * self.position_int[0]
        posY = self.position_int[1] - offset[1] #  tile_to_character_ratio * self.position_int[1]
        surf.blit(self.image, (posX * tile_to_character_ratio, posY * tile_to_character_ratio))

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

    def _act(self, event):
        """DEFINE IN HERITAGE"""
    
    def _approachX(self, goal: float, current: float, _dt: float):
        # Interpolate velocity towards a velocity_goal along X
        _dt *= 2000
        diff = goal - current
        if diff > _dt:
            return current + _dt
        if diff < -_dt:
            return current - _dt
        return goal

    def _approachY(self, goal: float, current: float, _dt: float):
        # Interpolate velocity towards a velocity_goal along Y
        _dt *= 10000
        diff = goal - current
        if diff > _dt:
            return current + _dt
        if diff < -_dt:
            return current - _dt
        return goal

    def _get_status(self, tilemap: Tilemap):
        """DEFINE IN HERITAGE : use self.status
        when going from one status to the other, reset self.frame_index"""
    
    def _animate(self):
        # Animate the entity sprite
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        image = pygame.transform.scale(image, (self.size[0], self.size[1]))
        if self.moving_left:
            flipped_image = pygame.transform.flip(image, True, False)
            self.image = flipped_image
        else:
            self.image = image
    
    def _raycast(self, angle, min_depth, depth, tilemap: Tilemap):
        depth = min(tile_size*3, depth)  # depth cannot go over 3 tiles (limit load on cpu)
        if -45 < angle <= 45:
            origin = self.rect().right, self.rect().centery
        elif 45 < angle <= 135:
            origin = self.rect().centerx, self.rect().top
        elif 135 < angle  <= 180 or -180 < angle <= -135:
            origin = self.rect().left, self.rect().centery
        else:
            origin = self.rect().centerx, self.rect().bottom
        x_const = cos(angle)
        y_const = -sin(angle)
        for distance in range(min_depth, depth+1):
            x = int(origin[0] + x_const * distance) // tile_size
            y = int(origin[1] + y_const * distance) // tile_size
            loc = str(x) + ';' + str(y)
            if loc in tilemap.tilemap:
                return tilemap.tilemap[loc]['pos']
        return False
