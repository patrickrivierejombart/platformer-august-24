import pygame
import sys
from settings import HEIGHT, WIDTH
from GUI.button import Button

class StatField(Button):
    def __init__(self, text, game, font, category):
        super().__init__(text, game, font, category)
        self.jauge = 8
        self.font=font
        
        minusOffset = 10
        plusOffset = 500
        self.minusButton = Button(
            "-", 
            self, 
            font, 
            "", 
            [
                [self.coordTL[0] + minusOffset,self.coordTL[1]],
                [self.coordTR[0] + minusOffset,self.coordTR[1]],
                [self.coordBL[0] + minusOffset,self.coordBL[1]],
                [self.coordBR[0] + minusOffset,self.coordBR[1]]
            ]
        )
        self.plusButton = Button(
            "+", 
            self, 
            font, 
            "", 
            [
                [self.coordTL[0] + plusOffset,self.coordTL[1]],
                [self.coordTR[0] + plusOffset,self.coordTR[1]],
                [self.coordBL[0] + plusOffset,self.coordBL[1]],
                [self.coordBR[0] + plusOffset,self.coordBR[1]]
            ]
        )
        self.bars = []
        self.count = 0
        
    def isClicked(self, mousePos):
        if(self.minusButton.isClicked(mousePos) or self.plusButton.isClicked(mousePos)):
            self.updateJauge(mousePos)
            return True
        else:
            return False
    
    def updateJauge(self, mousePos):
        self.jauge += 1 if self.plusButton.isClicked(mousePos) and self.jauge < 10 else 0
        self.jauge -=1 if self.minusButton.isClicked(mousePos) and self.jauge > 0 else 0
        print("jauge " + str(self.jauge))
        self.bars = []
        self.count = 0
        for i in range(self.jauge): self.bars.append(self.font.render(str(self.count), True, (255, 255, 255))); self.count+=1
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAHHHHHHHHHHHHHHHHHHHHHHHHHHH",self.bars)
        
        
    def displayButton(self, screen):
        screen.blit(self.text, (self.coordTL[0]-200, self.coordTL[1]))
        currcount = 0
        self.minusButton.displayButton(screen)
        self.plusButton.displayButton(screen)
        while currcount < self.count: 
            screen.blit(self.bars[currcount], (self.coordTL[0]+ (currcount+1) * 40, self.coordTL[1]))
            currcount+=1
            # print("currCount = ", currcount)
        # for x in self.bars: screen.blit(x, (self.coordTL[0]+ 2, self.coordTL[1]))
        
    