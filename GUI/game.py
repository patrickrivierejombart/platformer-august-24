import pygame
import sys
from GUI.button import Button
from settings import HEIGHT, WIDTH


pygame.font.init()


class Game:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.gameStarted = False
        self.showOptionMenu = False
        self.buttonCountStartMenu = 2
        self.currCountStartMenu = 0
        self.buttonCountOptionMenu = 2
        self.currCountOptionMenu = 0
        
        self.arialFont = pygame.font.SysFont('arial', 40)
        self.font = pygame.font.SysFont('impact', 70)
        self.message_color = pygame.Color("darkorange")
        
        self.startMenu_start_button = Button("Start", self, self.arialFont, "start")
        self.startMenu_quit_button = Button("Quit", self, self.arialFont, "start")
        # self.startMenu_option_button = Button("Options", self, self.arialFont, "start")
        # self.startMenu_sounds_button = Button("Sounds", self, self.arialFont, "start")
        
        self.optionMenu_resume_button = Button("Resume",self, self.arialFont, "options")
        self.optionMenu_quit_button = Button("Quit",self, self.arialFont, "options")
        
        

    def _draw_start_menu(self):
        self.screen.fill((0, 0, 0))
        
        self.startMenu_start_button.displayButton(self.screen)
        self.startMenu_quit_button.displayButton(self.screen)
        # self.startMenu_option_button.displayButton(self.screen)
        # self.startMenu_sounds_button.displayButton(self.screen)
        
        mousePressed = pygame.mouse.get_pressed()
        if(mousePressed[0] == True): 
            print("Left click")
            mousePos = pygame.mouse.get_pos()
            print(mousePos)
            if(self.startMenu_quit_button.isClicked(mousePos)):
                print("Quit button pressed")
                pygame.quit()
                sys.exit()
            if(self.startMenu_start_button.isClicked(mousePos)):
                print("Start button pressed")
                self.gameStarted = True
        if(mousePressed[1] == True): print("Middle click")
        if(mousePressed[2] == True): print("Right click")
        pygame.display.update()
        
    def _draw_option_menu(self):
        self.screen.fill((0, 0, 0))
        
        self.optionMenu_resume_button.displayButton(self.screen)
        self.optionMenu_quit_button.displayButton(self.screen)
        
        mousePressed = pygame.mouse.get_pressed()
        if(mousePressed[0] == True): 
            print("Left click")
            mousePos = pygame.mouse.get_pos()
            print(mousePos)
            if(self.optionMenu_quit_button.isClicked(mousePos)):
                print("Quit button pressed")
                pygame.quit()
                sys.exit()
            if(self.optionMenu_resume_button.isClicked(mousePos)):
                print("Resume button pressed")
                self.showOptionMenu = False
        if(mousePressed[1] == True): print("Middle click")
        if(mousePressed[2] == True): print("Right click")
        pygame.display.update()
        
        
    def show_life(self, player):
        life_size = 30
        img_path = "assets/textures/life/life.png"
        life_image = pygame.image.load(img_path)
        life_image = pygame.transform.scale(life_image, (life_size, life_size))
        indent = 0
        for life in range(player.hp):
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
        if player.hp <= 0 or player.rect.y >= HEIGHT:
            self._game_lose(player)
        elif player.rect.colliderect(goal.rect):
            self._game_win(player)
            
    def startMenu_state(self, screen: pygame.Surface):
        if(self.gameStarted): 
            self.screen = screen
            self.currCountStartMenu = 0
        else: self._draw_start_menu()
        
    def optionMenu_state(self, screen: pygame.Surface):
        if(self.showOptionMenu): self._draw_option_menu()
        else: 
            self.screen = screen
            self.currCountOptionMenu = 0
