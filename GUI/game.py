import pygame
from settings import HEIGHT, WIDTH


pygame.font.init()


class Game:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font = pygame.font.SysFont("impact", 70)
        self.message_color = pygame.Color("darkorange")

    def show_life(self, player):
        life_size = 30
        img_path = "assets/textures/life/life.png"
        life_image = pygame.image.load(img_path)
        life_image = pygame.transform.scale(life_image, (life_size, life_size))
        indent = 0
        for life in range(player.life):
            indent += life_size
            self.screen.blit(life_image, (indent, life_size))

    def _game_lose(self, player):
        player.game_over = True
        message = self.font.render('You Lose...', True, self.message_color)
        self.screen.blit(message, (WIDTH // 3 + 70, 70))

    def _game_win(self, player):
        player.game_over = True
        player.win = True
        message = self.font.render('You Win!!', True, self.message_color)
        self.screen.blit(message, (WIDTH // 3, 70))

    def game_state(self, player, goal):
        if player.life <= 0 or player.rect.y >= HEIGHT:
            self._game_lose(player)
        elif player.rect.colliderect(goal.rect):
            self._game_win(player)
