from GUI.button import Button
from GUI.controlField import ControlField
from controls import Controls
import pygame
import sys

class ControlMenu:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        
        self.arialFont = pygame.font.SysFont('arial', 40)
        
        
        self.key_changed = None
        self.buttonCountControlMenu = 5
        self.currCountControlMenu = 0
        self.controlMenu_resume_button = Button("Resume", self, self.arialFont, "controls")
        self.controlMenu_left_key = ControlField("Left", Controls.LEFT, self, self.arialFont, "controls")
        self.controlMenu_right_key = ControlField("Right", Controls.RIGHT,self, self.arialFont, "controls")
        self.controlMenu_jump_key = ControlField("Jump", Controls.JUMP,self, self.arialFont, "controls")
        self.controlMenu_stat_key = ControlField("Stats", Controls.STAT_MENU,self, self.arialFont, "controls")
        
    def _draw_control_menu(self):
        self.screen.fill((0, 0, 0))
        
        self.controlMenu_resume_button.displayButton(self.screen)
        self.controlMenu_left_key.displayButton(self.screen)
        self.controlMenu_right_key.displayButton(self.screen)
        self.controlMenu_jump_key.displayButton(self.screen)
        self.controlMenu_stat_key.displayButton(self.screen)
        
        mousePressed = pygame.mouse.get_pressed()
        
        if(mousePressed[0] == True): 
            print("Left click")
            mousePos = pygame.mouse.get_pos()
            print(mousePos)
            if(self.controlMenu_resume_button.isClicked(mousePos)):
                print("Resume button pressed")
                self.game.showControlMenu = False
                self.game.closedFromButton = True
                self.game.showOptionMenu = True
                
            if(self.controlMenu_left_key.isClicked(mousePos)):
                print("Left button pressed")
                self._chose_key()
                Controls.LEFT = self.key_changed
                self.key_changed = None
                print("key left changed = ", Controls.LEFT)
                
            if(self.controlMenu_right_key.isClicked(mousePos)):
                print("Right button pressed")
                self._chose_key()
                Controls.RIGHT = self.key_changed
                self.key_changed = None
                print("key right changed = ", Controls.RIGHT)
                
            if(self.controlMenu_jump_key.isClicked(mousePos)):
                print("Jump button pressed")
                self._chose_key()
                Controls.JUMP = self.key_changed
                self.key_changed = None
                print("key jump changed = ", Controls.JUMP)
                
            if(self.controlMenu_stat_key.isClicked(mousePos)):
                print("Stat menu button pressed")
                self._chose_key()
                Controls.STAT_MENU = self.key_changed
                self.key_changed = None
                print("key stat menu changed = ", Controls.STAT_MENU)
        
        if(mousePressed[1] == True): print("Middle click")
        if(mousePressed[2] == True): print("Right click")
        pygame.display.update()
        
    def isKeyUsed(self, key):
        return True if key == Controls.LEFT or key == Controls.RIGHT or key == Controls.JUMP or key == Controls.STAT_MENU or key == Controls.MENU else False
    
    def _chose_key(self):
        while(self.key_changed == None):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    key = event.key
                    if self.isKeyUsed(key):
                        print("Key already used, try something else")
                    elif key != 1073741904 and key != 1073741903 and key != 32 and (key > 122 or key < 97):
                        print("Key should be a letter, right/left arrow or spaceBar")
                    else:
                        self.key_changed = key
                    
