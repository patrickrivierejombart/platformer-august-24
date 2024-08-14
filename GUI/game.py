import pygame
import sys
import time
from GUI.button import Button
from GUI.statField import StatField
from GUI.controlField import ControlField
from settings import HEIGHT, WIDTH
from controls import Controls
from GUI.controlMenu import ControlMenu



pygame.font.init()


class Game:
    def __init__(self, screen: pygame.Surface):
        
        self.screen = screen
        self.closedFromButton = False
        
        
        self.arialFont = pygame.font.SysFont('arial', 40)
        self.font = pygame.font.SysFont('impact', 70)
        self.message_color = pygame.Color("darkorange")
        
        # Control menu
        self.showControlMenu = False
        # Start menu
        self.gameStarted = False
        self.buttonCountStartMenu = 3
        self.currCountStartMenu = 0
        self.startMenu_start_button = Button("Start", self, self.arialFont, "start")
        self.startMenu_stats_button = Button("Stats", self, self.arialFont, "start")
        self.startMenu_quit_button = Button("Quit", self, self.arialFont, "start")
        
        # Option menu
        self.showOptionMenu = False
        self.buttonCountOptionMenu = 3
        self.currCountOptionMenu = 0
        self.optionMenu_resume_button = Button("Resume",self, self.arialFont, "options")
        self.optionMenu_control_button = Button("Controls",self, self.arialFont, "options")
        self.optionMenu_quit_button = Button("Quit",self, self.arialFont, "options")
        
        # Stat menu
        self.showStatMenu = False
        self.buttonCountStatMenu = 3
        self.currCountStatMenu = 0
        self.statMenu_resume_button = Button("Resume", self, self.arialFont, "stats")
        self.statMenu_attack_button = StatField("Add attack",self, self.arialFont, "stats")
        self.statMenu_defense_button = StatField("Add defense",self, self.arialFont, "stats")
        
    def menuOpened(self):
        return True if self.showOptionMenu or self.showStatMenu or self.showControlMenu else False
    

    def _draw_start_menu(self):
            self.screen.fill((0, 0, 0))
            
            self.startMenu_start_button.displayButton(self.screen)
            self.startMenu_stats_button.displayButton(self.screen)
            self.startMenu_quit_button.displayButton(self.screen)
            # self.startMenu_sounds_button.displayButton(self.screen)
            print("C Good")
            mousePressed = pygame.mouse.get_pressed()
            if(mousePressed[0] == True): 
                print("Left click")
                mousePos = pygame.mouse.get_pos()
                print(mousePos)
                if(self.startMenu_quit_button.isClicked(mousePos)):
                    print("Quit button pressed")
                    pygame.quit()
                    sys.exit()
                elif(self.startMenu_start_button.isClicked(mousePos)):
                    print("Start button pressed")
                    self.gameStarted = True
                elif(self.startMenu_stats_button.isClicked(mousePos)):
                    print("Stats button pressed")
                    self.showStatMenu = True
            if(mousePressed[1] == True): print("Middle click")
            if(mousePressed[2] == True): print("Right click")
            pygame.display.update()
        
    def _draw_option_menu(self):
        self.screen.fill((0, 0, 0))
        
        self.optionMenu_resume_button.displayButton(self.screen)
        self.optionMenu_control_button.displayButton(self.screen)
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
            if(self.optionMenu_control_button.isClicked(mousePos)):
                print("Controls button pressed")
                self.showOptionMenu = False
                self.closedFromButton = True
                self.showControlMenu = True
            if(self.optionMenu_resume_button.isClicked(mousePos)):
                print("Resume button pressed")
                self.showOptionMenu = False
                self.closedFromButton = True
        if(mousePressed[1] == True): print("Middle click")
        if(mousePressed[2] == True): print("Right click")
        pygame.display.update()
    
    def _draw_stat_menu(self):
        self.screen.fill((0, 0, 0))
        self.statMenu_resume_button.displayButton(self.screen)
        self.statMenu_attack_button.displayButton(self.screen)
        self.statMenu_defense_button.displayButton(self.screen)
        mousePressed = pygame.mouse.get_pressed()
        if(mousePressed[0] == True): 
            print("Left click")
            mousePos = pygame.mouse.get_pos()
            print(mousePos)
            if(self.statMenu_attack_button.isClicked(mousePos)):
                print("Attack button pressed")
            if(self.statMenu_defense_button.isClicked(mousePos)):
                print("Defense button pressed")
            if(self.statMenu_resume_button.isClicked(mousePos)):
                print("Resume button pressed")
                self.showStatMenu = False
                self.closedFromButton = True
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
            
    def statMenu_state(self, screen: pygame.Surface):
        if(self.showStatMenu): 
            self._draw_stat_menu()
        else: 
            self.screen = screen
            self.currCountStatMenu = 0

    def controlMenu_state(self, screen: pygame.Surface):
            if(self.showControlMenu): 
                ControlMenu(self.screen, self)._draw_control_menu()
            else: 
                self.screen = screen
                self.currCountControlMenu = 0
    def update(self,player,game_event):
        self.startMenu_state(self.screen)
        
        if(game_event == "option" and not self.closedFromButton): self.showOptionMenu = True
        elif(game_event == "no_option"): self.showOptionMenu = False
        self.optionMenu_state(self.screen)
        
        if(game_event == "stat" and not self.closedFromButton): self.showStatMenu = True
        elif(game_event == "no_stat"): self.showStatMenu = False
        self.statMenu_state(self.screen)
        
        self.controlMenu_state(self.screen)
        