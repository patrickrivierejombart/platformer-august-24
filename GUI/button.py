import pygame
import sys
from settings import HEIGHT, WIDTH


pygame.font.init()


class Button:
    def __init__(self, text, game, font, category):
        self.text = font.render(text, True, (255, 255, 255))
        if(category == "start"):
            self.buttonCountStartMenu = game.buttonCountStartMenu
            self.currCountStartMenu = game.currCountStartMenu +1
            game.currCountStartMenu +=1
            self._setCoords(self.buttonCountStartMenu, self.currCountStartMenu)
        elif(category == "options"):
            self.buttonCountOptionMenu = game.buttonCountOptionMenu
            self.currCountOptionMenu = game.currCountOptionMenu +1
            game.currCountOptionMenu +=1
            self._setCoords(self.buttonCountOptionMenu, self.currCountOptionMenu)
        self.print = 0
        
    def _setCoords(self, buttonCount, currCount):
        height = (HEIGHT/(buttonCount * 2))* (currCount + currCount-1)
        print("height",height, "currentButton", currCount)
        self.coordTL = [WIDTH/2 - self.text.get_width()/2, height - self.text.get_height()/2]
        self.coordTR = [WIDTH/2 + self.text.get_width()/2, height - self.text.get_height()/2]
        self.coordBL = [WIDTH/2 - self.text.get_width()/2, height + self.text.get_height()/2]
        self.coordBR = [WIDTH/2 + self.text.get_width()/2, height + self.text.get_height()/2]
        print("h"+str(currCount)+" = ("+ str(HEIGHT)+ "/ (" + str(buttonCount)+ "x2))x "+ str(currCount)+ "+" + str(currCount-1))
        
        
    def isClicked(self,mousePos):
            return True if (
                mousePos[0] <= self.coordBR[0] and 
                mousePos[0] >= self.coordBL[0] and 
                mousePos[1] <= self.coordBR[1] and 
                mousePos[1] >= self.coordTL[1]
                ) else False
            
    def displayButton(self, screen):
        screen.blit(self.text, (self.coordTL[0], self.coordTL[1]))
        if(self.print ==1): print(self.coordTL[0],self.coordTL[1])
        self.print+=1