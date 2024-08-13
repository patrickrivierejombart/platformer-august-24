# main.py POC
import pygame
import sys
from settings import *
from ENVIRONMENT.elements.tilemap import Tilemap
from ENVIRONMENT.camera import Camera, Follow
from utils.texture_utils import load_image, load_images
from ENTITY.player.player import Player


class GAME_NAME_HERE:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Game POC")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.display = pygame.Surface((TILE_DISPLAY_WIDTH, TILE_DISPLAY_HEIGHT), pygame.SRCALPHA)
        self.character_layer = pygame.Surface((CHARACTER_DISPLAY_WIDTH, CHARACTER_DISPLAY_HEIGHT), pygame.SRCALPHA)
        
        self.clock = pygame.time.Clock()

        self.player_event = False

        self.assets = {
            'sand': load_images('terrain/sand'),
            'sand_decor': load_images('terrain/sand_decor'),
            'background': load_image('background.jpg')
        }

        self.player = Player(
            (250, 200), 
            4, 
            (PLAYER_SIZE_X, PLAYER_SIZE_Y), 
            "assets/textures/player/",
            animation_speed=0.08
        )

        self.tilemap = Tilemap(self, tile_size=TILE_SIZE)
        self.tilemap.load("assets/level_saves/level-1_map.json")

        self.camera = Camera()
        self.camera.setmethod(Follow(self.player, self.display))

    def run(self):
        while True:
            self.display.fill((0, 0, 0), (0, 0, WIDTH//4, HEIGHT//4))
            self.character_layer.fill((0, 0, 0, 0), (0, 0, WIDTH//2, HEIGHT//2))

            self.camera.scroll()
            render_scroll = self.camera.render_scroll()

            self.tilemap.render(self.display, offset=render_scroll)

            self.player.update(self.tilemap, self.player_event, self.display, offset=render_scroll)
            self.player.render(self.character_layer, offset=render_scroll)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player_event = "left"
                    if event.key == pygame.K_RIGHT:
                        self.player_event = "right"
                    if event.key == pygame.K_SPACE:
                        self.player_event = "space"
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.player_event = "no_left"
                    if event.key == pygame.K_RIGHT:
                        self.player_event = "no_right" 
                    if event.key == pygame.K_SPACE:
                        self.player_event = "no_space"
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            self.screen.blit(pygame.transform.scale(self.character_layer, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    play = GAME_NAME_HERE().run()
