from abc import ABC, abstractmethod
from ENTITY.player.player import Player
from pygame import Surface


class Camera:    
    def setmethod(self, method):
        self.method = method

    def scroll(self):
        self.method.scroll()
    
    def render_scroll(self):
        return self.method.render_scroll()


class CamScroll(ABC):
    def __init__(self, player: Player, display: Surface):
        self.player = player
        self.display = display
        self.offset = [0, 0]
    
    @abstractmethod
    def scroll(self):
        pass

    @abstractmethod
    def render_scroll(self):
        pass


class Follow(CamScroll):
    def __init__(self, player, display):
        CamScroll.__init__(self, player, display)
    
    def scroll(self):
        self.offset[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.offset[0]) / 30
        self.offset[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.offset[1]) / 30

    def render_scroll(self):
        return (int(self.offset[0]), int(self.offset[1]))
