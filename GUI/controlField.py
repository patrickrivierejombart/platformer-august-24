import pygame
import sys
from settings import HEIGHT, WIDTH
from GUI.button import Button

class ControlField(Button):
    def __init__(self, name, key, game, font, category):
        if(key == 1073741904):
            text = "<"
        elif(key == 1073741903):
            text = ">"
        elif(key == 32):
            text ="Space_bar"
        else:
            text = chr(key)
        super().__init__(name, game, font, category)
        self.font=font
        
        Offset = 10
        self.key = Button(
            text, 
            self, 
            font, 
            "", 
            [
                [self.coordTL[0] + Offset,self.coordTL[1]],
                [self.coordTR[0] + Offset,self.coordTR[1]],
                [self.coordBL[0] + Offset,self.coordBL[1]],
                [self.coordBR[0] + Offset,self.coordBR[1]]
            ]
        )
        self.bars = []
        self.count = 0
        
    def isClicked(self, mousePos):
        if(self.key.isClicked(mousePos)):
            return True
        else:
            return False
    
    def displayButton(self, screen):
        screen.blit(self.text, (self.coordTL[0]-200, self.coordTL[1]))
        self.key.displayButton(screen)
        
    