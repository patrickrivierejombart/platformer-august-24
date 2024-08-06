import pygame
from settings import tile_size, WIDTH
from ENVIRONMENT.elements.tile import Tile
from ENVIRONMENT.elements.trap import Trap
from ENVIRONMENT.elements.goal import Goal
from GUI.game import Game
from ENTITY.player.player import New_Player
from ENVIRONMENT.map_handler import MapHandler, Level
from utils.utils_2d import Position, Force
from utils.utils_config import read_configured_actions
from settings import gravity


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
                    player_sprite = New_Player(Position(x, y),
                                               1,
                                               [30, 50],
                                               "assets/textures/player/",
                                               read_configured_actions()
                                               )
                    self.player.add(player_sprite)
                elif cell == self.map_handler['goal']:
                    goal_sprite = Goal((x, y), tile_size)
                    self.goal.add(goal_sprite)
    
    def _scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        if player_x < WIDTH // 3 and player.status == "walk" and player.position.dir_x < 0:
            print("Shift left")
            self.world_shift = 8
        elif player_x > WIDTH - (WIDTH // 3) and player.status == "walk" and player.position.dir_x > 0:
            print("Shift right")
            self.world_shift = -8
        else:
            self.world_shift = 0

    def _horizontal_movement_collision(self):
        player = self.player.sprite
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.position.dir_x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                    player.position.clear_speed()
                elif player.position.dir_x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
                    player.position.clear_speed()
        if player.on_left and (player.rect.left < self.current_x or player.position.dir_x > 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or not player.position.dir_x < 0):
            player.on_right = False

    def _vertical_movement_collision(self):
        player = self.player.sprite
        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.position.dir_y >= 0:
                    player.rect.bottom = sprite.rect.top
                    player.position.update_force([Force(0, -gravity)])
                    player.on_ground = True
                elif player.position.dir_y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.position.clear_force()
                    player.on_ceiling = True
        if player.on_ground and player.position.dir_y < 0 or player.position.dir_y > gravity:
            player.on_ground = False
        if player.on_ceiling and player.position.dir_y > 0:
            player.on_ceiling = False

    def _handle_traps(self):
        player = self.player.sprite
        for sprite in self.traps.sprites():
            if sprite.rect.colliderect(player.rect):
                # Go on the right to avoid continuous collision with trap
                if player.position.dir_x < 0 or player.position.dir_y > 0:
                    player.rect.x += tile_size
                    player.position._x += tile_size
                # Go on the left to avoid continuous collision with trap
                elif player.position.dir_x > 0 or player.position.dir_y > 0:
                    player.rect.x -= tile_size
                    player.position._y += tile_size
                player.take_damage(2)

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
