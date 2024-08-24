import pygame
from pygame import Rect
from utils.texture_utils import import_sprite
from typing import Tuple, Literal
from settings import GRAVITY, DT, PLAYER_WALK_SPEED, PLAYER_JUMP_SPEED, CHARACTER_STATUS_DELAY, TILE_SIZE
from ENVIRONMENT.elements.collisions import CollisionMap
from math import cos, sin


class PhysicsEntity:
    def __init__(self, 
                 position: Tuple[int, int],
                 lives: int, 
                 base_size: Tuple[int, int],
                 sprite_path: str,
                 animation_speed: float = 0.15,
                 base_hp: int = 5,
                 base_speed: int = PLAYER_WALK_SPEED,
                 base_jump: int = PLAYER_JUMP_SPEED,
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
        self.previous_status = "idle"
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        # update time
        self.previous_time = 0
        # delays
        self._universal_delay = 0
        self._status_delay = CHARACTER_STATUS_DELAY
    
    def rect(self):
        return pygame.Rect(self.position_int[0], self.position_int[1], self.size[0], self.size[1])
    
    def update(self, collision_map: CollisionMap, event, surf, offset):
        self._universal_delay += 1
        self._act(event)
        self.collisions = {'up': False, 'down': False, 'right': False, 'left': False}
        
        # delta time
        current_time = pygame.time.get_ticks() / 1000
        delta_time = current_time - self.previous_time
        self.previous_time = current_time
        _dt = delta_time
        if delta_time > DT:
            _dt = DT

        self.velocity_float[0] = round(self._approachX(self.velocity_goal_int[0], self.velocity_float[0], _dt), 2)
        self.velocity_float[1] = round(self._approachY(self.velocity_goal_int[1], self.velocity_float[1], _dt), 2)
        frame_movement = (round(self.velocity_float[0] * _dt, 2), round(self.velocity_float[1] * _dt, 2))
        self.position_float[0] += frame_movement[0]
        self.position_float[1] += frame_movement[1]

        self.position_int[0] = int(self.position_float[0])
        entity_rect = self.rect()

        for rect in collision_map.physics_rects_around(self.position_int)['wall']:
            r_surf = pygame.Surface((rect.w, rect.h))
            r_surf.fill((0, 255, 0))
            surf.blit(r_surf, (rect.x - offset[0], rect.y - offset[1]))
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
        for rect in collision_map.physics_rects_around(self.position_float)['ground']:
            r_surf = pygame.Surface((rect.w, rect.h))
            r_surf.fill((0, 255, 0))
            surf.blit(r_surf, (rect.x - offset[0], rect.y - offset[1]))
            if entity_rect.colliderect(rect):
                if frame_movement[1] > 0:
                    entity_rect.bottom = rect.top
                    self.collisions['down'] = True
                if frame_movement[1] < 0:
                    # TODO : Implement later a way to handle ceilings without phasing through ground (differentiate ground and ceiling)
                    # entity_rect.top = rect.bottom
                    self.collisions['up'] = True
                self.position_float[1] = entity_rect.y
                self.position_int[1] = entity_rect.y
        for rect in collision_map.physics_rects_around(self.position_float)['jump_through']:
            if entity_rect.colliderect(rect) and frame_movement[1] > 0 and self._raycast_jump_through(0, 1, tile_size=collision_map.tile_size, collision_rect=rect):
                entity_rect.bottom = rect.top
                self.collisions['down'] = True
                self.position_float[1] = entity_rect.y
                self.position_int[1] = entity_rect.y
        
        self.velocity_goal_float[1] = self.velocity_goal_float[1] + GRAVITY * _dt
        self.velocity_goal_int[0] = int(self.velocity_goal_float[0])
        self.velocity_goal_int[1] = int(self.velocity_goal_float[1])
        
        if self.collisions['down'] or self.collisions['up']:
            self.velocity_goal_float[1] = 0
            self.velocity_float[1] = 0
        
        if self._universal_delay % self._status_delay == 0:
            self._get_status(collision_map=collision_map)
        self._animate()

        
    def render(self, surf, offset=(0, 0)):
        posX = self.position_int[0] - offset[0] #  tile_to_character_ratio * self.position_int[0]
        posY = self.position_int[1] - offset[1] #  tile_to_character_ratio * self.position_int[1]
        surf.blit(self.image, (posX, posY))

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

    def _get_status(self, collision_map: CollisionMap):
        """DEFINE IN HERITAGE : use self.status
        when going from one status to the other, reset self.frame_index"""
    
    def _animate(self):
        # Animate the entity sprite
        if self.previous_status != self.status:
            self.previous_status = self.status
            self.frame_index = 0
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
    
    def _raycast_jump_through(self, min_depth, depth, tile_size: int, collision_rect: Rect):
        POS_RATIO = tile_size
        depth = min(POS_RATIO*3, depth)  # depth cannot go over 3 tiles (limit load on cpu)
        origin_1 = [0, 0]
        origin_2 = [0, 0]
        origin = [0, 0]

        origin_1 = self.rect().right, self.rect().bottom
        origin_2 = self.rect().left, self.rect().bottom
        origin = self.rect().centerx, self.rect().bottom

        x_const = cos(-90)
        y_const = -sin(-90)

        x_left = collision_rect.x
        x_right = x_left + collision_rect.width
        y_top = collision_rect.y
        y_bottom = y_top + collision_rect.height

        print('x_left: ', x_left, ', x_right: ', x_right)
        print('y_top: ', y_top, ', y_bottom: ', y_bottom)

        for distance in range(min_depth, depth+1):
            x = int((origin[0] + x_const * distance))
            y = int((origin[1] + y_const * distance))
            x_1 = int((origin_1[0] + x_const * distance))
            y_1 = int((origin_1[1] + y_const * distance))
            x_2 = int((origin_2[0] + x_const * distance))
            y_2 = int((origin_2[1] + y_const * distance))

            print('x, y: ', (x, y))
            #loc = str(x) + ';' + str(y), str(x_1) + ';' + str(y_1), str(x_2) + ';' + str(y_2)
            #collision_loc = [collision_map.ground[loc_i]['pos'] for loc_i in loc if loc_i in collision_map.ground]
            #collision_loc.extend([collision_map.wall[loc_i]['pos'] for loc_i in loc if loc_i in collision_map.wall])
            loc = (x,y), (x_1,y_1), (x_2,y_2)
            is_x_collision = [(loc_i[0], loc_i[1]) for loc_i in loc if x_left < loc_i[0] < x_right]
            is_y_collision = [(loc_i[0], loc_i[1]) for loc_i in loc if y_top < loc_i[1] < y_bottom]
            if len(is_x_collision) > 0 and len(is_y_collision) == 3:
                return loc
        return False
    
    def _raycast(self, angle, min_depth, depth, collision_map: CollisionMap, logic: Literal['or', 'and']):
        POS_RATIO = collision_map.tile_size
        depth = min(POS_RATIO*3, depth)  # depth cannot go over 3 tiles (limit load on cpu)
        origin_1 = [0, 0]
        origin_2 = [0, 0]
        origin = [0, 0]
        if -45 < angle <= 45:
            origin_1 = self.rect().right, self.rect().top
            origin_2 = self.rect().right, self.rect().bottom
            origin = self.rect().right, self.rect().centery
        elif 45 < angle <= 135:
            origin_1 = self.rect().left, self.rect().top
            origin_2 = self.rect().right, self.rect().top
            origin = self.rect().centerx, self.rect().top
        elif 135 < angle  <= 180 or -180 < angle <= -135:
            origin_1 = self.rect().left, self.rect().bottom
            origin_2 = self.rect().left, self.rect().top
            origin = self.rect().left, self.rect().centery
        else:
            origin_1 = self.rect().right, self.rect().bottom
            origin_2 = self.rect().left, self.rect().bottom
            origin = self.rect().centerx, self.rect().bottom
        x_const = cos(angle)
        y_const = -sin(angle)
        for distance in range(min_depth, depth+1):
            x = int((origin[0] + x_const * distance) // POS_RATIO)
            y = int((origin[1] + y_const * distance) // POS_RATIO)
            x_1 = int((origin_1[0] + x_const * distance) // POS_RATIO)
            y_1 = int((origin_1[1] + y_const * distance) // POS_RATIO)
            x_2 = int((origin_2[0] + x_const * distance) // POS_RATIO)
            y_2 = int((origin_2[1] + y_const * distance) // POS_RATIO)
            loc = str(x) + ';' + str(y), str(x_1) + ';' + str(y_1), str(x_2) + ';' + str(y_2)
            collision_loc = [collision_map.ground[loc_i]['pos'] for loc_i in loc if loc_i in collision_map.ground]
            collision_loc.extend([collision_map.wall[loc_i]['pos'] for loc_i in loc if loc_i in collision_map.wall])
            collision_loc.extend([collision_map.jump_through[loc_i]['pos'] for loc_i in loc if loc_i in collision_map.jump_through])
            if logic == 'or' and len(collision_loc) > 0:
                return collision_loc
            if logic == 'and' and len(collision_loc) == 3:
                return collision_loc
        return False
