# main.py POC
import pygame
import sys
from settings import *
from ENVIRONMENT.world import World
from ENVIRONMENT.map_handler import Level1


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game POC")


class GAME_NAME_HERE:
    def __init__(self, screen: pygame.Surface, width, height):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.player_event = False
        self.bg_img = pygame.image.load(BG_IMG)
        self.bg_img = pygame.transform.scale(self.bg_img, (width, height))
    
    def main(self):
        world = World(level=Level1(), screen=self.screen)
        while True:
            self.screen.blit(self.bg_img, (0, 0))
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
                    self.player_event = False
            world.update(self.player_event)
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    play = GAME_NAME_HERE(screen, WIDTH, HEIGHT)
    play.main()
