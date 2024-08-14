# main.py POC
import pygame
import sys
from settings import *
from ENVIRONMENT.elements.level_handle import LevelHandle
from ENVIRONMENT.camera import Camera, Follow
from ENTITY.player.player import Player
from GUI.game import Game


class GAME_NAME_HERE:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("Game POC")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.display = pygame.Surface((CHARACTER_DISPLAY_WIDTH, CHARACTER_DISPLAY_HEIGHT), pygame.SRCALPHA)
        
        self.clock = pygame.time.Clock()

        self.player_event = False
        self.game_event = False

        self.player = Player(
            (1, -64), 
            4, 
            (PLAYER_SIZE_X, PLAYER_SIZE_Y), 
            "assets/textures/player/",
            animation_speed=0.08
        )
        
        self.game = Game(self.screen)

        self.level_handle = LevelHandle()
        self.level_handle.load_level('level-1')

        self.camera = Camera()
        self.camera.setmethod(Follow(self.player, self.display))

    def run(self):
        while True:
            self.display.fill((0, 0, 0), (0, 0, CHARACTER_DISPLAY_WIDTH, CHARACTER_DISPLAY_HEIGHT))

            self.camera.scroll()
            render_scroll = self.camera.render_scroll()

            self.level_handle.render(self.display, offset=render_scroll)

            self.player.update(self.level_handle.collision_map, self.player_event, self.display, offset=render_scroll)
            self.player.render(self.display, offset=render_scroll)
            
            

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.player_event = "left"
                        # print("left key down")
                    elif event.key == pygame.K_RIGHT:
                        self.player_event = "right"
                        # print("right key down")
                    elif event.key == pygame.K_SPACE:
                        self.player_event = "space"
                        # print("space key down")
                    elif event.key == pygame.K_ESCAPE:
                        if(self.game.showOptionMenu):
                            self.game_event = "no_option"
                        else:
                            self.game_event = "option"
                            self.game.closedFromButton = False
                        # print("escape key down")
                    elif event.key == pygame.K_y:
                        if(self.game.showStatMenu):
                            self.game_event = "no_stat"
                        else:
                            self.game_event = "stat"
                            self.game.closedFromButton = False
                        # print("y key down")
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.player_event = "no_left"
                        # print("left key up")
                    elif event.key == pygame.K_RIGHT:
                        self.player_event = "no_right" 
                        # print("right key up")
                    elif event.key == pygame.K_SPACE:
                        self.player_event = "no_space"
                        # print("space key up")
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            self.game.update(self.player,self.game_event)
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    play = GAME_NAME_HERE().run()
