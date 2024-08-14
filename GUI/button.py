import pygame
import sys
from settings import HEIGHT, WIDTH


pygame.font.init()


class Button:
    def __init__(self, text, game, font, category, coords=None):
        print(text, str(coords))
        self.text = font.render(text, True, (255, 255, 255))
        if(coords):
            self._setCoordsInnerButton(coords)
        elif(category == "start"):
            print("STAAAAAAAAAAAAAAAAAAAAAAAAARRRRRRRRRRRRRRRRRRRRRRRRRTTTTTTTTTTTTTTTTTTTTTTTTT")
            self.buttonCountStartMenu = game.buttonCountStartMenu
            self.currCountStartMenu = game.currCountStartMenu +1
            game.currCountStartMenu +=1
            self._setCoords(self.buttonCountStartMenu, self.currCountStartMenu)
        elif(category == "options"):
            print("CATEGOOOOOOOOOOOOOOOOOOOOOOOORYYYYYYYYYYYYYYYYYYY")
            self.buttonCountOptionMenu = game.buttonCountOptionMenu
            self.currCountOptionMenu = game.currCountOptionMenu +1
            game.currCountOptionMenu +=1
            self._setCoords(self.buttonCountOptionMenu, self.currCountOptionMenu)
        elif(category == "stats"):
            print("STAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAATS")
            self.buttonCountStatMenu = game.buttonCountStatMenu
            self.currCountStatMenu = game.currCountStatMenu +1
            game.currCountStatMenu +=1
            self._setCoords(self.buttonCountStatMenu, self.currCountStatMenu)
        self.print = 0
        
    def _setCoordsInnerButton(self, coords):
        self.coordTL = coords[0]
        self.coordTR = coords[1]
        self.coordBL = coords[2]
        self.coordBR = coords[3]
        
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