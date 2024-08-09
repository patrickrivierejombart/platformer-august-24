import pygame
from settings import tile_size
from ENVIRONMENT.elements.tile import MidTile, TopTile
from ENVIRONMENT.elements.trap import Trap
from ENVIRONMENT.elements.goal import Goal
from GUI.game import Game
from ENTITY.player.player import Player
from ENVIRONMENT.map_handler import MapHandler, Level
from pygame.math import Vector2
from settings import dt, player_size_x, player_size_y
from ENVIRONMENT.camera import *


class World:
    def __init__(self, level: Level, screen: pygame.Surface):
        self.screen = screen
        self.map_handler = MapHandler()
        self.map_handler.load_level(level=level)
        self.world_data = self.map_handler.level_map.map
        self._setup_world(self.map_handler.level_map.map)
        self.world_shift = 0
        self.current_x = 0
        self.game = Game(self.screen)
        self.previous_time = 0
    
    def _setup_world(self, layout):
        self.tiles = pygame.sprite.Group()
        self.traps = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x, y = col_index * tile_size, row_index * tile_size
                if cell == self.map_handler['top_tile']:
                    tile = TopTile((x, y), tile_size)
                    self.tiles.add(tile)
                elif cell == self.map_handler['mid_tile']:
                    tile = MidTile((x, y), tile_size)
                    self.tiles.add(tile)
                elif cell == self.map_handler['trap']:
                    trap = Trap((x + (tile_size // 4), y + (tile_size // 4)), tile_size // 2)
                    self.traps.add(trap)
                elif cell == self.map_handler['player']:
                    player_sprite = Player(Vector2(x, y),
                                               4,
                                               [player_size_x, player_size_y],
                                               "assets/textures/player/"
                                               )
                    self.camera = Camera(player_sprite)
                    self.camera.setmethod(Follow(self.camera, player_sprite))
                    self.player.add(player_sprite)
                elif cell == self.map_handler['goal']:
                    goal_sprite = Goal((x, y), tile_size)
                    self.goal.add(goal_sprite)
    
    def _scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.velocity_float_x
        if player_x < WIDTH // 3 and direction_x < 0:
            self.world_shift = 3
            # player.velocity_float_x = 0
        elif player_x > WIDTH - (WIDTH // 3) and direction_x > 0:
            self.world_shift = -3
            # player.velocity_float_x = 0
        elif direction_x < 0:
            self.world_shift = 3
        elif direction_x > 0:
            self.world_shift = -3
        else:
            self.world_shift = 0
            'self.world_shift = -player.velocity.x * 0.5'  # TODO
    
    def _tile_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.velocity.x * dt
        player.rect.y += player.velocity.y * dt
        player.velocity_goal += player.gravity * dt
        if not pygame.sprite.spritecollide(self.player.sprite, self.tiles, False):
            return
        colliding_tiles = pygame.sprite.spritecollide(self.player.sprite, self.tiles, False, pygame.sprite.collide_mask)
        print(colliding_tiles)
        if not colliding_tiles:
            return
        left_collisions = [tile.rect.right for tile in colliding_tiles if tile.rect.right > player.rect.left]
        right_collisions = [tile.rect.left for tile in colliding_tiles if tile.rect.left < player.rect.right]
        top_collisions = [tile.rect.bottom for tile in colliding_tiles if tile.rect.bottom < player.rect.top]
        bottom_collisions = [tile.rect.top for tile in colliding_tiles if tile.rect.top > player.rect.bottom]
        if player.velocity.x < 0 and left_collisions:
            player.rect.left = left_collisions[0]
            player.velocity.x = 0
            player.velocity_float_x = 0
            player.on_left = True
            self.current_x = player.rect.left
        elif player.velocity.x > 0 and right_collisions:
            player.rect.right = right_collisions[0]
            player.velocity.x = 0
            player.velocity_float_x = 0
            player.on_right = True
            self.current_x = player.rect.right
        elif player.velocity.y > 0 and bottom_collisions:
            player.rect.bottom = bottom_collisions[0]
            player.velocity.y = 0
            player.velocity_float_y = 0
            player.on_ground = True
        elif player.velocity.y < 0 and top_collisions:
            player.rect.top = top_collisions[0]
            player.velocity_float_y = 1
            player.velocity_goal_float_y = 1
            player.on_ceiling = True

    def _horizontal_movement_collision(self):
        player = self.player.sprite
        # player.rect.x += player.velocity.x * dt
        # player.rect.x = int(player.position_float_x)
        if not pygame.sprite.spritecollide(self.player.sprite, self.tiles, False):
            return
        collided = pygame.sprite.spritecollide(self.player.sprite, self.tiles, False, pygame.sprite.collide_mask)
        if not collided:
            return
        if player.velocity_float_x < 0:
            player.position_float_x = collided[0].rect.right
            player.velocity_float_x = 0
            player.on_left = True
        elif player.velocity_float_x > 0:
            player.position_float_x = collided[0].rect.left - tile_size
            player.velocity_float_x = 0
            player.on_right = True
        """
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.velocity.x < 0:
                    player.rect.left = sprite.rect.right
                    player.velocity.x = 0
                    player.velocity_float_x = 0
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.velocity.x > 0:
                    player.rect.right = sprite.rect.left
                    player.velocity.x = 0
                    player.velocity_float_x = 0
                    player.on_right = True
                    self.current_x = player.rect.right
        """
        if player.on_left and (player.rect.left < self.current_x or player.velocity_float_x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.velocity_float_x <= 0):
            player.on_right = False

    def _vertical_movement_collision(self):
        player = self.player.sprite
        if not pygame.sprite.spritecollide(self.player.sprite, self.tiles, False):
            return
        collided = pygame.sprite.spritecollide(self.player.sprite, self.tiles, False, pygame.sprite.collide_mask)
        if not collided:
            return
        if player.velocity_float_y > 0:
            player.position_float_y = collided[0].rect.top - tile_size
            player.velocity_float_y = 0
            player.on_ground = True
        elif player.velocity_float_y < 0:
            player.position_float_y = collided[0].rect.bottom
            player.velocity_float_y = 1
            player.velocity_goal_float_y = 1
            player.on_ceiling = True
        # player.rect.y += player.velocity.y * dt
        # player.rect.y = int(player.position_float_y)
        # player.velocity_goal += player.gravity * dt
        """
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.velocity_float_y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.velocity_float_y = 0
                    player.on_ground = True
                elif player.velocity_float_y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.velocity_float_y = 1
                    player.velocity_goal_float_y = 1
                    player.on_ceiling = True
        """
        if player.on_ground and player.velocity_float_y < 0:
            player.on_ground = False
        if player.on_ceiling and player.velocity_float_y > 0:
            player.on_ceiling = False

    def _handle_traps(self):
        player = self.player.sprite
        for sprite in self.traps.sprites():
            if sprite.rect.colliderect(player.rect):
                # Go on the right to avoid continuous collision with trap
                if player.velocity.x < 0 or player.velocity.y > 0:
                    player.rect.x += tile_size
                # Go on the left to avoid continuous collision with trap
                elif player.velocity.x > 0 or player.velocity.y > 0:
                    player.rect.x -= tile_size
                player.take_damage(1)

    def update(self, player_event):
        # player
        self.player.update(player_event)  # self.camera.offset.y)
        self.camera.scroll()
        print(self.camera.offset)
        # self._tile_movement_collision()
        self.tiles.update(self.camera.offset.x, 0)
        self.traps.update(self.camera.offset.x, 0)
        self.goal.update(self.camera.offset.x, 0)
        self._horizontal_movement_collision()
        self.camera.scroll()
        self.tiles.update(0, self.camera.offset.y)
        self.traps.update(0, self.camera.offset.y)
        self.goal.update(0, self.camera.offset.y)
        self._vertical_movement_collision()
        self.camera.scroll()
        self.tiles.update(self.camera.offset.x, self.camera.offset.y)
        self.traps.update(self.camera.offset.x, self.camera.offset.y)
        self.goal.update(self.camera.offset.x, self.camera.offset.y)
        # tile
        self.tiles.draw(self.screen)
        # trap
        self.traps.draw(self.screen)
        # goal
        self.goal.draw(self.screen)
        # self._handle_traps()
        # self._scroll_x()
        self.game.show_life(self.player.sprite)
        self.player.draw(self.screen)
        self.game.game_state(self.player.sprite, self.goal.sprite)
