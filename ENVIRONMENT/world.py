import pygame
from settings import tile_size, WIDTH
from ENVIRONMENT.elements.tile import Tile
from ENVIRONMENT.elements.trap import Trap
from ENVIRONMENT.elements.goal import Goal
from GUI.game import Game
from ENTITY.player.player import Player
from ENVIRONMENT.map_handler import MapHandler, Level
from utils import utils_2d as utils


class World:
    def __init__(self, level: Level, screen: pygame.Surface):
        self.screen = screen
        self.map_handler = MapHandler()
        self.map_handler.load_level(level=level)
        self.world_data = self.map_handler.level_map.map
        self._setup_world(self.map_handler.level_map.map)
        self.world_shift = 0
        self.current_x = 0
        self.gravity = 0.7
        self.game = Game(self.screen)
    
    def _setup_world(self, layout):
        self.tiles = pygame.sprite.Group()
        self.traps = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x, y = col_index * tile_size, row_index * tile_size
                if cell == self.map_handler['tile']:
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                elif cell == self.map_handler['trap']:
                    trap = Trap((x + (tile_size // 4), y + (tile_size // 4)), tile_size // 2)
                    self.traps.add(trap)
                elif cell == self.map_handler['player']:
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)
                elif cell == self.map_handler['goal']:
                    goal_sprite = Goal((x, y), tile_size)
                    self.goal.add(goal_sprite)
    
    
    def _scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x
        if player_x < WIDTH // 3 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > WIDTH - (WIDTH // 3) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 3
    
    def _apply_gravity(self, player):
        player.direction.y += self.gravity
        player.rect.y += player.direction.y

    def _horizontal_movement_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def _vertical_movement_collision(self):
        player = self.player.sprite
        self._apply_gravity(player)
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def _handle_traps(self):
        player = self.player.sprite
        for sprite in self.traps.sprites():
            if sprite.rect.colliderect(player.rect):
                # Go on the right to avoid continuous collision with trap
                if player.direction.x < 0 or player.direction.y > 0:
                    player.rect.x += tile_size
                # Go on the left to avoid continuous collision with trap
                elif player.direction.x > 0 or player.direction.y > 0:
                    player.rect.x -= tile_size
                player.life -= 1

    def update(self, player_event):
        # tile
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.screen)
        # trap
        self.traps.update(self.world_shift)
        self.traps.draw(self.screen)
        # goal
        self.goal.update(self.world_shift)
        self.goal.draw(self.screen)
        self._scroll_x()
        # player
        self._horizontal_movement_collision()
        self._vertical_movement_collision()
        self._handle_traps()
        self.player.update(player_event)
        self.game.show_life(self.player.sprite)
        self.player.draw(self.screen)
        self.game.game_state(self.player.sprite, self.goal.sprite)